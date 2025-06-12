from odoo import models, fields, api

class Doctor(models.Model):
    _name = 'hr.hospital.doctor'
    _description = 'Лікарі'

    name = fields.Char(
        string='Прізвище та ім\'я',
        required=True
    )
    phone = fields.Char(
        string='Номер телефону',
        required=True
    )
    email = fields.Char(
        string='Електронна пошта',
    )
    specialization = fields.Many2one(
        comodel_name='hr.hospital.specialization',
        string='Спеціалізація',
        required=True
    )
    active = fields.Boolean(
        string='Активний',
        default=True
    )