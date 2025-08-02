"""Medical diagnosis model for the hr_hospital module."""

from datetime import timedelta

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Diagnosis(models.Model):
    """Model representing medical diagnoses."""

    _name = 'hr.hospital.medical.diagnosis'
    _description = 'Diagnosis'

    name = fields.Char(
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: 'New'
    )

    visit_id = fields.Many2one(
        comodel_name='hr.hospital.patient.visit',
        string="Visit",
        required=True,
        ondelete='cascade',
        domain=lambda self: [
            ('state', '=', 'done'),
            (
                'visit_date',
                '>=',
                (
                    fields.Date.today() - timedelta(days=30)
                ).strftime('%Y-%m-%d')
            )
        ]
    )
    disease_id = fields.Many2one(
        comodel_name='hr.hospital.type.of.disease',
        string="Disease",
        required=True,
        domain=[
            ('is_contagious', '=', True),
            ('danger_level', 'in', ['high', 'critical'])
        ]
    )
    description = fields.Text(
        string="Description of diagnosis"
    )
    treatment = fields.Html(
        string="Prescribed treatment"
    )
    is_approved = fields.Boolean(
        string="Approved",
        default=False
    )
    approved_by_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string="The doctor who approved",
        readonly=True
    )
    approved_date = fields.Datetime(
        string="Approval date",
        readonly=True
    )
    severity = fields.Selection(
        [
            ('mild', 'Mild'),
            ('moderate', 'Moderate'),
            ('severe', 'Severe'),
            ('critical', 'Critical'),
        ],
    )
    diagnosis_unit = fields.Integer(
        string="Visit Unit",
        default=1
    )

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = (
                self.env['ir.sequence']
                .next_by_code('hr.hospital.medical.diagnosis')
                or 'New'
            )
        return super().create(vals)

    def action_approve(self):
        """
        Approves the medical diagnosis if it hasn't been approved yet.

        If the current user has an associated doctor profile,
        sets that doctor as the one who approved the diagnosis.
        Also records the approval timestamp.

        Raises:
            ValidationError: If the diagnosis is already approved.
        """
        for rec in self:
            if not rec.is_approved:
                if hasattr(self.env.user, 'doctor_id'):
                    approved_by_id = self.env.user.doctor_id.id
                else:
                    approved_by_id = False
                rec.write({
                    'is_approved': True,
                    'approved_by_id': approved_by_id,
                    'approved_date': fields.Datetime.now(),
                })
            else:
                raise ValidationError(
                    _("The diagnosis has already been confirmed.")
                )
