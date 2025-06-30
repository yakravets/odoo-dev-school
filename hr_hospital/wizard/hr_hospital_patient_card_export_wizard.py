from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime
import json
import csv
import io
import base64

class PatientCardExportWizard(models.TransientModel):
    _name = 'hr.hospital.patient.card.export.wizard'
    _description = _('Patient Card Export Wizard')

    patient_id = fields.Many2one(
        'hr.hospital.patient', 
        string=_('Patient'), 
        required=True
    )
    date_from = fields.Date(
        string=_('Start date')
    )
    date_to = fields.Date(
        string=_('End date')
    )

    include_diagnoses = fields.Boolean(
        string=_('Include diagnoses'), 
        default=True
    )
    include_recommendations = fields.Boolean(
        string=_('Include recommendations'), 
        default=True
    )

    lang_id = fields.Many2one(
        'res.lang', 
        string=_('Report language')
    )
    export_format = fields.Selection(
        [
            ('json', 'JSON'),
            ('csv', 'CSV'),
        ], 
        string=_('Export format'), 
        default='json'
    )

    export_file = fields.Binary(
        string=_('File'), 
        readonly=True
    )
    export_filename = fields.Char(
        string=_('File name'), 
        readonly=True
    )

    @api.onchange('patient_id')
    def _onchange_patient_lang(self):
        if self.patient_id and self.patient_id.lang:
            lang = self.env['res.lang'].search([('code', '=', self.patient_id.lang)], limit=1)
            self.lang_id = lang

    def _get_data(self):
        visits = self.env['hr.hospital.patient.visit'].search([
            ('patient_id', '=', self.patient_id.id),
            ('date', '>=', self.date_from or '1900-01-01'),
            ('date', '<=', self.date_to or '2100-01-01')
        ])

        data = []
        for visit in visits:
            item = {
                _('Date'): str(visit.date),
                _('Doctor'): visit.doctor_id.name,
            }
            if self.include_diagnoses:
                item[_('Diagnosis')] = visit.diagnosis or ''
            if self.include_recommendations:
                item[_('Recommendations')] = visit.recommendation or ''
            data.append(item)
        return data

    def action_export(self):
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
            'res_model': 'patient.card.export.wizard',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new',
        }
