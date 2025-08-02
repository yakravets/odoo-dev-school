"""Doctor model for HR Hospital module."""

from datetime import date

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Doctor(models.Model):
    """Represents a doctor in the hospital system."""

    _name = 'hr.hospital.doctor'
    _description = 'Doctor'
    _inherit = 'hr.hospital.abstract.person'

    _sql_constraints = [
        ('unique_license_number', 'unique(license_number)',
            'The license number must be unique!'),
        ('check_rating_range', 'CHECK(rating >= 0.00 AND rating <= 5.00)',
            'The rating must be from 0.00 to 5.00!'),
    ]

    user_id = fields.Many2one(
        comodel_name='res.users',
        string="System user"
    )
    specialization_id = fields.Many2one(
        comodel_name='hr.hospital.specialization',
        string='Specialization',
        required=True
    )
    is_intern = fields.Boolean(
        string="Intern"
    )
    mentor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string="Mentor doctor",
        domain="[('is_intern', '=', False)]"
    )
    license_number = fields.Char(
        string="License number",
        required=True,
        copy=False
    )
    license_issue_date = fields.Date(
        string="License issue date"
    )
    work_experience = fields.Integer(
        string="Work experience (years)",
        compute='_compute_work_experience',
        store=True
    )
    rating = fields.Float(
        digits=(3, 2),
        default=0.0
    )
    schedule_ids = fields.One2many(
        comodel_name='hr.hospital.doctor.schedule',
        inverse_name='doctor_id',
        string="Work schedule"
    )
    education_country_id = fields.Many2one(
        comodel_name='res.country',
        string="Country of study"
    )
    intern_ids = fields.One2many(
        comodel_name='hr.hospital.doctor',
        inverse_name='mentor_id',
        string="Interns",
        domain=[('is_intern', '=', True)],
        readonly=True,
    )
    visit_ids = fields.One2many(
        comodel_name='hr.hospital.patient.visit',
        inverse_name='doctor_id',
        string="Work schedule"
    )

    @api.depends('license_issue_date')
    def _compute_work_experience(self):
        today = date.today()
        for record in self:
            if record.license_issue_date:
                experience = _calculate_work_experience(record, today)
                record.work_experience = max(0, experience)
            else:
                record.work_experience = 0

    @api.constrains('mentor_id')
    def _check_mentor_is_not_intern(self):
        for rec in self:
            if rec.mentor_id and rec.mentor_id.is_intern:
                raise ValidationError(
                    _("An intern cannot be a mentor physician.")
                )

    @api.constrains('rating')
    def _check_rating(self):
        for record in self:
            if record.rating < 0.0 or record.rating > 5.0:
                raise ValidationError(
                    _("The rating must be between 0.00 and 5.00.")
                )
            if record.mentor_id \
                    and record.id \
                    and record.mentor_id.id == record.id:

                raise ValidationError(
                    _("A doctor cannot be his own mentor.")
                )

    @api.constrains('mentor_id', 'is_intern')
    def _check_mentor(self):
        for record in self:
            if record.is_intern and not record.mentor_id:
                raise ValidationError(
                    _("For interns, it is mandatory to indicate"
                        " a mentor physician.")
                )
            if not record.is_intern and record.mentor_id:
                raise ValidationError(
                    _("Only interns can have a mentor doctor.")
                )

    @api.onchange('is_intern')
    def _onchange_is_intern(self):
        if self.is_intern and not self.mentor_id:
            mentor = self.env['hr.hospital.doctor'].search(
                [
                    ('is_intern', '=', False)
                ],
                limit=1
            )
            if mentor:
                self.mentor_id = mentor.id

    def action_create_visit_quick(self):
        """
        Open a form view to quickly create a new patient visit.

        Ensures the method is called on a single record and returns an action
        dictionary to open a modal form for 'hr.hospital.patient.visit',
        pre-filling the doctor and planned datetime fields.

        Returns:
            dict: Odoo action to open the patient visit form view as a popup.
        """
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('New Patient Visit'),
            'res_model': 'hr.hospital.patient.visit',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_doctor_id': self.id,
                'default_planned_datetime': fields.Datetime.now(),
            }
        }


def _calculate_work_experience(record, today):
    return (
        today.year
        - record.license_issue_date.year
        - (
            (today.month, today.day)
            < (record.license_issue_date.month, record.license_issue_date.day)
        )
    )
