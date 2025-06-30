from odoo import models, fields

class ContactPerson(models.Model):
    _name = 'hr.hospital.contact.person'
    _description = 'Пацієнт'
    _inherit = 'hr.hospital.abstract.person'

    type = fields.Selection(
        selection=[
            ('husbent/wife', 'Чоловік/Дружина'),
            ('father/mouther', 'Батько/Мати'),
            ('relative', 'Родич'),
            ('friend', 'Друг'),
            ('colleague', 'Колега'),
            ('other', 'Інше')
        ],
        string="Тип контактної особи",
        required=True
    )
    patient_ids = fields.One2many(
        comodel_name='hr.hospital.patient',
        inverse_name='contact_person_ids',
        string="Пацієнти",
    )