# -*- coding: utf-8 -*-

from odoo import models, fields, api

import random

class player(models.Model):
    _name = 'battlewarcraft.player'
    _description = 'Players of the game'

    name = fields.Char(string="Nombre", required=True)
    password = fields.Char()
    avatar = fields.Image(max_width = 200, max_height=200)
    bando = fields.Many2one("battlewarcraft.bando")

class bando(models.Model):
    _name = 'battlewarcraft.bando'
    _description = 'Bandos'

    name = fields.Char(string="Nombre",required =True)
    type = fields.Selection([('1','Alliance'),('2','Horde')])
    imagenbando = fields.Image(max_width = 150, max_height=150)
  
 
 

# class battlewarcraft(models.Model):
#     _name = 'battlewarcraft.battlewarcraft'
#     _description = 'battlewarcraft.battlewarcraft'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
