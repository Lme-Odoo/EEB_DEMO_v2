# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, api, fields

class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    analytic_aux_line_ids= fields.One2many('analytic.account.line.aux','analytic_account_line_id', string="Lignes auxiliaires")
    is_different_amount  = fields.Boolean(
        string='Montant différent',
        help='Le montant de la ligne analytique est différent que le montant des lignes auxiliaires.',
        compute='_get_different_amount',
        store=True)
    bailleur_id = fields.Many2one('res.partner', string='Bailleur', related='account_id.partner_id')
    abs_amount = fields.Float(string='Montant Absolu', compute='_get_absolut_amount', store=True)

    def unlink(self):
        for line in self:
            line.analytic_aux_line_ids.write({
                'move_id': line.move_id.id
            })
        super().unlink()

    @api.depends('amount')
    def _get_absolut_amount(self):
        for rec in self:
            rec.abs_amount = abs(rec.amount)

    @api.model
    def create(self, vals):
        res = super(AccountAnalyticLine, self).create(vals)
        existing_aux_line_ids = False
        if vals.get('move_id', False):
            move_line = self.env['account.move.line'].browse(vals.get('move_id'))
            if move_line.exists():
                existing_aux_line_ids = self.env['analytic.account.line.aux'].search([('move_id','=',move_line.id)])

        if existing_aux_line_ids:
            existing_aux_line_ids.write({
                'analytic_account_line_id': res.id,
            })
        else:
            self.env['analytic.account.line.aux'].create(
                {
                    'name': res.name,
                    'analytic_account_line_id': res.id,
                    'invoice_date': res.date,
                    'realisation_date': res.date,
                    'amount': res.amount,
                    'unit_amount': res.unit_amount
                    }
            )
        if res.account_id.group_id:
            res.analytic_aux_line_ids[-1].group_id = res.account_id.group_id
        return res

    @api.depends('amount', 'analytic_aux_line_ids', 'analytic_aux_line_ids.amount')
    def _get_different_amount(self):
        for rec in self:
            total = 0
            for aux_line in rec.analytic_aux_line_ids:
                total += aux_line.amount
            if round(rec.amount, 2) == round(total, 2):
                rec.is_different_amount = False
            else:
                rec.is_different_amount = True
