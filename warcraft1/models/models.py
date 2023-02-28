# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
import random
from datetime import datetime

class player(models.Model):
    _name = 'res.partner'
    _description = 'Players of the game'
    _inherit='res.partner'

    #name = fields.Char(string="Nombre", required=True)
    password = fields.Char(required=True)
    avatar = fields.Image(max_width = 100, max_height=100)
    avatar_mini = fields.Image(related="avatar", max_width=50, max_height=50)
    bando = fields.Many2one("warcraft1.bando")
    bandoimg = fields.Image(related = "bando.bandoimg")
    bandoimg_mini = fields.Image(related="bandoimg", max_width = 100, max_height=100)
    anyo_nacimiento = fields.Integer(required=True)
    fecha_registro = fields.Datetime(default=datetime.today())
    bandoname = fields.Char(related="bando.name")
    is_player = fields.Boolean()
    colony = fields.One2many("warcraft1.colony", "player")
    colony_count = fields.Integer(compute="_compute_colony_count", store=True)


    @api.onchange('anyo_nacimiento')
    def _onchange_registro(self):
        if self.anyo_nacimiento > 2015:
            return {'warning' : {'title':'Bad birth year','message': 'The Player is too young'}}
      
    _sql_constraints = [('nombre_uniq','UNIQUE(name)','El nom no es por repetir')]


     #llança un action  
    def launch_player_wizard(self):
        return {
            'name': 'Create Player',
            'type':'ir.actions.act_window',
            'res_model':'warcraft1.player_wizard',
            'view_mode':'form',
            'target':'new',
        }

    @api.depends('colony')
    def _compute_colony_count(self):
        for player in self:
            player.colony_count = len(player.colony)

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
    player = fields.Many2one('res.partner', domain="[('is_player','=',True)]", ondelete="cascade",required=True)
    player_avatar = fields.Image(related="player.avatar", string="Player Avatar")
    money = fields.Float(default=100.0)
    buildings = fields.One2many('warcraft1.building', 'colony')
    buildings_available = fields.Many2many('warcraft1.building_type',compute='_get_available_buildings')
    hall_level = fields.Integer(default=0)
    required_money_hall = fields.Float(compute='_get_required_money_hall')


    water = fields.Float()
    metal = fields.Float()
    wood = fields.Float()
    food = fields.Float()
    warrior = fields.Integer()

    money_production = fields.Float(compute='_get_total_productions')
    water_production = fields.Float(compute='_get_total_productions')
    metal_production = fields.Float(compute='_get_total_productions')
    wood_production = fields.Float(compute='_get_total_productions')
    food_production = fields.Float(compute='_get_total_productions')
    warrior_production = fields.Integer(compute='_get_total_productions')


    def _get_required_money_hall(self):
        for c in self:
            c.required_money_hall = 10 ** c.hall_level

    @api.depends('player')
    def _get_available_buildings(self):
        for c in self:
           c.buildings_available = self.env['warcraft1.building_type'].search([('bando', '=', c.player.bando.id), ('cost_structure','<=',c.money) ])


    @api.depends('buildings')
    def _get_total_productions(self):
        for c in self:
            if len(c.buildings)>0:
                c.money_production =  sum(c.buildings.mapped('money_production'))
                c.water_production =  sum(c.buildings.mapped('water_production'))
                c.metal_production = sum(c.buildings.mapped('metal_production'))
                c.wood_production =  sum(c.buildings.mapped('wood_production'))
                c.food_production =  sum(c.buildings.mapped('food_production'))
                c.warrior_production =  sum(c.buildings.mapped('warrior_production'))
                
            else:
                c.money = c.money

    # CRON (aumentar materiales)
    @api.model
    def produce(self):
        self.search([]).produce_colony()


    def produce_colony(self):
        for colony in self:
            money = colony.money
            water = colony.water + colony.water_production
            metal = colony.metal + colony.metal_production
            wood = colony.wood + colony.wood_production
            food = colony.food + colony.food_production
            warrior = colony.warrior + colony.warrior_production
            
            if len(colony.buildings)>0:
                money += colony.money_production

            colony.write({
                "money":money,
                "water": water,
                "metal": metal,
                "wood": wood,
                "food": food,
                "warrior": warrior,
            })


    _sql_constraints = [    ('player_uniq', 'unique(player)', 'Un jugador solo puede tener una colonia'),  ('name_uniq', 'unique(name)', 'El nombre de la colonia debe ser único'),]
    
    
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
    money_production = fields.Float(compute='_get_productions')
    water_production = fields.Float(compute='_get_productions')
    metal_production = fields.Float(compute='_get_productions')
    wood_production = fields.Float(compute='_get_productions')
    food_production = fields.Float(compute='_get_productions')
    warrior_production = fields.Integer(compute='_get_productions')
    stopped = fields.Boolean(compute='_get_productions')

    def _get_productions(self):
        for b in self:
            level = b.level
            money_production = b.type.money_production * level
            water_production = b.type.water_production * level
            metal_production = b.type.metal_production * level
            wood_production = b.type.wood_production * level
            food_production = b.type.food_production * level
            warrior_production = b.type.warrior_production * level

            if money_production + b.colony.money >= 0 and water_production + b.colony.water >= 0 and metal_production + b.colony.metal >= 0 and wood_production + b.colony.wood >= 0 and food_production + b.colony.food >= 0 and warrior_production + b.colony.warrior >= 0:
                b.money_production = money_production
                b.water_production = water_production
                b.metal_production = metal_production
                b.wood_production = wood_production
                b.food_production = food_production
                b.warrior_production = warrior_production
                b.stopped = False
            else:
                money_production = 0
                b.water_production = 0
                b.metal_production = 0
                b.wood_production = 0
                b.food_production = 0
                b.warrior_production = 0
                b.stopped = True


class building_type(models.Model):
    _name = 'warcraft1.building_type'
    _description = 'Building types'

    name = fields.Char()
    image = fields.Image(max_width=200, max_height=200)
    bando = fields.Many2one("warcraft1.bando")
    hp_structure = fields.Float()
    cost_structure = fields.Integer()

    money_production = fields.Float()
    water_production = fields.Float()
    metal_production = fields.Float()
    wood_production = fields.Float()
    food_production = fields.Float()
    warrior_production = fields.Integer()
  

    def build(self):  
        for b in self:
            colony_id = self.env['warcraft1.colony'].browse(self.env.context['ctx_colony'])[0]
            if colony_id.money >= b.cost_structure:
                self.env['warcraft1.building'].create({
                    "colony": colony_id.id,
                    "type": b.id
                })
                colony_id.money -= b.cost_structure
            else:
                 raise ValidationError("Saldo insuficiente")

           

class battle(models.Model):
    _name = 'warcraft1.battle'
    _description = 'Battle'

    name = fields.Char(required=True)
    date_start = fields.Datetime()
    date_end = fields.Datetime()
    player1 = fields.Many2one('res.partner', string='Player 1', required=True)
    player2 = fields.Many2one('res.partner', string='Player 2', required=True)
    colony_count_p1 = fields.Integer(string='Player 1 Colonies', related="player1.colony_count")
    colony_count_p2 = fields.Integer(string='Player 2 Colonies',  related="player2.colony_count")
    player_ids = fields.Many2many('res.partner', string='Players')
    winner = fields.Char(string='Winner')

    _sql_constraints = [('unique_players', 'CHECK (player1 != player2)', 'Both players should be different')]

    @api.constrains('player1', 'player2')
    def _check_players(self):
        if self.player1 == self.player2:
            raise ValidationError("Both players should be different")
 
    @api.onchange('player_ids')
    def _onchange_player_ids(self):
        if self.player1 and self.player2:
            colony_count_p1 = sum(player.colony_count for player in self.player_ids.filtered(lambda p: p.id == self.player1.id))
            colony_count_p2 = sum(player.colony_count for player in self.player_ids.filtered(lambda p: p.id == self.player2.id))
            self.colony_count_p1 = colony_count_p1
            self.colony_count_p2 = colony_count_p2
    
    def start_battle(self):
        if self.colony_count_p1 <= 0 or self.colony_count_p2 <= 0:
            raise ValidationError("Both players must have at least one colony")

        if self.player1.colony.warrior > self.player2.colony.warrior:
            self.winner = self.player1.name
        elif self.player2.colony.warrior > self.player1.colony.warrior:
            self.winner = self.player2.name
        else:
            self.winner = 'Tie!'
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Winner!',
                'message': f'The winner is {self.winner}!',
                'sticky': False,
            }
        }

#    type = fields.Many2one('warcraft1.building_type')

# ---------------------------- WIZARD -----------------------------------
# model que pot ser, siga borrat
class player_wizard(models.TransientModel):
    _name = 'warcraft1.player_wizard'
    _description = 'Wizard create  new Clients Players'

    # El context conté, entre altre coses,
    # el active_id del model que està obert.
    def _default_client(self):
         return self.env['res.partner'].browse(self._context.get('active_id')) 

    name = fields.Many2one('res.partner', default=_default_client)
    password = fields.Char(required = True)
    avatar = fields.Image(max_width = 100, max_height=100)
    anyo_nacimiento = fields.Integer(required=True)

    def create_player(self):
        self.ensure_one()
        self.name.write({"password":self.password,
                        "avatar":self.avatar,
                        "is_player":True,
                        })


# NO ES PODIA crear un boto per a crear tots els pasos fins a la batalla dalt, per la ver. de odoo
# crear usuaris>crear colonies> crear batalla
# Aixi, que el botó es troba dins d'un player en la seua vista form
# seleccionar jugador1>seleccionar juagdor2 > crear batalla
class battle_wizard(models.TransientModel):
    _name = 'warcraft1.battle_wizard'
    _description = 'Battle Wizard'


    def _default_player(self):
        return self.env['res.partner'].browse(self._context.get('active_id')) 

    name = fields.Char()
    date_start = fields.Datetime()
    date_end = fields.Datetime()
    player1 = fields.Many2one('res.partner', string='Player 1', default=_default_player)
    player2 = fields.Many2one('res.partner', string='Player 2')
    colony_count_p1 = fields.Integer(string='Player 1 Colonies', related="player1.colony_count")
    colony_count_p2 = fields.Integer(string='Player 2 Colonies',  related="player2.colony_count")
    player_ids = fields.Many2many('res.partner', string='Players')
    winner = fields.Char(string='Winner')
    state = fields.Selection([('1', 'Jugador1'),('2', 'Jugador2'),('3', 'Batalla')], default='1')

    _sql_constraints = [('unique_players', 'CHECK (player1 != player2)', 'Both players should be different')]

    @api.constrains('player1', 'player2')
    def _check_players(self):
        if self.player1 == self.player2:
            raise ValidationError("Both players should be different")
 
    @api.onchange('player_ids')
    def _onchange_player_ids(self):
        if self.player1 and self.player2:
            colony_count_p1 = sum(player.colony_count for player in self.player_ids.filtered(lambda p: p.id == self.player1.id))
            colony_count_p2 = sum(player.colony_count for player in self.player_ids.filtered(lambda p: p.id == self.player2.id))
            self.colony_count_p1 = colony_count_p1
            self.colony_count_p2 = colony_count_p2
    
    def start_battle(self):
        if self.colony_count_p1 <= 0 or self.colony_count_p2 <= 0:
            raise ValidationError("Both players must have at least one colony")

        if self.player1.colony.warrior > self.player2.colony.warrior:
            self.winner = self.player1.name
        elif self.player2.colony.warrior > self.player1.colony.warrior:
            self.winner = self.player2.name
        else:
            self.winner = 'Tie!'
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Winner!',
                'message': f'The winner is {self.winner}!',
                'sticky': False,
            }
        }

    def action_previous(self):
        if self.state == '2':
            self.state = '1'
        elif self.state == '3':
            self.state = '2'
        return{
            'name': 'create battle',
            'type': 'ir.actions.act_window',
            'res_model': 'warcraft1.battle_wizard',
            'view_mode': 'form',
            'target': 'new',
            'res_id': self.id
        }
    
    def action_next(self):
        if self.state == '1':
            self.state = '2'
        elif self.state == '2':
            self.state = '3'
        elif self.state == '3':
            if not self.name or not self.player1 or not self.player2:
                raise ValidationError("Please fill in all required fields")
        return {
            'name': 'create battle',
            'type': 'ir.actions.act_window',
            'res_model': 'warcraft1.battle_wizard',
            'view_mode': 'form',
            'target': 'new',
            'res_id': self.id,
        }


    def edit_player(self):
        if self.state == '1':
            return {
                'name': 'edit player',
                'type': 'ir.actions.act_window',
                'res_model': 'warcraft1.edit_player_state1',
                'view_mode': 'form',
                'target': 'new',
                'context':{ 
                    'ctx_player':self.player1.id,
                    'keep_open': True
                }
            }
        elif self.state == '2':
            return {
                'name': 'edit player',
                'type': 'ir.actions.act_window',
                'res_model': 'warcraft1.edit_player_state1',
                'view_mode': 'form',
                'target': 'new',
                'context':{ 
                    'ctx_player':self.player2.id,
                    'keep_open': True
                }
            }
    
    def action_battle_wizard(self):
        if self._context.get('keep_open'):
            return {'type': 'ir.actions.act_window_close'}

        battle = self.env['warcraft1.battle'].create({
            'name': self.name,
            'date_start': self.date_start,
            'date_end': self.date_end,
            'player1': self.player1.id,
            'player2': self.player2.id,
            'colony_count_p1': self.colony_count_p1,
            'colony_count_p2': self.colony_count_p2,
            'player_ids': self.player_ids.id,
            'winner': self.winner,
          
         
        })
        return {'type': 'ir.actions.act_window_close'}



class edit_player_state1(models.Model):
    _name = 'warcraft1.edit_player_state1'
    _description = 'Players State'


    def _default_player(self):
        player_id = self.env.context.get('ctx_player')
        if player_id:
            return self.env['res.partner'].browse(player_id) 
        return self.env['res.partner']

    player = fields.Many2one('res.partner', string='Player 1', default=_default_player)
    name = fields.Char(string="Nombre", required=True)
    password = fields.Char(required=True)
    avatar = fields.Image(max_width = 100, max_height=100)
    bando = fields.Many2one("warcraft1.bando")
    bandoimg = fields.Image()
    anyo_nacimiento = fields.Integer(required=True)
    fecha_registro = fields.Datetime(default=datetime.today())
    bandoname = fields.Char()
    is_player = fields.Boolean()
    colony = fields.One2many("warcraft1.colony", "player")
    colony_count = fields.Integer(compute="_compute_colony_count", store=True)
    
    @api.onchange('anyo_nacimiento')
    def _onchange_registro(self):
        if self.anyo_nacimiento > 2015:
            return {'warning' : {'title':'Bad birth year','message': 'The Player is too young'}}
      
    _sql_constraints = [('nombre_uniq','UNIQUE(name)','El nom no es por repetir')]


     #llança un action  
    def launch_player_wizard(self):
        return {
            'name': 'Create Player',
            'type':'ir.actions.act_window',
            'res_model':'warcraft1.player_wizard',
            'view_mode':'form',
            'target':'new',
        }

    @api.depends('colony')
    def _compute_colony_count(self):
        for player in self:
            player.colony_count = len(player.colony)

    def edit_player(self):
        self.player.write({
            'name': self.name,
            'password': self.password,
            'avatar': self.avatar,
            'bando': self.bando.id,
            'bandoimg': self.bandoimg,
            'anyo_nacimiento': self.anyo_nacimiento,
            'fecha_registro': self.fecha_registro,
            'bandoname': self.bandoname,
            'is_player': self.is_player,
            'colony': self.colony.id,
            'colony_count': self.colony_count,
        })
