from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class AnalyticCostItemUom(models.Model):
    _name = 'analytic.cost.item.uom'
    _description = "Cost Item Unit of measure"

    name = fields.Char(string='Nom')


class AnalyticCostItem(models.Model):
    _name = 'analytic.cost.item'
    _description = "Cost Item"

    description = fields.Char(string='Description')
    sequence = fields.Integer( string='Sequence', required=True)
    name = fields.Char(string='Nom', compute= '_get_name_and_level', store= True)
    group_id = fields.Many2one('account.analytic.group', string='Groupe de comptes analytiques',required=True)
    parent_id = fields.Many2one('analytic.cost.item', string='Poste de coût parent')
    child_ids = fields.One2many('analytic.cost.item','parent_id', string='Postes de coût enfants', readonly=True)
    analytic_aux_ids = fields.One2many('analytic.account.line.aux','analytic_cost_item_id', string='Lignes auxiliaires')
    currency_id = fields.Many2one('res.currency', string='Devise', default=lambda self: self.env.company.currency_id.id)
    dotation = fields.Monetary(string='Dotation', compute='_compute_dotation', inverse='_set_dotation', store=True)
    total_dotation = fields.Monetary(string='Total dotation', compute= '_get_total_dotation', store= True)
    linked_spend = fields.Monetary(string='Total des dépenses liées', compute= '_get_total_linked_spend', store= True)
    spend = fields.Monetary(string='Total des dépenses', compute= '_get_total_spend', store= True)
    amount = fields.Monetary(string='Solde', compute= '_get_balance', store= True)
    total_amount = fields.Monetary(string='Solde total', compute= '_get_total_balance', store= True)
    prefix = fields.Char(string='Prefix', compute= '_get_prefix', store= True)
    level = fields.Integer(string='Level', compute= '_get_name_and_level', store= True)
    position = fields.Integer(string='Position', compute= '_get_position', store= True)
    reference = fields.Char(string='Ref', compute= '_get_reference', store= True)
    is_cost_item = fields.Boolean(string="Est un groupe de poste de coût", default=False, store=True)
    uom = fields.Many2one('analytic.cost.item.uom', string='Unités')
    uom_number = fields.Integer(string="Nombre d'unités", default=1)
    unit_dotation = fields.Monetary(string='Coût unitaire',default=0)
    total_unit_spend = fields.Float(string='Quantité totale dépensée', compute='_compute_total_unit_spend')

    @api.depends('analytic_aux_ids', 'analytic_aux_ids.unit_amount')
    def _compute_total_unit_spend(self):
        for rec in self:
            rec.total_unit_spend = sum(rec.analytic_aux_ids.mapped('unit_amount'))

    @api.depends('unit_dotation', 'uom_number')
    def _compute_dotation(self):
        for rec in self:
            rec.dotation = rec.unit_dotation * rec.uom_number

    @api.onchange('uom_number', 'dotation')
    def _set_dotation(self):
        for rec in self:
            rec.unit_dotation = rec.dotation/rec.uom_number

    @api.depends('name', 'parent_id.name')
    def _get_reference(self):
        for rec in self:
            if rec.parent_id:
                rec.reference = rec.parent_id.reference
            else:
                rec.reference = self.env['ir.sequence'].next_by_code('analytic.cost.item')

    @api.onchange('parent_id')
    def _show_parent_id(self):
        if self.parent_id:
            self.group_id = self.parent_id.group_id

    @api.onchange('group_id')
    def _show_group_id(self):
        if self.group_id:
            self.parent_id = None
            return {'domain':
            {'parent_id': [('group_id', '=', self.group_id.id),('is_cost_item','=', True)]}
            } 
        else:
            return {'domain':
            {'parent_id': []}
            }       

    @api.depends('sequence', 'parent_id.prefix')
    def _get_prefix(self):
        for rec in self:
            if not rec.parent_id:
                rec.prefix = str(rec.sequence)
            else:
                rec.prefix = rec.parent_id.prefix + '.' + str(rec.sequence)

    @api.depends('parent_id', 'level', 'prefix')
    def _get_position(self):
        for rec in self:
            elements = rec.prefix.split('.')
            position = ""
            for e in elements:
                if int(e) < 10:
                    position += "0" + str(int(e))
                else:
                    position += e
            rec.position = int(position.ljust(9, '0'))

    @api.depends('parent_id', 'level', 'description', 'prefix', 'parent_id.name')
    def _get_name_and_level(self):
        for rec in self:
            if rec.parent_id:
                rec.level = rec.parent_id.level + 1
            rec.name = rec.level * "--" + str(rec.prefix) + " " + str(rec.description)

    @api.constrains('sequence', 'parent_id')
    def _check_sequence(self):
        for rec in self:
            if rec.parent_id:
                if rec.sequence in rec.parent_id.child_ids.filtered(lambda child: child != rec).mapped('sequence'):
                    raise ValidationError(_('The prefix number %s is already in use in the parent %s') % (rec.prefix, rec.parent_id.name))

    @api.depends('linked_spend', 'analytic_aux_ids.amount', 'child_ids.linked_spend', 'child_ids.total_amount', 'child_ids.amount')
    def _get_total_linked_spend(self):
        for rec in self:
            if not rec.is_cost_item:
                total = 0
                rec.linked_spend = 0
                for aux in rec.analytic_aux_ids:
                    total += aux.amount
                rec.linked_spend = -total
            else:
                total = 0
                rec.linked_spend = -total
                return rec.linked_spend

    @api.depends('spend', 'child_ids', 'child_ids.spend','child_ids.linked_spend', 'child_ids.total_amount', 'analytic_aux_ids.amount')
    def _get_total_spend(self):
        for rec in self:
            if not rec.is_cost_item:
                rec.spend = 0
            else:
                total = 0
                for child in rec.child_ids:
                    total += child.linked_spend + child.spend
                rec.spend = total 

    @api.depends('linked_spend', 'dotation', 'child_ids', 'child_ids.amount', 'child_ids.dotation', 'child_ids.total_amount')
    def _get_balance(self):
        for rec in self:
            if not rec.is_cost_item:
                rec.amount = rec.dotation - rec.linked_spend
            else:
                rec.amount = 0


    @api.depends('child_ids','amount', 'dotation', 'child_ids.amount', 'child_ids.dotation', 'total_amount', 'child_ids.total_amount')
    def _get_total_balance(self):
        for rec in self:
            if not rec.is_cost_item:
                rec.total_amount = 0
            else:
                total = 0
                for child in rec.child_ids:
                    total += child.amount + child.total_amount
                rec.total_amount = total

    @api.depends('child_ids','dotation', 'child_ids.total_dotation', 'child_ids.dotation')
    def _get_total_dotation(self):
        for rec in self:
            if not rec.is_cost_item:
                rec.total_dotation = 0
            else:
                total = 0
                for child in rec.child_ids:
                    total += child.dotation + child.total_dotation
                rec.total_dotation = total
