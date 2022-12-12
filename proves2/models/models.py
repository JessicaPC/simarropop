# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
import random

class player(models.Model):
    _name = 'expanse.player'
    _description = 'Players of the game'

    def get_name(self): # tindre un def diferent en el proyecte
        first = ["Mad","Rig"]
  #      first = list(string.ascii_lowercase)
        second = ["Garcia","Mantis"]
        print("************************GENERATED")
        return random.choice(first) + " "+ random.choice(second)
    name = fields.Char(required=True, default=get_name())
    password = fields.Char()
    avatar = fields.image(max_width = 200, max_height=200)
    avatar_tuab = fields.image(related="avatar",max_width = 200, max_height=200)
    colonies = fields.One2many('expanse.colony', 'player')
    spaceship = fields.Many2Many
    colonies_qty = fields.Integer(compute="get_colonies_qty") #quantitat de colonies
#constrain nombre repetido
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

#colonies
    def update_hanger(self):
        for c in self:
            required_money = 10++c.hanger_level
            available_money = c.player.money
            if(required_money <= available_money):
                c.hanger_level == 1
                c.player.money = c.player.money - required_money

class battle(models.Model):
    _name = 'expanse.battle'
    _description = 'Battle'

    name = fields.Char()
    date_start = fields.Datetime()
    date_end = fields.Datetime()
    player1 = fields.Many2one('expanse.player')
    player2 = fields.Many2one('expanse.player')

# si cambie el juagdor, cambiara el nom al isntant, no esperar a guardar
    @api.onchange('player1')
    def onchange_player1(self):
    self.name = self.player1.name
    return{
        'domain':{
            'colony1':[('id', 'in', self.player1.colonies.ids)],
            'player2':[('id', 'in', )]
        }
    }


#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
