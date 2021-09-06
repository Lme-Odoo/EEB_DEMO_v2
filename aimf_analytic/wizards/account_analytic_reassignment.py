from odoo import models, fields, _
from odoo.exceptions import UserError
from odoo.tools import float_is_zero


class AccountAnalyticReassigment(models.TransientModel):
    _name = 'account.analytic.reassignment'
    _description = 'Analytic account reassignment wizard'

    source_project_id = fields.Many2one('account.analytic.account', string='Projet source', readonly=True)
    source_project_parent_id = fields.Many2one(related='source_project_id.parent_group_id', string="Groupe parent")
    source_partner_id = fields.Many2one(related='source_project_id.partner_id', string="Client")
    balance = fields.Float(string='Solde projet source', readonly=True)
    balance_to_reassign = fields.Float(string='Montant à réaffecter')
    destination_project_id = fields.Many2one('account.analytic.account', string='Projet destination')

    def button_confirm(self):
        if self.balance_to_reassign > self.balance:
            raise UserError(_('Le montant à réaffecter doit être inférieur ou égal au solde du projet source'))
        elif float_is_zero(self.balance_to_reassign, precision_rounding=3):
            raise UserError(_('Le montant à réaffecter doit être supérieur à zéro'))
        elif not self.destination_project_id:
            raise UserError(_('Veuillez indiquer un projet de destination'))

        ref = self.env['ir.sequence'].next_by_code('analytic.account.reassignment.reference.sequence')
        debit_vals = {
            'name': 'Réaffectation vers %s' %(self.destination_project_id.name),
            'account_id': self.source_project_id.id,
            'tag_ids': [(4, self.env.ref('aimf_analytic.reassignment_tag').id, 0)],
            'ref': ref,
            'amount': self.balance_to_reassign*-1
        }
        self.env['account.analytic.line'].create(debit_vals)

        credit_vals = {
            'name': 'Réaffectation provenant de %s' %(self.source_project_id.name),
            'account_id': self.destination_project_id.id,
            'tag_ids': [(4, self.env.ref('aimf_analytic.reassignment_tag').id, 0)],
            'ref': ref,
            'amount': self.balance_to_reassign
        }
        self.env['account.analytic.line'].create(credit_vals)
