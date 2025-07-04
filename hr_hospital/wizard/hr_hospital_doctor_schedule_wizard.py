from odoo import models, fields, api, _
from datetime import timedelta

class DoctorScheduleWizard(models.TransientModel):
    _name = 'hr.hospital.doctor.schedule.wizard'
    _description = _('Doctor Schedule Wizard')

    doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor', 
        string=_('Doctor'), 
        required=True
    )
    date_start = fields.Date(
        string=_('Start week'), 
        required=True
    )
    week_count = fields.Integer(
        string=_('Number of weeks'), 
        default=1, 
        required=True
    )
    schedule_type = fields.Selection(  
        [
            ('standard', _('Standard')),
            ('even', _('Even week')),
            ('odd', _('Odd week'))
        ], 
        string=_('Schedule type'), 
        default='standard')

    monday = fields.Boolean(
        string=_('Monday')
    )
    tuesday = fields.Boolean(
        string=_('Tuesday')
    )
    wednesday = fields.Boolean(
        string=_('Wednesday')
    )
    thursday = fields.Boolean(
        string=_('Thursday')
    )
    friday = fields.Boolean(
        string=_('Friday')
    )
    saturday = fields.Boolean(
        string=_('Saturday')
    )
    sunday = fields.Boolean(
        string=_('Sunday')
    )

    time_start = fields.Float(
        string=_('Start time')
    )
    time_end = fields.Float(
        string=_('End time')
    )
    break_from = fields.Float(
        string=_('Break from')
    )
    break_to = fields.Float(
        string=_('Break to')
    )

    @api.model
    def _float_to_time(self, float_hour):
        hours = int(float_hour)
        minutes = int(round((float_hour - hours) * 60))
        return f'{hours:02d}:{minutes:02d}'

    def action_generate_schedule(self):
        Schedule = self.env['hr.hospital.schedule']

        weekdays = {
            0: self.monday,
            1: self.tuesday,
            2: self.wednesday,
            3: self.thursday,
            4: self.friday,
            5: self.saturday,
            6: self.sunday,
        }

        current_date = self.date_start
        for week in range(self.week_count):
            for day_offset in range(7):
                day = current_date + timedelta(days=day_offset + week * 7)
                weekday = day.weekday()  # 0 = Monday
                is_even = ((day.isocalendar()[1] % 2) == 0)

                if weekdays.get(weekday):
                    if self.schedule_type == 'even' and not is_even:
                        continue
                    if self.schedule_type == 'odd' and is_even:
                        continue

                    Schedule.create({
                        'doctor_id': self.doctor_id.id,
                        'date': day,
                        'time_start': self._float_to_time(self.time_start),
                        'time_end': self._float_to_time(self.time_end),
                        'break_from': self._float_to_time(self.break_from),
                        'break_to': self._float_to_time(self.break_to),
                    })
