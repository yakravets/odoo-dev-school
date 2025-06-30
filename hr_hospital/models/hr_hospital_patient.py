from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date

class Patient(models.Model):
    _name = 'hr.hospital.patient'
    _description = _('Patient')
    _inherit = 'hr.hospital.abstract.person'

    personal_doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string=_("Personal doctor")
    )
    passport_data = fields.Char(
        string=_("Passport data"),
        size=10
    )    
    blood_group = fields.Selection(
        [
            ('o_pos', 'O(I) Rh+'),
            ('o_neg', 'O(I) Rh-'),
            ('a_pos', 'A(II) Rh+'),
            ('a_neg', 'A(II) Rh-'),
            ('b_pos', 'B(III) Rh+'),
            ('b_neg', 'B(III) Rh-'),
            ('ab_pos', 'AB(IV) Rh+'),
            ('ab_neg', 'AB(IV) Rh-'),
        ],
        string=_("Blood type/Rh factor"),
    )
    allergies = fields.Text(
        string=_("Allergies")
    )
    insurance_company_id = fields.Many2one(
        comodel_name='res.partner',
        string=_("Insurance company"),
        domain=[('is_company', '=', True)]
    )
    insurance_policy_number = fields.Char(
        string=_("Insurance policy number")
    )

    contact_person_ids = fields.Many2many(
        comodel_name='hr.hospital.contact.person',
        relation='hr_hospital_contact_person_patient_rel',
        column1='patient_id',
        column2='contact_person_id',
        string=_("Contact persons"),
    )
    doctor_history_ids = fields.One2many(
        comodel_name='hr.hospital.patient.doctor.history',
        inverse_name='patient_id',
        string=_("The history of personal doctors")
    )

    @api.constrains('birth_date')
    def _check_age_positive(self):
        for rec in self:
            if rec.birth_date:
                today = date.today()
                if rec.birth_date >= today:
                    raise ValidationError(_("The date of birth must be in the past."))
                age = today.year - rec.birth_date.year - ((today.month, today.day) < (rec.birth_date.month, rec.birth_date.day))
                if age < 0:
                    raise ValidationError(_("The patient's age must be greater than 0."))

    @api.model_create_multi
    def create(self, vals_list):
        patients = super().create(vals_list)
        for rec, vals in zip(patients, vals_list):
            if 'personal_doctor_id' in vals and vals['personal_doctor_id']:
                rec._create_doctor_history(vals['personal_doctor_id'])
        return patients

    def write(self, vals):
        res = super().write(vals)
        for rec in self:
            if 'personal_doctor_id' in vals and vals['personal_doctor_id']:
                rec._create_doctor_history(vals['personal_doctor_id'])
        return res

    def _create_doctor_history(self, doctor_id):
        self.env['hr.hospital.patient.doctor.history'].create({
            'patient_id': self.id,
            'doctor_id': doctor_id,
            'assign_date': fields.Date.context_today(self),
            'active': True,
        })

    @api.onchange('citizenship_country_id')
    def _onchange_citizenship_country_id(self):
        if self.citizenship_country_id:
            suggested_lang = self._get_suggested_language_from_country(self.citizenship_country_id)
            if suggested_lang:
                return {
                    'warning': {
                        'title': _("Language of communication"),
                        'message': _("Recommended language for this country:") + suggested_lang.name
                    },
                    'value': {
                        'communication_language_id': suggested_lang.id
                    }
                }

    def _get_suggested_language_from_country(self, country):
        mapping = {
            'UA': 'uk_UA',
            'PL': 'pl_PL',
            'RU': 'ru_RU',
            'US': 'en_US',
        }
        code = country.code
        lang_code = mapping.get(code)
        if lang_code:
            return self.env['res.lang'].search([('code', '=', lang_code)], limit=1)
        return False
    