"""Wizard for generating disease reports within a specific date range."""

from odoo import models, fields


class DiseaseReportWizard(models.TransientModel):
    """Transient model for creating disease reports by period."""
    _name = 'hr.hospital.disease.report.wizard'
    _description = 'Disease report for the period'

    doctor_ids = fields.Many2many(
        comodel_name='hr.hospital.doctor',
        string='Doctors'
    )
    disease_ids = fields.Many2many(
        comodel_name='hr.hospital.type.of.disease',
        relation='hr_hospital_disease_ids_rel',
        string='Diseases',
    )
    country_ids = fields.Many2many(
        comodel_name='res.country',
        string='Countries'
    )
    date_start = fields.Date(
        string='Start date',
        required=True
    )
    date_end = fields.Date(
        string='End date',
        required=True
    )
    report_type = fields.Selection(
        [
            ('detailed', 'Detailed'),
            ('summary', 'Summary')
        ],
        string='Report type',
        default='detailed'
    )
    group_by = fields.Selection(
        [
            ('doctor', 'Doctor'),
            ('disease', 'Disease'),
            ('month', 'Month'),
            ('country', 'Country')
        ],
        string='Group by',
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
        return self.env.ref('hr_hospital.action_report_disease') \
            .report_action(self, data=report_data)
