"""Contact person model for HR Hospital module."""

from odoo import models, fields, _


class ContactPerson(models.Model):
    """Contact model that stores common personal info for patients linking."""

    _name = 'hr.hospital.contact.person'
    _description = 'Contact Person'
    _inherit = 'hr.hospital.abstract.person'

    type = fields.Selection(
        selection=[
            ('husbent/wife', _('Husband/Wife')),
            ('father/mouther', _('Father/Mother')),
            ('relative', _('Relative')),
            ('friend', _('Friend')),
            ('colleague', _('Colleague')),
            ('other', _('Other')),
        ],
        string=_("Type of Contact Person"),
        required=True
    )
    patient_ids = fields.One2many(
        comodel_name='hr.hospital.patient',
        inverse_name='contact_person_ids',
        string=_("Patients"),
    )
