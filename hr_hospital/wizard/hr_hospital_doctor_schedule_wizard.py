from odoo import models, fields, api
from datetime import timedelta, datetime

class DoctorScheduleWizard(models.TransientModel):
    _name = 'hr.hospital.doctor.schedule.wizard'
    _description = 'Doctor Schedule Wizard'

    doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor', 
        string='Лікар', 
        required=True
    )
    date_start = fields.Date(
        string='Тиждень початку', 
        required=True
    )
    week_count = fields.Integer(
        string='Кількість тижнів', 
        default=1, 
        required=True
    )
    schedule_type = fields.Selection(  
        [
            ('standard', 'Стандартний'),
            ('even', 'Парний тиждень'),
            ('odd', 'Непарний тиждень')
        ], 
        string='Тип розкладу', 
        default='standard')

    monday = fields.Boolean(string='Понеділок')
    tuesday = fields.Boolean(string='Вівторок')
    wednesday = fields.Boolean(string='Середа')
    thursday = fields.Boolean(string='Четвер')
    friday = fields.Boolean(string='Пʼятниця')
    saturday = fields.Boolean(string='Субота')
    sunday = fields.Boolean(string='Неділя')

    time_start = fields.Float(string='Час початку')
    time_end = fields.Float(string='Час закінчення')
    break_from = fields.Float(string='Перерва з')
    break_to = fields.Float(string='Перерва до')

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
