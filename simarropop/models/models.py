# -*- coding: utf-8 -*-

from odoo import models, fields, api

class usuario(models.Model):
    #_name = 'simarropop.usuario'
    _name = 'res.partner'
    _description = 'Users de la App'
    _inherit = 'res.partner'

    name = fields.Char(required=True)
    email = fields.Char(required=True)
    phone = fields.Char(required=True)
    city = fields.Char(required=True)
    articulos_publicados = fields.One2many("simarropop.articulo", "usuario")
    articulos_comprados = fields.One2many("simarropop.articulo", "usuario_comprador")
    valoraciones = fields.One2many("simarropop.valoracion", "usuario")
    mensajes = fields.One2many("simarropop.mensaje", "usuario")
    mensajes_receptor = fields.One2many("simarropop.mensaje", "usuario")
    fecha_nacimiento =  fields.Datetime()
    contrasenya = fields.Char(required=True)
    is_user = fields.Boolean()
    valoracion_media = fields.Float(compute='_compute_valoracion_media', store=True) 
        # store = opción que permite almacenar en BD el valor calculado de ese campo, en lugar de calcularlo cada vez que se consulta. 
         # Esto puede mejorar significativamente el rendimiento 
    
    @api.depends('valoraciones.puntuacion')
    def _compute_valoracion_media(self):
        for record in self:
            valoraciones = record.valoraciones
            total_puntuacion = 0
            numero_valoraciones = 0
            for valoracion in valoraciones:
                total_puntuacion += valoracion.puntuacion
                numero_valoraciones += 1
            record.valoracion_media = total_puntuacion / numero_valoraciones if numero_valoraciones else 0
    # record = variable que se utiliza para almacenar los datos de un registro específico
        # puede ser utilizada para mostrar o modificar la información 


    
# ---------------------------------------------------------------------
class articulo(models.Model):
    _name = 'simarropop.articulo'
    _description = 'Articulos de la App'
        
    
      
    name = fields.Char(required=True)
    usuario = fields.Many2one("res.partner")
    usuario_comprador = fields.Many2one("res.partner")
    categoria = fields.Many2one("simarropop.categoria")
    fotos = fields.One2many("simarropop.foto", "articulo")
    fotos_img = fields.Image(related = "fotos.foto_articulo") 
    fotos_img_ruta = fields.Char()
    precio = fields.Float()
    cantidad = fields.Integer()
    precio_total = fields.Float(compute='_compute_precio_total')
    descripcion = fields.Char()
    ubicacion = fields.Char(related="usuario.city")
    fecha_publicacion = fields.Datetime()
    persona_articulos_favoritos = fields.Many2many("res.partner", string="Personas que les gusta este articulo")

    #se cambia el precio en valor de la cantidad que haya de ese articulo
    @api.onchange('precio', 'cantidad')
    def _compute_precio_total(self):
        for record in self:
            record.precio_total = record.precio * record.cantidad
    

    @api.model
    def actualizar_fecha_publicacion(self):
        articulos = self.search([])
        for articulo in articulos:
            articulo.fecha_publicacion = fields.Datetime.now()

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
    

    name = fields.Char(string="Nombre valoracion")
    usuario = fields.Many2one("res.partner")
    opinion = fields.Char()
    puntuacion = fields.Float(min=1,max=10)
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


    def _default_articulo(self):
        return self.env['res.partner'].browse(self._context.get('active_id'))  # El context conté, entre altre coses,
        # el active_id del model que està obert.

   

    name = fields.Char(string='Nombre')
    usuario = fields.Many2one('res.partner', string='Usuario', default=_default_articulo)
    usuario_comprador = fields.Many2one("res.partner")
    categoria = fields.Many2one('simarropop.categoria', string='Categoría')
    precio = fields.Float(string='Precio')
    cantidad = fields.Integer()
    precio_total = fields.Float(compute='_compute_precio_total')
    descripcion = fields.Char(string='Descripción')
    ubicacion = fields.Char(string='Ubicación', related="usuario.city")
    fotos = fields.One2many("simarropop.foto", "articulo")
 
    
    def agregar_articulo(self):
        articulo = self.env['simarropop.articulo'].create({
            'name': self.name,
            'usuario': self.usuario.id,
            'usuario_comprador': self.usuario_comprador.id,
            'categoria': self.categoria.id,
            'precio': self.precio,
            'descripcion': self.descripcion,
            'ubicacion': self.ubicacion,
          
         
        })
        return {'type': 'ir.actions.act_window_close'}

    @api.onchange('precio', 'cantidad')
    def _compute_precio_total(self):
        for record in self:
            record.precio_total = record.precio * record.cantidad


class foto_wizard(models.TransientModel):
    _name = 'simarropop.foto_wizard'

    def _default_foto(self):
        return self.env['simarropop.articulo'].browse(self._context.get('active_id'))  
      

    name = fields.Char(string="foto")
    articulo = fields.Many2one("simarropop.articulo", ondelete="cascade", default=_default_foto)
    foto_articulo = fields.Image()
    fotos_articulo_ruta = fields.Char()

    

    def agregar_foto(self):
        foto = self.env['simarropop.foto'].create({
            'name': self.name,
            'articulo': self.articulo.id,
            'foto_articulo': self.foto_articulo,
            'fotos_articulo_ruta': self.fotos_articulo_ruta,
            
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
