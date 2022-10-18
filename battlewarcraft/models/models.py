# -*- coding: utf-8 -*-
# https://www.odoo.com/fr_FR/forum/aide-1/create-a-dynamic-form-view-85212
from odoo import models, fields, api

import random

class player(models.Model):
    _name = 'battlewarcraft.player'
    _description = 'Players of the game'

    name = fields.Char(string="Nombre", required=True)
    password = fields.Char()
    avatar = fields.Image(max_width = 100, max_height=100)
    avatar_mini = fields.Image(related="avatar", max_width=50, max_height=50)
    bando = fields.Many2one("battlewarcraft.bando")
    bandoimg = fields.Image(related = "bando.bandoimg")
    bandoimg_mini = fields.Image(related="bandoimg", max_width = 100, max_height=100)


class bando(models.Model):
    _name = 'battlewarcraft.bando'
    _description = 'Bandos'

    name = fields.Char(string="Nombre",required=True)
    type = fields.Selection([('1','Alliance'),('2','Horde')])
    bandoimg = fields.Image(max_width = 100, max_height=100)
    bandoimg_mini = fields.Image(related="bandoimg", max_width = 100, max_height=100)

  
class alliance(models.Model):
    _name = 'battlewarcraft.alliance'
    _description = 'Alliance'

    name = fields.Char(string="Nombre",required=True)


 #@api_contrsains('level'){
 #   def check_level(self):
 #       for b in self:
  #              if b.level>10:
  #                  raise ValidationError("level cant be more than 10")
 #}
 
    #bandoimg_tuab = fields.Image(related="bandoimg",max_width = 100, max_height=100)
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
