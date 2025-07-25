from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class PatientVisit(models.Model):
    _name = 'hr.hospital.patient.visit'
    _description = _('Patient visits')

    name = fields.Char(
        string=_("Name"),
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: _('New')
    )
    planned_datetime = fields.Datetime(
        string=_('Scheduled date/time'),
        required=True
    )
    actual_datetime = fields.Datetime(
        string=_("Actual date and time of visit"),
        readonly=True
    )
    status = fields.Selection(
        [
            ('planned', _('Scheduled')),
            ('done', _('Completed')),
            ('cancelled', _('Cancelled')),
            ('no_show', _('Didn\'t show up')),
        ],
        string=_('Status'),
        required=True,
        default='planned'
    )
    patient_id = fields.Many2one(
        comodel_name='hr.hospital.patient',
        string=_('Patient'),
        required=True
    )
    doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string=_('Doctor'),
        required=True,
        ondelete='restrict',
        domain="[('license_number', '!=', False)]"
    )
    visit_type = fields.Selection(
        [
            ('primary', _('Primary')),
            ('repeat', _('Repeat')),
            ('preventive', _('Preventive')),
            ('emergency', _('Emergency')),
        ],
        string=_("Type of visit")
    )
    diagnosis_ids = fields.One2many(
        comodel_name='hr.hospital.medical.diagnosis',
        inverse_name='visit_id',
        string=_("Diagnoses")
    )
    recommendation = fields.Html(
        string=_("Recommendations")
    )
    amount = fields.Monetary(
        string=_("Cost of visit"),
        currency_field='currency_id'
    )
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string=_("Currency")
    )

    diagnosis_count = fields.Integer(
        string=_("Count of diagnoses"),
        compute='_compute_diagnosis_count',
        store=True
    )
    visit_unit = fields.Integer(
        string=_("Visit Unit"),
        default=1
    )

    @api.depends('diagnosis_ids')
    def _compute_diagnosis_count(self):
        for rec in self:
            rec.diagnosis_count = len(rec.diagnosis_ids)

    @api.constrains('doctor_id', 'patient_id', 'planned_datetime')
    def _check_unique_patient_doctor_per_day(self):
        for rec in self:
            if rec.doctor_id and rec.patient_id and rec.planned_datetime:
                domain = [
                    ('id', '!=', rec.id),
                    ('doctor_id', '=', rec.doctor_id.id),
                    ('patient_id', '=', rec.patient_id.id),
                    ('planned_datetime', '>=', rec.planned_datetime.replace(
                        hour=0, minute=0, second=0
                    )),
                    ('planned_datetime', '<', rec.planned_datetime.replace(
                        hour=23, minute=59, second=59
                    )),
                ]
                count = self.search_count(domain)
                if count > 0:
                    raise ValidationError(
                        _("A patient cannot be scheduled with the same doctor more than once a day.")
                    )

    @api.onchange('patient_id')
    def _onchange_patient_id(self):
        if self.patient_id and self.patient_id.allergies:
            message = _("The patient has allergies: ") + self.patient_id.allergies
            return {
                'warning': {
                    'title': _("Attention: patient allergies"),
                    'message': message
                }
            }

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'] \
                .next_by_code('hr.hospital.patient.visit') or _('New')
        return super().create(vals)

    def unlink(self):
        for rec in self:
            if rec.diagnosis_ids:
                raise ValidationError(
                    _("You cannot delete a visit for which diagnoses exist.")
                )
        return super().unlink()
