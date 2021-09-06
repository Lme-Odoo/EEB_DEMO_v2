from odoo import models, fields, api, _
from odoo.exceptions import UserError


class AnalyticAccountLineAux(models.Model):
    _name = 'analytic.account.line.aux'
    _description = "Account line aux"

    name = fields.Char(string='Description', required=True)
    analytic_cost_item_id = fields.Many2one('analytic.cost.item', string='Poste de coût')
    currency_id = fields.Many2one('res.currency', string='Devise', default=lambda self: self.env.company.currency_id.id)
    amount = fields.Monetary(string='Montant')
    absolute_value_amount = fields.Float(string='Valeur absolue du montant', compute='_get_absolute_value_amount')
    invoice_date = fields.Date(string='Date de facture')
    result = fields.Many2one('analytic.account.line.aux.result', string='Résultats')
    state = fields.Selection([('validated', 'Validé'), ('not_validated', 'Pas validé')], default='not_validated', string='Status')
    analytic_account_line_id = fields.Many2one('account.analytic.line')
    group_id = fields.Many2one('account.analytic.group', related='analytic_account_line_id.group_id', store = True, string='Projet')
    unit_amount = fields.Float('Quantité', readonly=False, store=True)
    realisation_date = fields.Date(string='Date de réalisation')
    bailleur_id = fields.Many2one('res.partner', string='Bailleur', related='analytic_account_line_id.bailleur_id')
    ref_number = fields.Char(string='Numéro de référence')
    move_id = fields.Many2one('account.move.line', string='Ligne de facture')

    def write(self, vals):
        super().write(vals)
        for rec in self:
            if rec.analytic_cost_item_id and rec.group_id != rec.analytic_cost_item_id.group_id:
                raise UserError(_("Le poste de coût choisi n'est pas compatible avec une ou plusieurs écriture(s) auxiliaire(s) sélectionnée(s) car il ne s'agit pas du même projet"))

    def _get_absolute_value_amount(self):
        for rec in self:
            rec.absolute_value_amount = abs(rec.amount)

    def _get_analytic_account_line_id(self):
        for rec in self:
            rec.analytic_account_line_id = rec.analytic_account_line_id

