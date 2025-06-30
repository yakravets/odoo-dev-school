from odoo import models, fields, _

class TypeOfDisease(models.Model):
    _name = 'hr.hospital.type.of.disease'
    _description = _('Disease')

    name = fields.Char(
        string=_('Name'),
        required=True
    )
    active = fields.Boolean(
        string=_('Active'),
        default=True
    )
    parent_id = fields.Many2one(
        comodel_name='hr.hospital.type.of.disease',
        string=_("Parent"),
        ondelete='set null'
    )
    child_ids = fields.One2many(
        comodel_name='hr.hospital.type.of.disease',
        inverse_name='parent_id',
        string=_("Related diseases")
    )
    severity = fields.Selection(
        selection=[
            ('mild', _('Mild')),
            ('moderate', _('Moderate')),
            ('severe', _('Severe')),
            ('critical', _('Critical')),
        ],
        string=_('Severity'),
        required=True
    )
    icd10_code = fields.Char(
        string=_("ICD-10 code"), 
        size=10
    )
    danger_level = fields.Selection(
        [
            ('low', _('Low')),
            ('medium', _('Medium')),
            ('high', _('High')),
            ('critical', _('Critical')),
        ],
        string=_("Danger level")
    )
    is_contagious = fields.Boolean(
        string=_("Contagious")
    )
    symptoms = fields.Text(
        string=_("Symptoms")
    )
    region_ids = fields.Many2many(
        comodel_name='res.country',
        relation='hr_hospital_type_of_disease_country_rel',
        column1='disease_id',
        column2='country_id',
        string=_("Distribution regions")
    )
    