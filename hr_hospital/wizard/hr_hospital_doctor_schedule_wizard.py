"""
Wizard for generating or viewing the schedule of a specific doctor.
"""

from datetime import timedelta
from odoo import models, fields, api


class DoctorScheduleWizard(models.TransientModel):
    """
    Transient wizard model to assist with viewing
    or creating doctor schedules.
    """

    _name = 'hr.hospital.doctor.schedule.wizard'
    _description = 'Doctor Schedule Wizard'

    doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string='Doctor',
        required=True
    )
    date_start = fields.Date(
        string='Start week',
        required=True
    )
    week_count = fields.Integer(
        string='Number of weeks',
        default=1,
        required=True
    )
    schedule_type = fields.Selection(
        [
            ('workday', 'Working day'),
            ('vacation', 'Leave'),
            ('sick_leave', 'Hospital'),
            ('conference', 'Conference'),
        ],
        string='Schedule type',
        default='workday'
    )
    monday = fields.Boolean()
    tuesday = fields.Boolean()
    wednesday = fields.Boolean()
    thursday = fields.Boolean()
    friday = fields.Boolean()
    saturday = fields.Boolean()
    sunday = fields.Boolean()
    time_start = fields.Float(
        string='Start time'
    )
    time_end = fields.Float(
        string='End time'
    )

    @api.model
    def _float_to_time(self, float_hour):
        """
        Convert a float hour (e.g., 13.5) to time string format
        (e.g., '13:30').

        :param float_hour: Float representation of hours.
        :return: Time in 'HH:MM' format as a string.
        """

        hours = int(float_hour)
        minutes = int(round((float_hour - hours) * 60))
        return f'{hours:02d}:{minutes:02d}'

    def action_generate_schedule(self):
        """
        Generate a schedule for a doctor over a specified number of weeks,
        based on selected weekdays and schedule type (all, even, odd).

        For each selected weekday, creates a schedule record with specified
        start/end time and break time, adjusting based on whether
        the week is even or odd.
        """

        schedule = self.env['hr.hospital.doctor.schedule']

        current_date = self.date_start
        for week in range(self.week_count):
            for day_offset in range(7):
                day = current_date + timedelta(days=day_offset + week * 7)
                # 0 is Monday.
                weekday = day.weekday()

                is_work = (self.monday and weekday == 0)\
                    or (self.tuesday and weekday == 1)\
                    or (self.wednesday and weekday == 2)\
                    or (self.thursday and weekday == 3)\
                    or (self.friday and weekday == 4)\
                    or (self.saturday and weekday == 5)\
                    or (self.sunday and weekday == 6)

                if not is_work:
                    continue

                schedule.create({
                    'doctor_id': self.doctor_id.id,
                    'date': day,
                    'schedule_type': self.schedule_type,
                    'day_of_week': [
                        'mon',
                        'tue',
                        'wed',
                        'thu',
                        'fri',
                        'sat',
                        'sun'
                    ][weekday],
                    'from_time': self.time_start,
                    'to_time': self.time_end,
                })
