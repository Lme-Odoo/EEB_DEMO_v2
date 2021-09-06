from odoo import models, fields, api, _

class Status(models.Model):
    _name = 'aimf.status'
    _description = "Status"


    name = fields.Char(string='Nom', store=True)