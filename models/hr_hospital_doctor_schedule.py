from odoo import models, fields

class DoctorSchedule(models.Model):
    _name = 'hr.hospital.doctor.schedule'
    _description = 'Розклад лікаря'
    _sql_constraints = [
        ('check_time', 'CHECK(to_time > from_time)', 'Час закінчення повинен бути після часу початку!'),
    ]

    doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string="Лікар",
        required=True,
        ondelete='cascade'
    )
    day_of_week = fields.Selection(
        [
            ('mon', 'Понеділок'),
            ('tue', 'Вівторок'),
            ('wed', 'Середа'),
            ('thu', 'Четвер'),
            ('fri', 'П\'ятниця'),
            ('sat', 'Субота'),
            ('sun', 'Неділя')
        ],
        string="День тижня"
    )
    date = fields.Date(
        string="Дата (конкретна)"
    )
    from_time = fields.Float(
        string="Час початку"
    )
    to_time = fields.Float(
        string="Час закінчення"
    )
    schedule_type = fields.Selection(
        [
            ('workday', 'Робочий день'),
            ('vacation', 'Відпустка'),
            ('sick_leave', 'Лікарняний'),
            ('conference', 'Конференція'),
        ],
        string="Тип"
    )
    note = fields.Char(
        string="Примітки"
    )