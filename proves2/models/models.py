# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
import random

class player(models.Model):
    _name = 'expanse.player'
    _description = 'Players of the game'

    def get_name(self): # tindre un def diferent en el proyecte
        first = ["Mad","Rig"]
        second = ["Garcia","Mantis"]
        print("************************GENERATED")
        return random.choice(first) + " "+ random.choice(second)
    name = fields.Char(required=True, default=get_name())
    password = fields.Char()
    avatar = fields.image(max_width = 200, max_height=200)
    colonies = fields.One2many('expanse.colony', 'player')
    colonies_qty = fields.Integer(compute="get_colonies_qty") #quantitat de colonies

    @api.depends('colonies')
    def get_colonies_qty(self):
        print(self)
        for p in self:
            print(p,p.name)
            p.colonies_qty = len(p.colonies) #longitud de un array


class planet(models.Model):
    _name = 'expanse.planet'
    _description = 'Planets'

    name = fields.Char(required=True)
    avatar = fields.image(max_width=200, max_height=200)
    size = fields.Float()
    gravity = fields.Float(compute='_get_gravity')
    colonies = fields.One2many('expanse.colony', 'planet')

    @api.constrains('size')
    def check_planet_size(self): #funcio sempre amb for
        for planet in self:
                if planet.size> 1000 or planet.size <1:
                    raise  ValidationError("Your planet is too big: %s" % planet.size)

    @api.depends('size')
    def _get_gravity(self):  # funcio sempre amb for
        for planet in self:
                if planet.size > 1000 or planet.size < 1:
                    planet.gravity = planet.size*10

class colony(models.Model):
    _name = 'expanse.colony'
    _description = 'Colonies'

    name = fields.Char(required=True)
    planet = fields.Many2one('expanse.planet')
    player = fields.Many2one('expanse.player')
    player_avatar = fields.Image(related='player.avatar')
    creation_date = fields.Datetime(default = fields.Date.now())


class spaceship(models.Model):
    _name = 'expanse.spaceship'
    _description = 'Spaceship'

    name = fields.Char(required=True)
    colonies = fields.One2many('expanse.colony', 'planet')
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
