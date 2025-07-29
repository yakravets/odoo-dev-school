"""Doctor schedule model for the hr_hospital module."""

from odoo import models, fields, api, _


class DoctorSchedule(models.Model):
    """Model representing the schedule of a doctor."""

    _name = 'hr.hospital.doctor.schedule'
    _description = _('Doctor schedule')
    _sql_constraints = [
        ('check_time', 'CHECK(to_time > from_time)',
            _('The end time must be after the start time!')),
    ]

    name = fields.Char(
        string=_("Name"),
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: _('New')
    )

    doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string=_("Doctor"),
        required=True,
        ondelete='cascade',
        domain="[('specialization_id', '!=', False)]"
    )
    day_of_week = fields.Selection(
        [
            ('mon', _('Monday')),
            ('tue', _('Tuesday')),
            ('wed', _('Wednesday')),
            ('thu', _('Thursday')),
            ('fri', _('Friday')),
            ('sat', _('Saturday')),
            ('sun', _('Sunday'))
        ],
        string=_("Day of the week")
    )
    date = fields.Date(
        string=_("Date (specific)")
    )
    from_time = fields.Float(
        string=_("Start time")
    )
    to_time = fields.Float(
        string=_("End time")
    )
    schedule_type = fields.Selection(
        [
            ('workday', _('Working day')),
            ('vacation', _('Leave')),
            ('sick_leave', _('Hospital')),
            ('conference', _('Conference')),
        ],
        string=_("Type")
    )
    note = fields.Char(
        string=_("Notes")
    )

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'] \
                .next_by_code('hr.hospital.doctor.schedule') or _('New')
        return super().create(vals)
