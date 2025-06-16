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
        comodel_name='hr.hospital.patient',
        string='Пацієнт',
        required=True
    )
    doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string='Лікар',
        required=True,
    )
    note = fields.Html(
        string="Скарги пацієнта"
    )
    type_of_disease_id = fields.Many2one(
        comodel_name='hr.hospital.type.of.disease',
        string='Діагноз',
    )
    recommendation = fields.Html(
        string="Рекомендації"
    )