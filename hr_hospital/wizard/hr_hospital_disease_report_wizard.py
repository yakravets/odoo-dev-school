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
        string='Хвороби',
        relation='hr_hospital_disease_ids_rel'
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

    def action_report(self):
        self.ensure_one()
        report_data = {
            'doctor_ids': self.doctor_ids.ids,
            'disease_ids': self.disease_ids.ids,
            'country_ids': self.country_ids.ids,
            'date_start': self.date_start,
            'date_end': self.date_end,
            'report_type': self.report_type,
            'group_by': self.group_by
        }
        return self.env.ref('hr_hospital.action_report_disease').report_action(self, data=report_data)