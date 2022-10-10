# -*- coding: utf-8 -*-

from odoo import models, fields, api
import random

class player(models.Model):
     _name = 'miniWarcraft.player'
     _description = 'Players of the Game'

     def get_name(self):  # tindre un def diferent en el proyecte
         nombre = ["Thrall", "Anduin","Jaina"]
         apellido = ["Garcia", "Valiente","caca"]
         print("************************Nombre generado")
         return random.choice(nombre) + " " + random.choice(apellido)

     name = fields.Char(required=True, default=get_name())
     password = fields.Char()
     avatar = fields.image(max_width=200, max_height=200)


#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
