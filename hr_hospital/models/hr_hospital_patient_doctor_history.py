"""
Model for storing the history of changes in
assigned personal doctors for hospital patients.
"""

from odoo import models, fields, api


class PatientDoctorHistory(models.Model):
    """
    Stores historical records of personal doctor changes for a patient.
    """

    _name = 'hr.hospital.patient.doctor.history'
    _description = 'History of changes in personal doctors'

    name = fields.Char(
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: 'New'
    )

    active = fields.Boolean(
        default=True
    )
    patient_id = fields.Many2one(
        comodel_name='hr.hospital.patient',
        string="Patient",
        required=True,
        ondelete='cascade'
    )
    doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string="Doctor",
        required=True,
        ondelete='restrict'
    )
    assign_date = fields.Date(
        string="Appointment date",
        required=True,
        default=fields.Date.context_today
    )
    change_date = fields.Date(
        string="Change date"
    )
    change_reason = fields.Text(
        string="Reason for change"
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = (
                    self.env['ir.sequence']
                    .next_by_code('hr.hospital.patient.doctor.history')
                    or 'New'
                )

        records = super().create(vals_list)

        for record in records:
            if record.patient_id:
                prev = self.search([
                    ('patient_id', '=', record.patient_id.id),
                    ('active', '=', True),
                    ('id', '!=', record.id),
                ])
                prev.write({
                    'active': False,
                    'change_date': fields.Date.context_today(self),
                })

        return records
