"""
Defines the model for medical specializations
used in the hospital system.
"""

from odoo import models, fields, _


class Specialization(models.Model):
    """Represents a medical specialization (e.g. cardiology, neurology)."""

    _name = 'hr.hospital.specialization'
    _description = _('Specializations')

    name = fields.Char(
        string=_('Name'),
        required=True
    )
    active = fields.Boolean(
        string=_('Active'),
        default=True
    )
    code = fields.Char(
        string=_("Specialty code"),
        size=10,
        required=True
    )
    description = fields.Text(
        string=_("Description")
    )
    doctor_ids = fields.One2many(
        comodel_name='hr.hospital.doctor',
        inverse_name='specialization_id',
        string=_("Doctors")
    )
