from odoo import models, fields, api

class Patient(models.Model):
    _name = 'hr.hospital.patient'
    _description = 'Пацієнти'

    name = fields.Char(
        string='Прізвище та ім\'я',
        required=True
    )
    phone = fields.Char(
        string='Номер телефону',
        required=True
    )
    birth_date = fields.Date(
        string='Дата народження',
        required=True
    )
    home_addess = fields.Char(
        string='Домашня адреса'
    )
    gender = fields.Selection(
        [
            ('unknown', 'Не вказана'),
            ('man', 'Чоловік'),
            ('woman', 'Жінка'),
        ], 
        string='Стать', 
        required=True, 
        default='unknown'
    )
    