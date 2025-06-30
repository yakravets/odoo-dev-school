from odoo import models, fields

class DiseaseReportWizard(models.TransientModel):
    _name = 'hr.hospital.disease.report.wizard'
    _description = 'Звіт по хворобах за період'

    doctor_ids = fields.Many2many(
        comodel_name='hr.hospital.doctor',
        string='Лікарі'
    )
    disease_ids = fields.Many2many(
        comodel_name='hr.hospital.type.of.disease',
        string='Хвороби'
    )
    country_ids = fields.Many2many(
        comodel_name='res.country',
        string='Країни'
    )
    date_start = fields.Date(
        string='Дата початку',
        required=True
    )
    date_end = fields.Date(
        string='Дата закінчення',
        required=True
    )
    report_type = fields.Selection(
        [('detailed', 'Детальний'), ('summary', 'Підсумковий')],
        string='Тип звіту',
        default='detailed'
    )
    group_by = fields.Selection(
        [
            ('doctor', 'Лікар'),
            ('disease', 'Хвороба'),
            ('month', 'Місяць'),
            ('country', 'Країна')
        ],
        string='Групувати за',
        required=True
    )