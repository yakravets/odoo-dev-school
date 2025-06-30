from odoo import models, fields, api

class Specialization(models.Model):
    _name = 'hr.hospital.specialization'
    _description = 'Спеціалізації'
 
    name = fields.Char(
        string='Назва',
        required=True
    )
    active = fields.Boolean(
        string='Активний',
        default=True
    )
    code = fields.Char(
        string="Код спеціальності", 
        size=10, 
        required=True
    )
    description = fields.Text(
        string="Опис"
    )
    doctor_ids = fields.One2many(
        comodel_name='hr.hospital.doctor', 
        inverse_name='specialization_id', 
        string="Лікарі"
    )
