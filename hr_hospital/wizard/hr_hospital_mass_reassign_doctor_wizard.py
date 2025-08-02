"""
Mass Doctor Reassignment Wizard module
"""

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class MassReassignDoctorWizard(models.TransientModel):
    """
    Wizard for mass reassignment of doctors in patient visits.
    Allows selecting an old doctor and new doctor, and reassigns
    patient visits within an optional date range.
    """

    _name = 'hr.hospital.mass.reassign.doctor.wizard'
    _description = 'Mass Doctor Reassignment Wizard'

    old_doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string="Old doctor",
        required=False
    )
    new_doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string="New doctor",
        required=True
    )
    patient_ids = fields.Many2many(
        comodel_name='hr.hospital.patient',
        string="Patients",
        domain="[('personal_doctor_id', '=', old_doctor_id)]"
    )
    change_date = fields.Date(
        string="Change date",
        default=fields.Date.context_today
    )
    change_reason = fields.Text(
        string="Reason for change",
        required=True
    )

    @api.onchange('old_doctor_id')
    def _onchange_old_doctor_id(self):
        if self.old_doctor_id:
            return {
                'domain': {
                    'patient_ids': [
                        ('personal_doctor_id', '=', self.old_doctor_id.id)
                    ]
                }
            }

        return {
            'domain': {
                'patient_ids': []
            }
        }

    def action_reassign(self):
        """
        Reassigns selected patients to a new doctor.

        Raises:
            UserError: If no patients are selected.

        For each selected patient, updates the personal doctor
        to the new doctor, and creates a history record logging
        the reassignment with date and reason.

        Closes the wizard window upon completion.
        """

        if not self.patient_ids:
            raise UserError(
                _("Select at least one patient to reassign.")
            )
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

        return {
            'type': 'ir.actions.act_window_close'
        }
