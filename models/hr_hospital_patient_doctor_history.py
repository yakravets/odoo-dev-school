from odoo import models, fields, api

class PatientDoctorHistory(models.Model):
    _name = 'hr.hospital.patient.doctor.history'
    _description = 'Історія змін персональних лікарів'

    active = fields.Boolean(
        string="Активний", 
        default=True
    )
    patient_id = fields.Many2one(
        comodel_name='hr.hospital.patient',
        string="Пацієнт",
        required=True,
        ondelete='cascade'
    )
    doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string="Лікар",
        required=True,
        ondelete='restrict'
    )
    assign_date = fields.Date(
        string="Дата призначення",
        required=True,
        default=fields.Date.context_today
    )
    change_date = fields.Date(
        string="Дата зміни"
    )
    change_reason = fields.Text(
        string="Причина зміни"
    )

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for record in records:
            if record.patient_id:
                prev = self.search([
                    ('patient_id', '=', record.patient_id.id),
                    ('active', '=', True),
                    ('id', '!=', record.id),
                ])
                prev.write({'active': False, 'change_date': fields.Date.context_today(self)})
        return records
    