from odoo import models, fields, api, _
from odoo.exceptions import UserError

class MassReassignDoctorWizard(models.TransientModel):
    _name = 'hr.hospital.mass.reassign.doctor.wizard'
    _description = 'Візард масового перепризначення лікаря'

    old_doctor_id = fields.Many2one(
        'hr.hospital.doctor',
        string="Старий лікар",
        required=False
    )
    new_doctor_id = fields.Many2one(
        'hr.hospital.doctor',
        string="Новий лікар",
        required=True
    )
    patient_ids = fields.Many2many(
        'hr.hospital.patient',
        string="Пацієнти",
        domain="[('personal_doctor_id', '=', old_doctor_id)]"
    )
    change_date = fields.Date(
        string="Дата зміни",
        default=fields.Date.context_today
    )
    change_reason = fields.Text(
        string="Причина зміни",
        required=True
    )

    @api.onchange('old_doctor_id')
    def _onchange_old_doctor_id(self):
        if self.old_doctor_id:
            return {
                'domain': {
                    'patient_ids': [('personal_doctor_id', '=', self.old_doctor_id.id)]
                }
            }
        else:
            return {
                'domain': {
                    'patient_ids': []
                }
            }

    def action_reassign(self):
        if not self.patient_ids:
            raise UserError(_("Оберіть принаймні одного пацієнта для перепризначення."))
        for patient in self.patient_ids:
            patient.write({
                'personal_doctor_id': self.new_doctor_id.id
            })

            self.env['hr.hospital.patient.doctor.history'].create({
                'patient_id': patient.id,
                'doctor_id': self.new_doctor_id.id,
                'assign_date': self.change_date,
                'change_reason': self.change_reason,
                'active': True,
            })
        return {'type': 'ir.actions.act_window_close'}