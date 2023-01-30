# -*- coding: utf-8 -*-

from odoo import models, fields, api

class usuario(models.Model):
    #_name = 'simarropop.usuario'
    _name = 'res.partner'
    _description = 'Users de la App'
    _inherit = 'res.partner'

    #name = fields.Char()
# ---------------------------------------------------------------------
class articulo(models.Model):
    _name = 'simarropop.articulo'
    _description = 'Articulos de la App'
    

    name = fields.Char()

# ---------------------------------------------------------------------

class mensaje(models.Model):
    _name = 'simarropop.mensaje'
    _description = 'Mensajes de la App'
    

    name = fields.Char()

# ---------------------------------------------------------------------

class categoria(models.Model):
    _name = 'simarropop.categoria'
    _description = 'Categorias de la App'
    

    name = fields.Char()

# ---------------------------------------------------------------------

class foto(models.Model):
    _name = 'simarropop.foto'
    _description = 'Fotos de la App'
    

    name = fields.Char()

# ---------------------------------------------------------------------

class valoracion(models.Model):
    _name = 'simarropop.valoracion'
    _description = 'Valoraciones de la App'
    

    name = fields.Char()

# ---------------------------------------------------------------------


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
