# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, api, fields

class AccountAnalyticGroup(models.Model):
    _inherit = 'account.analytic.group'

    analytic_aux_line_ids= fields.One2many('analytic.account.line.aux','group_id', string="Lignes auxiliaires")
    analytic_cost_item_ids= fields.One2many('analytic.cost.item','group_id', string="Postes de couts")
    get_all_aux_lines = fields.Integer( string='Line auxiliaire', compute='_compute_get_all_aux_lines')
    get_all_cost_items = fields.Integer(string='Poste de cout', compute='_compute_get_all_cost_items')
    beneficiary_city_id = fields.Many2one('res.partner', string='Ville bénéficiaire')
    manager_id = fields.Many2one('hr.employee', string='Gestionnaire')
    status_id = fields.Many2one('aimf.status', string='Statut')


    def get_aux_lines(self):
        return {
            'name': 'Analytic account line aux tree',
            'view_type': 'form',
            'view_mode': 'tree,form',  
            'res_model': 'analytic.account.line.aux',
            'domain':[('id', 'in', self.analytic_aux_line_ids.ids)],
            'type': 'ir.actions.act_window',
            'target': 'current',
        }

    def get_cost_items(self):
        return {
            'name': 'cost item tree',
            'view_type': 'form',
            'view_mode': 'tree,form',  
            'res_model': 'analytic.cost.item',
            'domain':[('id', 'in', self.analytic_cost_item_ids.ids)],
            'type': 'ir.actions.act_window',
            'target': 'current',
        }


    def _compute_get_all_aux_lines(self):
        for rec in self:
            rec.get_all_aux_lines = len(rec.analytic_aux_line_ids)

    def _compute_get_all_cost_items(self):
        for rec in self:
            rec.get_all_cost_items = len(rec.analytic_cost_item_ids)