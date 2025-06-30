from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re
from datetime import date

class AbstractPerson(models.AbstractModel):
    _name = 'hr.hospital.abstract.person'
    _description = 'Abstract Person Model'
    _inherit = ['image.mixin']
    _abstract = True


    first_name = fields.Char(
        string='Ім\'я',
        required=True
    )
    last_name = fields.Char(
        string='Прізвище',
        required=True
    )
    middle_name = fields.Char(
        string='По батькові',   
    )    
    name = fields.Char(
        string='Повне ім\'я',
        compute='_compute_name',
        readonly=True,
        store=True
    )
    active = fields.Boolean(
        string='Активний',
        default=True
    )

    phone = fields.Char(
        string='Номер телефону',
        required=True
    )
    email = fields.Char(
        string='Електронна пошта',
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
    birth_date = fields.Date(
        string='Дата народження',
        required=True
    )
    age = fields.Integer(
        string="Вік", 
        compute='_compute_age', 
        readonly=True,
        store=True
    )
    citizenship_country_id = fields.Many2one(
        comodel_name='res.country',
        string='Країна громадянства',
    )
    language_id = fields.Many2one(
        comodel_name='res.lang',
        string='Мова спілкування',
    )

    @api.depends('birth_date')
    def _compute_age(self):
        for record in self:
            if record.birth_date:
                today = date.today()
                born = record.birth_date
                age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
                record.age = age
            else:
                record.age = 0
    
    @api.depends('last_name', 'first_name', 'middle_name')
    def _compute_name(self):
        for record in self:
            parts = [record.last_name, record.first_name, record.middle_name]
            record.name = ' '.join([p for p in parts if p])

    @api.constrains('phone')
    def _check_phone(self):
        phone_pattern = re.compile(r'^\+?\d{10,15}$')
        for record in self:
            if record.phone and not phone_pattern.match(record.phone):
                raise ValidationError("Телефон повинен бути у форматі +380XXXXXXXXX або 0XXXXXXXXX.")

    @api.constrains('email')
    def _check_email(self):
        email_pattern = re.compile(r'^[\w\.-]+@[\w\.-]+\.\w{2,4}$')
        for record in self:
            if record.email and not email_pattern.match(record.email):
                raise ValidationError("Некоректний формат Email.")

    