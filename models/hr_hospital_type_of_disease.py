from odoo import models, fields, api

class TypeOfDisease(models.Model):
    _name = 'hr.hospital.type.of.disease'
    _description = 'Захворювання(хвороби)'

    name = fields.Char(
        string='Назва',
        required=True
    )
    active = fields.Boolean(
        string='Активний',
        default=True
    )
    parent_id = fields.Many2one(
        comodel_name='hr.hospital.type.of.disease',
        string="Батьківська хвороба",
        ondelete='set null'
    )
    child_ids = fields.One2many(
        comodel_name='hr.hospital.type.of.disease',
        inverse_name='parent_id',
        string="Дочірні хвороби"
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
    icd10_code = fields.Char(string="Код МКХ-10", size=10)
    danger_level = fields.Selection(
        [
            ('low', 'Низький'),
            ('medium', 'Середній'),
            ('high', 'Високий'),
            ('critical', 'Критичний'),
        ],
        string="Ступінь небезпеки"
    )
    is_contagious = fields.Boolean(
        string="Заразна"
    )
    symptoms = fields.Text(
        string="Симптоми"
    )
    region_ids = fields.Many2many(
        comodel_name='res.country',
        relation='hr_hospital_type_of_disease_country_rel',
        column1='disease_id',
        column2='country_id',
        string="Регіон поширення"
    )
    