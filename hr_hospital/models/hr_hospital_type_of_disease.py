"""Defines the model for types of diseases used in the hospital system."""

from odoo import models, fields


class TypeOfDisease(models.Model):
    """Represents a type or category of disease."""

    _name = 'hr.hospital.type.of.disease'
    _description = 'Disease'

    name = fields.Char(
        required=True,
        translate=True
    )
    active = fields.Boolean(
        default=True
    )
    parent_id = fields.Many2one(
        comodel_name='hr.hospital.type.of.disease',
        string="Parent",
        ondelete='set null'
    )
    child_ids = fields.One2many(
        comodel_name='hr.hospital.type.of.disease',
        inverse_name='parent_id',
        string="Related diseases"
    )
    severity = fields.Selection(
        selection=[
            ('mild', 'Mild'),
            ('moderate', 'Moderate'),
            ('severe', 'Severe'),
            ('critical', 'Critical'),
        ],
        required=True
    )
    icd10_code = fields.Char(
        string="ICD-10 code",
        size=10
    )
    danger_level = fields.Selection(
        [
            ('low', 'Low'),
            ('medium', 'Medium'),
            ('high', 'High'),
            ('critical', 'Critical'),
        ],
        string="Danger level"
    )
    is_contagious = fields.Boolean(
        string="Contagious"
    )
    symptoms = fields.Text(
        translate=True
    )
    region_ids = fields.Many2many(
        comodel_name='res.country',
        relation='hr_hospital_type_of_disease_country_rel',
        column1='disease_id',
        column2='country_id',
        string="Distribution regions"
    )
