# -*- coding: utf-8 -*-

from odoo import models, fields, api

class usuario(models.Model):
    #_name = 'simarropop.usuario'
    _name = 'res.partner'
    _description = 'Users de la App'
    _inherit = 'res.partner'

    #name = fields.Char()
    articulos = fields.One2many("simarropop.articulo", "usuario")
    valoraciones = fields.One2many("simarropop.valoracion", "usuario")
    mensajes = fields.One2many("simarropop.mensaje", "usuario")
    fecha_nacimiento =  fields.Datetime()
    contrasenya = fields.Char(required=True)
    is_user = fields.Boolean()

# ---------------------------------------------------------------------
class articulo(models.Model):
    _name = 'simarropop.articulo'
    _description = 'Articulos de la App'
    

    name = fields.Char()
    usuario = fields.Many2one("res.partner")
    categoria = fields.Many2one("simarropop.categoria")
    fotos = fields.One2many("simarropop.foto", "articulo")
    fotos_img = fields.Image(related = "fotos.foto_articulo") # si se borra el articulo, se borran sus fotos
    fotos_img_ruta = fields.Char()
    precio = fields.Float()
    descripcion = fields.Char()
    ubicacion = fields.Char()
    
# ---------------------------------------------------------------------

class mensaje(models.Model):
    _name = 'simarropop.mensaje'
    _description = 'Mensajes de la App'
    

    name = fields.Char()
    usuario = fields.Many2one("res.partner")
    contenido = fields.Char()

# ---------------------------------------------------------------------

class categoria(models.Model):
    _name = 'simarropop.categoria'
    _description = 'Categorias de la App'
    

    name = fields.Char()
    articulo = fields.One2many("simarropop.articulo", "categoria")
    descripcion_categoria = fields.Char()
    categoria_img = fields.Image()
    minicategoria_img = fields.Image(related="categoria_img", max_width = 100, max_height=100)
    
# ---------------------------------------------------------------------

class foto(models.Model):
    _name = 'simarropop.foto'
    _description = 'Fotos de la App'

    name = fields.Char()
    articulo = fields.Many2one("simarropop.articulo", ondelete="cascade")
    foto_articulo = fields.Image()
    fotos_articulo_ruta = fields.Char()
    

# ---------------------------------------------------------------------

class valoracion(models.Model):
    _name = 'simarropop.valoracion'
    _description = 'Valoraciones de la App'
    

    name = fields.Char()
    usuario = fields.Many2one("res.partner")
    opinion = fields.Char()
    puntuacion = fields.Float()
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
