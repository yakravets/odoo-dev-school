"""Doctor schedule model for the hr_hospital module."""

from odoo import models, fields, api


class DoctorSchedule(models.Model):
    """Model representing the schedule of a doctor."""

    _name = 'hr.hospital.doctor.schedule'
    _description = 'Doctor schedule'
    _sql_constraints = [
        ('check_time', 'CHECK(to_time > from_time)',
            'The end time must be after the start time!'),
    ]

    name = fields.Char(
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: 'New'
    )

    doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string="Doctor",
        required=True,
        ondelete='cascade',
        domain="[('specialization_id', '!=', False)]"
    )
    day_of_week = fields.Selection(
        [
            ('mon', 'Monday'),
            ('tue', 'Tuesday'),
            ('wed', 'Wednesday'),
            ('thu', 'Thursday'),
            ('fri', 'Friday'),
            ('sat', 'Saturday'),
            ('sun', 'Sunday')
        ],
        string="Day of the week"
    )
    date = fields.Date(
        string="Date (specific)"
    )
    from_time = fields.Float(
        string="Start time"
    )
    to_time = fields.Float(
        string="End time"
    )
    schedule_type = fields.Selection(
        [
            ('workday', 'Working day'),
            ('vacation', 'Leave'),
            ('sick_leave', 'Hospital'),
            ('conference', 'Conference'),
        ],
        string="Type"
    )
    note = fields.Char(
        string="Notes"
    )

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'] \
                .next_by_code('hr.hospital.doctor.schedule') or 'New'
        return super().create(vals)
