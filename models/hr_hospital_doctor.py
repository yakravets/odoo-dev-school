from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date

class Doctor(models.Model):
    _name = 'hr.hospital.doctor'
    _description = 'Лікар'
    _inherit = 'hr.hospital.abstract.person'

    _sql_constraints = [
        ('unique_license_number', 'unique(license_number)', 'Ліцензійний номер має бути унікальним!'),
        ('check_rating_range', 'CHECK(rating >= 0.00 AND rating <= 5.00)', 'Рейтинг має бути від 0.00 до 5.00!'),
    ]

    user_id = fields.Many2one(
        comodel_name='res.users',
        string="Користувач системи"
    )
    specialization_id = fields.Many2one(
        comodel_name='hr.hospital.specialization',
        string='Спеціалізація',
        required=True
    )
    is_intern = fields.Boolean(
        string="Інтерн"
    )
    mentor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string="Лікар-ментор",
        domain="[('is_intern', '=', False)]"
    )
    license_number = fields.Char(
        string="Ліцензійний номер",
        required=True,
        copy=False
    )
    license_issue_date = fields.Date(
        string="Дата видачі ліцензії"
    )
    work_experience = fields.Integer(
        string="Досвід роботи (років)",
        compute='_compute_work_experience',
        store=True
    )
    rating = fields.Float(
        string="Рейтинг",
        digits=(3, 2),
        default=0.0
    )
    schedule_ids = fields.One2many(
        comodel_name='hr.hospital.doctor.schedule',
        inverse_name='doctor_id',
        string="Графік роботи"
    )
    education_country_id = fields.Many2one(
        comodel_name='res.country',
        string="Країна навчання"
    )

    @api.depends('license_issue_date')
    def _compute_work_experience(self):
        today = date.today()
        for rec in self:
            if rec.license_issue_date:
                exp = today.year - rec.license_issue_date.year - (
                    (today.month, today.day) < (rec.license_issue_date.month, rec.license_issue_date.day)
                )
                rec.work_experience = max(0, exp)
            else:
                rec.work_experience = 0

    @api.constrains('mentor_id')
    def _check_mentor_is_not_intern(self):
        for rec in self:
            if rec.mentor_id and rec.mentor_id.is_intern:
                raise ValidationError("Інтерн не може бути лікарем-ментором.")

    @api.constrains('rating')
    def _check_rating(self):
        for record in self:
            if record.rating < 0.0 or record.rating > 5.0:
                raise ValidationError("Рейтинг має бути від 0.00 до 5.00.")
            if record.mentor_id and record.id and record.mentor_id.id == record.id:
                raise ValidationError("Лікар не може бути ментором самому собі.")

    @api.constrains('mentor_id', 'is_intern')
    def _check_mentor(self):
        for record in self:
            if record.is_intern and not record.mentor_id:
                raise ValidationError("Для інтернів обов'язково вказати лікаря-ментора.")
            if not record.is_intern and record.mentor_id:
                raise ValidationError("Лікар-ментор може бути лише у інтернів.")
                
    @api.onchange('is_intern')
    def _onchange_is_intern(self):
        if self.is_intern and not self.mentor_id:
            mentor = self.env['hr.hospital.doctor'].search([('is_intern', '=', False)], limit=1)
            if mentor:
                self.mentor_id = mentor.id

    def name_get(self):
        result = []
        for rec in self:
            name = " ".join(filter(None, [rec.last_name, rec.first_name, rec.middle_name]))
            if rec.speciality_id:
                name = f"{name} ({rec.speciality_id.name})"
            result.append((rec.id, name))
        return result
    