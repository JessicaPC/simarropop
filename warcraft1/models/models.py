# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
import random
from datetime import datetime

class player(models.Model):
    _name = 'warcraft1.player'
    _description = 'Players of the game'

    

    name = fields.Char(string="Nombre", required=True)
    password = fields.Char(required=True)
    avatar = fields.Image(max_width = 100, max_height=100)
    avatar_mini = fields.Image(related="avatar", max_width=50, max_height=50)
    bando = fields.Many2one("warcraft1.bando")
    bandoimg = fields.Image(related = "bando.bandoimg")
    bandoimg_mini = fields.Image(related="bandoimg", max_width = 100, max_height=100)
    anyo_nacimiento = fields.Integer(required=True)
    fecha_registro = fields.Datetime(default=datetime.today())
    money = fields.Float(default=20.0)
    bandoname = fields.Char(related="bando.name")

    @api.onchange('anyo_nacimiento')
    def _onchange_registro(self):
        if self.anyo_nacimiento > 2015:
            return {'warning' : {'title':'Bad birth year','message': 'The Player is too young'}}
       

    _sql_constraints = [('nombre_uniq','UNIQUE(name)','El nom no es por repetir')]
 
    

class bando(models.Model):
    _name = 'warcraft1.bando'
    _description = 'Bandos'


    name = fields.Char(string="Nombre",required=True)
    bandoimg = fields.Image(max_width = 100, max_height=100)
    bandoimg_mini = fields.Image(related="bandoimg", max_width = 100, max_height=100)
    descripcion = fields.Char()


class colony(models.Model):
    _name = 'warcraft1.colony'
    _description = 'Colonies'


    name = fields.Char(required=True)
    player = fields.Many2one('warcraft1.player', ondelete="cascade")
    player_avatar = fields.Image(related="player.avatar", string="Player Avatar")
    money = fields.Float(related="player.money")
    buildings = fields.One2many('warcraft1.building', 'colony')
    buildings_available = fields.Many2many('warcraft1.building_type',compute='_get_available_buildings')
    hall_level = fields.Integer(default=0)
    required_money_hall = fields.Float(compute='_get_required_money_hall')


    water = fields.Float()
    metal = fields.Float()
    wood = fields.Float()
    food = fields.Float()

    water_production = fields.Float(compute='_get_total_productions')
    metal_production = fields.Float(compute='_get_total_productions')
    wood_production = fields.Float(compute='_get_total_productions')
    food_production = fields.Float(compute='_get_total_productions')

    def _get_required_money_hall(self):
        for c in self:
            c.required_money_hall = 10 ** c.hall_level

    @api.depends('player')
    def _get_available_buildings(self):
        for c in self:
           c.buildings_available = self.env['warcraft1.building_type'].search([('bando', '=', c.player.bando.id), ('cost_structure','<=',c.money) ])

   

    # CRON (aumentar materiales)
    @api.model
    def produce(self):
        self.search([]).produce_colony()


    def produce_colony(self):
        for colony in self:
            water = colony.water + 10
            metal = colony.metal + 6
            wood = colony.wood + 15
            food = colony.food + 10

            colony.write({
                "water": water,
                "metal": metal,
                "wood": wood,
                "food": food,
            })

    @api.depends('buildings')
    def _get_total_productions(self):
        for c in self:
            c.water_production =  sum(c.buildings.mapped('water_production'))
            c.metal_production = sum(c.buildings.mapped('metal_production'))
            c.wood_production =  sum(c.buildings.mapped('wood_production'))
            c.food_production =  sum(c.buildings.mapped('food_production'))



class building(models.Model):
    _name = 'warcraft1.building'
    _description = 'Buildings'

    name = fields.Char(related='type.name')
    image = fields.Image(related='type.image')
    colony = fields.Many2one('warcraft1.colony', ondelete="cascade")
    cost_structure = fields.Integer(related='type.cost_structure')
    hp_structure = fields.Float(related='type.hp_structure')
    type = fields.Many2one('warcraft1.building_type', ondelete="restrict")
    level = fields.Integer(default=1)
    experience = fields.Integer(default=0)
    water_production = fields.Float(compute='_get_productions')
    metal_production = fields.Float(compute='_get_productions')
    wood_production = fields.Float(compute='_get_productions')
    food_production = fields.Float(compute='_get_productions')
    stopped = fields.Boolean(compute='_get_productions')

    def _get_productions(self):
        for b in self:
            level = b.level
            water_production = b.type.water_production * level
            metal_production = b.type.metal_production * level
            wood_production = b.type.wood_production * level
            food_production = b.type.food_production * level

            if water_production + b.colony.water >= 0 and metal_production + b.colony.metal >= 0 and wood_production + b.colony.wood >= 0 and food_production + b.colony.food >= 0:
                b.water_production = water_production
                b.metal_production = metal_production
                b.wood_production = wood_production
                b.food_production = food_production
                b.stopped = False
            else:
                b.water_production = 0
                b.metal_production = 0
                b.wood_production = 0
                b.food_production = 0
                b.stopped = True


class building_type(models.Model):
    _name = 'warcraft1.building_type'
    _description = 'Building types'

    name = fields.Char()
    image = fields.Image(max_width=200, max_height=200)
    bando = fields.Many2one("warcraft1.bando")
    hp_structure = fields.Float()
    cost_structure = fields.Integer()

    water_production = fields.Float()
    metal_production = fields.Float()
    wood_production = fields.Float()
    food_production = fields.Float()
  

    def build(self):  
        for b in self:
            colony_id = self.env['warcraft1.colony'].browse(self.env.context['ctx_colony'])[0]
            if colony_id.money >= b.cost_structure:
                self.env['warcraft1.building'].create({
                    "colony": colony_id.id,
                    "type": b.id
                })
                colony_id.player.money -= b.cost_structure
            else:
                 raise ValidationError("Saldo insuficiente")

           

class battle(models.Model):
    _name = 'warcraft1.battle'
    _description = 'Battle'

    name = fields.Char()
    date_start = fields.Datetime()
    date_end = fields.Datetime()
    player1 = fields.Many2one('warcraft1.player')
    player2 = fields.Many2one('warcraft1.player')
#    type = fields.Many2one('warcraft1.building_type')



# class warcraft1(models.Model):
#     _name = 'warcraft1.warcraft1'
#     _description = 'warcraft1.warcraft1'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
