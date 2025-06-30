from odoo import models, fields, api
from odoo.exceptions import ValidationError

class PatientVisit(models.Model):
    _name = 'hr.hospital.patient.visit'
    _description = 'Візити пацієнтів'

    planned_datetime = fields.Datetime(
        string='Запланована дата/час',
        required=True
    )
    actual_datetime = fields.Datetime(
        string="Фактичні дата та час візиту",
        readonly=True
    )
    status = fields.Selection(
        [
            ('planned', 'Заплановано'),
            ('done', 'Завершено'),
            ('cancelled', 'Скасовано'),
            ('no_show', 'Не з\'явився'),
        ],
        string='Статус',
        required=True,
        default='planned'
    )
    patient_id = fields.Many2one(
        comodel_name='hr.hospital.patient',
        string='Пацієнт',
        required=True
    )
    doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string='Лікар',
        required=True,
        ondelete='restrict'
    )
    visit_type = fields.Selection(
        [
            ('primary', 'Первинний'),
            ('repeat', 'Повторний'),
            ('preventive', 'Профілактичний'),
            ('emergency', 'Невідкладний'),
        ],
        string="Тип візиту"
    )
    diagnosis_ids = fields.One2many(
        comodel_name='hr.hospital.medical.diagnosis',
        inverse_name='visit_id',
        string="Діагнози"
    )
    recommendation = fields.Html(
        string="Рекомендації"
    )
    amount = fields.Monetary(
        string="Вартість візиту", 
        currency_field='currency_id'
    )
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string="Валюта"
    )

    diagnosis_count = fields.Integer(
        string="Кількість діагнозів",
        compute='_compute_diagnosis_count',
        store=True
    )

    @api.depends('diagnosis_ids')
    def _compute_diagnosis_count(self):
        for rec in self:
            rec.diagnosis_count = len(rec.diagnosis_ids)

    @api.constrains('doctor_id', 'patient_id', 'planned_datetime')
    def _check_unique_patient_doctor_per_day(self):
        for rec in self:
            if rec.doctor_id and rec.patient_id and rec.planned_datetime:
                domain = [
                    ('id', '!=', rec.id),
                    ('doctor_id', '=', rec.doctor_id.id),
                    ('patient_id', '=', rec.patient_id.id),
                    ('planned_datetime', '>=', rec.planned_datetime.replace(hour=0, minute=0, second=0)),
                    ('planned_datetime', '<', rec.planned_datetime.replace(hour=23, minute=59, second=59)),
                ]
                count = self.search_count(domain)
                if count > 0:
                    raise ValidationError("Пацієнт не може бути записаний до одного лікаря більше одного разу на день.")

    @api.onchange('patient_id')
    def _onchange_patient_id(self):
        if self.patient_id and self.patient_id.allergies:
            return {
                'warning': {
                    'title': "Увага: алергії пацієнта",
                    'message': f"У пацієнта вказано алергії: {self.patient_id.allergies}"
                }
            }

    def unlink(self):
        for rec in self:
            if rec.diagnosis_ids:
                raise ValidationError("Не можна видалити візит, для якого існують діагнози.")
        return super().unlink()