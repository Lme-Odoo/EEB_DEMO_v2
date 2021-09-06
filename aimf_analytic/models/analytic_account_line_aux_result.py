from odoo import models, fields, api, _


class AnalyticAccountLineAuxResult(models.Model):
    _name = 'analytic.account.line.aux.result'
    _description = "Account line aux result"

    name = fields.Char(string='Nom')
