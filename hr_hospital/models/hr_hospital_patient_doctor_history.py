from odoo import models, fields, api, _


class PatientDoctorHistory(models.Model):
    _name = 'hr.hospital.patient.doctor.history'
    _description = _('History of changes in personal doctors')

    name = fields.Char(
        string=_("Name"),
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: _('New')
    )

    active = fields.Boolean(
        string=_("Active"),
        default=True
    )
    patient_id = fields.Many2one(
        comodel_name='hr.hospital.patient',
        string=_("Patient"),
        required=True,
        ondelete='cascade'
    )
    doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string=_("Doctor"),
        required=True,
        ondelete='restrict'
    )
    assign_date = fields.Date(
        string=_("Appointment date"),
        required=True,
        default=fields.Date.context_today
    )
    change_date = fields.Date(
        string=_("Change date")
    )
    change_reason = fields.Text(
        string=_("Reason for change")
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'] \
                    .next_by_code('hr.hospital.patient.doctor.history') or _('New')

        records = super().create(vals_list)

        for record in records:
            if record.patient_id:
                prev = self.search([
                    ('patient_id', '=', record.patient_id.id),
                    ('active', '=', True),
                    ('id', '!=', record.id),
                ])
                prev.write(
                    {
                        'active': False,
                        'change_date': fields.Date.context_today(self)
                    }
                )
        return records
