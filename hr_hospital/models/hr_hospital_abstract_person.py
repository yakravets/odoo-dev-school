"""Abstract person model for HR Hospital module."""

import re
from datetime import date

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class AbstractPerson(models.AbstractModel):
    """Abstract model that stores common personal info for patients/doctors."""

    _name = 'hr.hospital.abstract.person'
    _description = 'Abstract Person Model'
    _inherit = ['image.mixin']
    _abstract = True

    first_name = fields.Char(
        string='First name',
        required=True
    )
    last_name = fields.Char(
        string='Last name',
        required=True
    )
    middle_name = fields.Char(
        string='Middle name',
    )
    name = fields.Char(
        string='Full Name',
        compute='_compute_name',
        readonly=True,
        store=True
    )
    active = fields.Boolean(
        default=True
    )
    phone = fields.Char(
        string='Phone number',
        required=True
    )
    email = fields.Char()
    gender = fields.Selection(
        [
            ('unknown', 'Unknown'),
            ('man', 'Man'),
            ('woman', 'Woman'),
        ],
        required=True,
        default='unknown'
    )
    birth_date = fields.Date(
        string='Birth date',
        required=True
    )
    age = fields.Integer(
        compute='_compute_age',
        readonly=True,
        store=True
    )
    citizenship_country_id = fields.Many2one(
        comodel_name='res.country',
        string='Citizenship country'
    )
    language_id = fields.Many2one(
        comodel_name='res.lang',
        string='Language',
    )

    @api.depends('birth_date')
    def _compute_age(self):
        today = date.today()
        for record in self:
            if record.birth_date:
                born = record.birth_date
                age = _compute_age(born, today)
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
                raise ValidationError(
                    _("Phone number must be in format "
                        "+380XXXXXXXXX.")
                )

    @api.constrains('email')
    def _check_email(self):
        email_pattern = re.compile(r'^[\w\.-]+@[\w\.-]+\.\w{2,4}$')
        for record in self:
            if record.email and not email_pattern.match(record.email):
                raise ValidationError(
                    _("Incorrect Email.")
                )


def _compute_age(born, today):
    return today.year - born.year - (
        (today.month, today.day) < (born.month, born.day)
    )
