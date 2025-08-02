"""Contact person model for HR Hospital module."""

from odoo import models, fields


class ContactPerson(models.Model):
    """Contact model that stores common personal info for patients linking."""

    _name = 'hr.hospital.contact.person'
    _description = 'Contact Person'
    _inherit = 'hr.hospital.abstract.person'

    type = fields.Selection(
        selection=[
            ('husbent/wife', 'Husband/Wife'),
            ('father/mouther', 'Father/Mother'),
            ('relative', 'Relative'),
            ('friend', 'Friend'),
            ('colleague', 'Colleague'),
            ('other', 'Other'),
        ],
        string="Type of Contact Person",
        required=True
    )
    patient_ids = fields.One2many(
        comodel_name='hr.hospital.patient',
        inverse_name='contact_person_ids',
        string="Patients",
    )
