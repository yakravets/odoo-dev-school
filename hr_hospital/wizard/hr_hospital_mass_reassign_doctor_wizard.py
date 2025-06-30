from odoo import models, fields, api, _
from odoo.exceptions import UserError

class MassReassignDoctorWizard(models.TransientModel):
    _name = 'hr.hospital.mass.reassign.doctor.wizard'
    _description = _('Mass Doctor Reassignment Wizard')

    old_doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string=_("Old doctor"),
        required=False
    )
    new_doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string=_("New doctor"),
        required=True
    )
    patient_ids = fields.Many2many(
        comodel_name='hr.hospital.patient',
        string=_("Patients"),
        domain="[('personal_doctor_id', '=', old_doctor_id)]"
    )
    change_date = fields.Date(
        string=_("Change date"),
        default=fields.Date.context_today
    )
    change_reason = fields.Text(
        string=_("Reason for change"),
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
            raise UserError(_("Select at least one patient to reassign."))
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