# -*- coding: utf-8 -*-

from odoo import models, fields, api

class usuario(models.Model):
    #_name = 'simarropop.usuario'
    _name = 'res.partner'
    _description = 'Users of the App'
    _inherit = 'res.partner'

    #name = fields.Char()






# class simarropop(models.Model):
#     _name = 'simarropop.simarropop'
#     _description = 'simarropop.simarropop'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
