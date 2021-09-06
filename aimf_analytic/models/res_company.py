# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields

class ResCompany(models.Model):
    _inherit = 'res.company'

    invoicing_account_id = fields.Many2one('res.partner.bank', string='Invoicing account id')
    permanent_secretary_id = fields.Many2one('res.partner', string='Signature')
    signature_image = fields.Binary("Image", help="Select image here")