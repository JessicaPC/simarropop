# -*- coding: utf-8 -*-
# https://www.odoo.com/fr_FR/forum/aide-1/create-a-dynamic-form-view-85212
from odoo import models, fields, api
from odoo.exceptions import ValidationError
import random



class player(models.Model):
    _name = 'miniwarcraft.player'
    _description = 'Players of the game'

    def get_name(self): 
        palabra = ["user","usuario"]
        numero = ["0","1", "2", "3", "4", "5", "6", "7", "8","9", "10", 
            "11", "12", "13", "14", "15", "16", "17", "18", "19", "20"]
        return random.choice(palabra) +  random.choice(numero)

    name = fields.Char(string="Nombre", required=True, default=get_name)
    password = fields.Char(required=True)
    avatar = fields.Image(max_width = 100, max_height=100)
    avatar_mini = fields.Image(related="avatar", max_width=50, max_height=50)
    bando = fields.Many2one("miniwarcraft.bando")
    bandoimg = fields.Image(related = "bando.bandoimg")
    bandoimg_mini = fields.Image(related="bandoimg", max_width = 100, max_height=100)
    fecha_registro = fields.Datetime()
    
  

class bando(models.Model):
    _name = 'miniwarcraft.bando'
    _description = 'Bandos'


    name = fields.Char(string="Nombre",required=True)
    type = fields.Selection([('1','Alliance'),('2','Horde')])
    bandoimg = fields.Image(max_width = 100, max_height=100)
    bandoimg_mini = fields.Image(related="bandoimg", max_width = 100, max_height=100)
    descripcion = fields.Char()
    building = fields.Many2one("miniwacraft.building")

  


class building(models.Model):
    _name = 'miniwarcraft.building'
    _description = 'Edificios'
    
    name = fields.Char()
    level = fields.Integer(default=1)
 #   type = fields.Selection([('1','Edificio Alianza'),('2','Edificio Horda')])
    


class building_type(models.Model):
    _name = 'miniwarcraft.building_type'
    _description = 'Tipo de edificios'

    name = fields.Char()
    #price_base = fields.Float()
    #water_production = fields.Float()
    #wood_production = fields.Float()


class battle(models.Model):
    _name = 'miniwarcraft.battle'
    _description = 'Battle'

    name = fields.Char()
    date_start = fields.Datetime()
    date_end = fields.Datetime()
    player1 = fields.Many2one('miniwarcraft.player')
    player2 = fields.Many2one('miniwarcraft.player')
#    type = fields.Many2one('miniwarcraft.building_type')



# class miniwarcraft(models.Model):
#     _name = 'miniwarcraft.miniwarcraft'
#     _description = 'miniwarcraft.miniwarcraft'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
