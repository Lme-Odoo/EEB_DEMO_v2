from odoo import models, fields, api, _


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    parent_group_id = fields.Many2one('account.analytic.group', compute='_compute_parent_group', string="Groupe parent", store=True)
    partner_id = fields.Many2one('res.partner', string='Bailleur', auto_join=True, tracking=True, check_company=True)
    programation_id = fields.Many2one('aimf.programation', string='Programmation')
    
    @api.depends('group_id', 'group_id.parent_id')
    def _compute_parent_group(self):
        for rec in self:
            rec.parent_group_id = self._get_top_parent_group(rec.group_id)
    
    def _get_top_parent_group(self, group):
        if group.parent_id:
            return self._get_top_parent_group(group.parent_id)
        else:
            return group

    def button_reassign(self):
        vals = {
            'source_project_id': self.id,
            'balance': float(self.balance),
        }
        view = self.env.ref('aimf_analytic.view_account_analytic_reassignment_form')
        wiz = self.env['account.analytic.reassignment'].create(vals)
        return {
            'name': _('Réaffectation'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'account.analytic.reassignment',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'res_id': wiz.id,
            'context': self.env.context,
        }
