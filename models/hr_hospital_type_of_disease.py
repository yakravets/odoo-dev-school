from odoo import models, fields, api

class TypeOfDisease(models.Model):
    _name = 'hr.hospital.type.of.disease'
    _description = 'Захворювання(хвороби)'

    name = fields.Char(
        string='Назва',
        required=True
    )
    severity = fields.Selection(
        selection=[
            ('mild', 'Легкий'),
            ('moderate', 'Середній'),
            ('severe', 'Важкий')
        ],
        string='Серйозність',
        required=True
    )