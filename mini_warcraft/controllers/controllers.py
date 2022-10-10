# -*- coding: utf-8 -*-
# from odoo import http


# class MiniWarcraft(http.Controller):
#     @http.route('/mini_warcraft/mini_warcraft', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mini_warcraft/mini_warcraft/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('mini_warcraft.listing', {
#             'root': '/mini_warcraft/mini_warcraft',
#             'objects': http.request.env['mini_warcraft.mini_warcraft'].search([]),
#         })

#     @http.route('/mini_warcraft/mini_warcraft/objects/<model("mini_warcraft.mini_warcraft"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mini_warcraft.object', {
#             'object': obj
#         })
