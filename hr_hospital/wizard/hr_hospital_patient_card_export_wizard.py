"""
Wizard for exporting patient cards data.

Provides functionality to export patient card information
in different formats such as CSV or JSON.
"""

import json
import csv
import io
import base64
from odoo import models, fields, api


class PatientCardExportWizard(models.TransientModel):
    """
    Transient wizard model to export patient card data.

    Allows the user to select export format and generates
    the corresponding file with patient card details.
    """

    _name = 'hr.hospital.patient.card.export.wizard'
    _description = 'Patient Card Export Wizard'

    patient_id = fields.Many2one(
        comodel_name='hr.hospital.patient',
        string='Patient',
        required=True
    )
    date_from = fields.Date(
        string='Start date'
    )
    date_to = fields.Date(
        string='End date'
    )

    include_diagnoses = fields.Boolean(
        string='Include diagnoses',
        default=True
    )
    include_recommendations = fields.Boolean(
        string='Include recommendations',
        default=True
    )

    lang_id = fields.Many2one(
        comodel_name='res.lang',
        string='Report language'
    )
    export_format = fields.Selection(
        [
            ('json', 'JSON'),
            ('csv', 'CSV'),
        ],
        string='Export format',
        default='json'
    )

    export_file = fields.Binary(
        string='File',
        readonly=True
    )
    export_filename = fields.Char(
        string='File name',
        readonly=True
    )

    @api.onchange('patient_id')
    def _onchange_patient_lang(self):
        if self.patient_id and self.patient_id.language_id:
            lang = self.env['res.lang'].search(
                [
                    ('code', '=', self.patient_id.language_id.code)
                ],
                limit=1)
            self.lang_id = lang

    def _get_data(self):
        visits = self.env['hr.hospital.patient.visit'].search([
            ('patient_id', '=', self.patient_id.id),
            ('actual_datetime', '>=', self.date_from or '1900-01-01'),
            ('actual_datetime', '<=', self.date_to or '2100-01-01')
        ])

        data = []
        for visit in visits:
            item = {
                'Date': str(visit.actual_datetime),
                'Doctor': visit.doctor_id.name,
            }
            if self.include_diagnoses:
                item['Diagnosis'] = [d.name for d in visit.diagnosis_ids] or []
            if self.include_recommendations:
                item['Recommendations'] = visit.recommendation or ''
            data.append(item)
        return data

    def action_export(self):
        """
        Generate and prepare the export file for the patient card.

        Depending on the selected export format ('json' or 'csv'),
        this method fetches the patient data, formats it accordingly,
        encodes the result to base64, and sets the export
        file and filename fields.

        Returns an action to display the wizard form with
        the generated file ready for download.
        """

        data = self._get_data()
        if self.export_format == 'json':
            file_content = json.dumps(data, ensure_ascii=False, indent=2)
            filename = f"card_{self.patient_id.name.replace(' ', '_')}.json"
        else:  # CSV
            output = io.StringIO()
            if data:
                writer = csv.DictWriter(output, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
            file_content = output.getvalue()
            filename = f"card_{self.patient_id.name.replace(' ', '_')}.csv"

        self.export_file = base64.b64encode(file_content.encode('utf-8'))
        self.export_filename = filename

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'hr.hospital.patient.card.export.wizard',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new',
        }
