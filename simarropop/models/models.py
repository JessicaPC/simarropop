# -*- coding: utf-8 -*-

from odoo import models, fields, api

class usuario(models.Model):
    #_name = 'simarropop.usuario'
    _name = 'res.partner'
    _description = 'Users de la App'
    _inherit = 'res.partner'

    #name = fields.Char()
    articulos_publicados = fields.One2many("simarropop.articulo", "usuario")
    articulos_favoritos = fields.Many2many("simarropop.articulo", "usuario")
    articulos_comprados = fields.One2many("simarropop.articulo", "usuario_comprador")
    valoraciones = fields.One2many("simarropop.valoracion", "usuario")
    mensajes = fields.One2many("simarropop.mensaje", "usuario")
    mensajes_receptor = fields.One2many("simarropop.mensaje", "usuario")
    fecha_nacimiento =  fields.Datetime()
    contrasenya = fields.Char(required=True)
    is_user = fields.Boolean()
    
    

# ---------------------------------------------------------------------
class articulo(models.Model):
    _name = 'simarropop.articulo'
    _description = 'Articulos de la App'
    

    name = fields.Char()
    usuario = fields.Many2one("res.partner")
    usuario_comprador = fields.Many2one("res.partner")
    categoria = fields.Many2one("simarropop.categoria")
    fotos = fields.One2many("simarropop.foto", "articulo")
    fotos_img = fields.Image(related = "fotos.foto_articulo") 
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
    usuario_receptor = fields.Many2one("res.partner")
    contenido = fields.Char()

# ---------------------------------------------------------------------

class categoria(models.Model):
    _name = 'simarropop.categoria'
    _description = 'Categorias de la App'
    

    name = fields.Char()
    articulo = fields.One2many("simarropop.articulo", "categoria")
    descripcion_categoria = fields.Char()
    categoria_img = fields.Image()
   
    
# ---------------------------------------------------------------------

class foto(models.Model):
    _name = 'simarropop.foto'
    _description = 'Fotos de la App'

    name = fields.Char()
    articulo = fields.Many2one("simarropop.articulo", ondelete="cascade")# si se borra el articulo, se borran sus fotos
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
class venta(models.Model):
    #_name = 'simarropop.usuario'
    _name = 'sale.order'
    _description = 'Ventas de la App'
    _inherit = 'sale.order'

    #name = fields.Char()
    articulo_nombre = fields.Char()
    usuario_nombre = fields.Char()
    accion_nombre = fields.Char()

    

# ---------------------------------------------------------------------
# --------------   WIZARDS ------------------------
class articulo_wizard(models.TransientModel):
    _name = 'simarropop.articulo_wizard'

    name = fields.Char(string='Nombre')
    usuario = fields.Many2one('res.partner', string='Usuario')
    categoria = fields.Many2one('simarropop.categoria', string='Categoría')
    precio = fields.Float(string='Precio')
    descripcion = fields.Char(string='Descripción')
    ubicacion = fields.Char(string='Ubicación')
    fotos_img = fields.Image(string='Foto')
    
    def agregar_articulo(self):
        articulo = self.env['simarropop.articulo'].create({
            'name': self.name,
            'usuario': self.usuario.id,
            'categoria': self.categoria.id,
            'precio': self.precio,
            'descripcion': self.descripcion,
            'ubicacion': self.ubicacion,
            'fotos_img': self.foto_articulo,
        })
        return {'type': 'ir.actions.act_window_close'}
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
