from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import timedelta

class Diagnosis(models.Model):
    _name = 'hr.hospital.medical.diagnosis'
    _description = _('Diagnosis')

    name = fields.Char(
        string=_("Name"), 
        required=True, 
        copy=False, 
        readonly=True, 
        default=lambda self: _('New')
    )

    visit_id = fields.Many2one(
        comodel_name='hr.hospital.patient.visit',
        string=_("Visit"),
        required=True,
        ondelete='cascade',
        domain=lambda self: [
            ('state', '=', 'done'),
            ('visit_date', '>=', (fields.Date.today() - timedelta(days=30)).strftime('%Y-%m-%d'))
        ]
    )
    disease_id = fields.Many2one(
        comodel_name='hr.hospital.type.of.disease',
        string=_("Disease"),
        required=True,
        domain="[('is_contagious', '=', True), ('danger_level', 'in', ['high', 'critical'])]"
    )
    description = fields.Text(
        string=_("Description of diagnosis")
    )
    treatment = fields.Html(
        string=_("Prescribed treatment")
    )
    is_approved = fields.Boolean(
        string=_("Approved"), 
        default=False
    )
    approved_by_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string=_("The doctor who approved"),
        readonly=True
    )
    approved_date = fields.Datetime(
        string=_("Approval date"), 
        readonly=True
    )
    severity = fields.Selection(
        [
            ('mild', _('Mild')),
            ('moderate', _('Moderate')),
            ('severe', _('Severe')),
            ('critical', _('Critical')),
        ],
        string=_("Severity")
    )
    diagnosis_unit = fields.Integer(
        string=_("Visit Unit"), 
        default=1
    )

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('hr.hospital.medical.diagnosis') or _('New')
        return super(Diagnosis, self).create(vals)

    def action_approve(self):
        for rec in self:
            if not rec.is_approved:
                rec.write({
                    'is_approved': True,
                    'approved_by_id': self.env.user.doctor_id.id if hasattr(self.env.user, 'doctor_id') else False,
                    'approved_date': fields.Datetime.now(),
                })
            else:
                raise ValidationError(_("The diagnosis has already been confirmed."))