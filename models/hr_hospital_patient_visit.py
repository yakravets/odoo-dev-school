from odoo import models, fields, api

class PatientVisit(models.Model):
    _name = 'hr.hospital.patient.visit'
    _description = 'Візити пацієнтів'

    planned_datetime = fields.Datetime(
        string='Запланована дата',
        required=True
    )
    visited_datetime = fields.Datetime(
        string='Дата візиту',
    )
    status = fields.Selection(
        [
            ('planned', 'Заплановано'),
            ('in_process', 'В процесі'),
            ('success', 'Завершено'),
            ('canceled', 'Скасовано'),
        ],
        string='Статус',
        required=True,
        default='planned'
    )
    patient_id = fields.Many2one(
        comodel='hr.hospital.patient',
        string='Пацієнт',
        required=True,
        on_delete='restrict',
    )
    doctor_id = fields.Many2one(
        comodel='hr.hospital.doctor',
        string='Лікар',
        required=True,
        on_delete='restrict',
    )
    note = fields.Html(
        string="Скарги пацієнта"
    )
    type_of_disease_id = fields.Many2one(
        comodel='hr.hospital.type.of.disease',
        string='Діагноз',
        on_delete='restrict',
    )
    recommendation = fields.Html(
        string="Рекомендації"
    )