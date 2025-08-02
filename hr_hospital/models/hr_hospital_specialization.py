"""
Defines the model for medical specializations
used in the hospital system.
"""

from odoo import models, fields


class Specialization(models.Model):
    """Represents a medical specialization (e.g. cardiology, neurology)."""

    _name = 'hr.hospital.specialization'
    _description = 'Specializations'

    name = fields.Char(
        required=True
    )
    active = fields.Boolean(
        default=True
    )
    code = fields.Char(
        string="Specialty code",
        size=10,
        required=True
    )
    description = fields.Text()
    doctor_ids = fields.One2many(
        comodel_name='hr.hospital.doctor',
        inverse_name='specialization_id',
        string="Doctors"
    )
