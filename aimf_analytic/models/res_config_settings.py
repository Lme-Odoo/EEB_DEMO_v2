# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import _, api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    
    invoicing_account_id = fields.Many2one('res.partner.bank', string='Invoicing account id')
    permanent_secretary_id = fields.Many2one('res.partner', string='Signature')
    signature_image = fields.Binary("Image", help="Select image here")


    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update({
        'invoicing_account_id': int(self.env['ir.config_parameter'].sudo().get_param('aimf_analytic.invoicing_account_id')),
        'permanent_secretary_id': int(self.env['ir.config_parameter'].sudo().get_param('aimf_analytic.permanent_secretary_id')),
        'signature_image': self.env['ir.config_parameter'].sudo().get_param('aimf_analytic.signature_image'),
        })
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        company = self.company_id or self.env.user.company_id
        self.env['ir.config_parameter'].sudo().set_param('aimf_analytic.invoicing_account_id', self.invoicing_account_id.id)
        self.env['ir.config_parameter'].sudo().set_param('aimf_analytic.permanent_secretary_id', self.permanent_secretary_id.id)
        self.env['ir.config_parameter'].sudo().set_param('aimf_analytic.signature_image', self.signature_image)
        company.signature_image = self.signature_image
        company.permanent_secretary_id = self.permanent_secretary_id.id
        company.invoicing_account_id = self.invoicing_account_id.id
