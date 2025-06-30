from odoo import models, fields
from odoo.exceptions import ValidationError

class Diagnosis(models.Model):
    _name = 'hr.hospital.medical.diagnosis'
    _description = 'Діагноз'

    visit_id = fields.Many2one(
        comodel_name='hr.hospital.patient.visit',
        string="Візит",
        required=True,
        ondelete='cascade'
    )
    disease_id = fields.Many2one(
        comodel_name='hr.hospital.type.of.disease',
        string="Хвороба",
        required=True
    )
    description = fields.Text(
        string="Опис діагнозу"
    )
    treatment = fields.Html(
        string="Призначене лікування"
    )
    is_approved = fields.Boolean(
        string="Затверджено", 
        default=False
    )
    approved_by_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string="Лікар, що затвердив",
        readonly=True
    )
    approved_date = fields.Datetime(
        string="Дата затвердження", 
        readonly=True
    )
    severity = fields.Selection(
        [
            ('mild', 'Легкий'),
            ('moderate', 'Середній'),
            ('severe', 'Тяжкий'),
            ('critical', 'Критичний')
        ],
        string="Ступінь тяжкості"
    )

    def action_approve(self):
        for rec in self:
            if not rec.is_approved:
                rec.write({
                    'is_approved': True,
                    'approved_by_id': self.env.user.doctor_id.id if hasattr(self.env.user, 'doctor_id') else False,
                    'approved_date': fields.Datetime.now(),
                })
            else:
                raise ValidationError("Діагноз вже затверджено.")