# -*- coding: utf-8 -*-

from odoo import models, fields, api

import random

class player(models.Model):
    _name = 'mini_warcraft.player'
    _description = 'Players of the game'

    name = fields.Char(string="Nombre", required=True)
    password = fields.Char()
    avatar = fields.Image(max_width = 200, max_height=200)
    

class bando(models.Model):
    _name = 'mini_warcraft.bando'
    _description = 'Bandos'

    type = fields.Selection([('1','Alianza'),('2','Horda')])
    name = fields.Selection(selection='a_function_name')
   
# class mini_warcraft(models.Model):
#     _name = 'mini_warcraft.mini_warcraft'
#     _description = 'mini_warcraft.mini_warcraft'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
