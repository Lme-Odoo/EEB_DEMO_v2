from odoo import models, fields, api, _

class programation(models.Model):
    _name = 'aimf.programation'
    _description = "Programation"


    name = fields.Char(string='Nom', store=True)