from odoo import models, fields, api

class Specialization(models.Model):
    _name = 'hr.hospital.specialization'
    _description = 'Спеціалізації'

    name = fields.Char(
        string='Назва',
        required=True
    )
    description = fields.Text(
        string='Опис'
    )
    active = fields.Boolean(
        string='Активний',
        default=True
    )
