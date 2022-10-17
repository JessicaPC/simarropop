# -*- coding: utf-8 -*-
# from odoo import http


# class Battlewarcraft(http.Controller):
#     @http.route('/battlewarcraft/battlewarcraft', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/battlewarcraft/battlewarcraft/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('battlewarcraft.listing', {
#             'root': '/battlewarcraft/battlewarcraft',
#             'objects': http.request.env['battlewarcraft.battlewarcraft'].search([]),
#         })

#     @http.route('/battlewarcraft/battlewarcraft/objects/<model("battlewarcraft.battlewarcraft"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('battlewarcraft.object', {
#             'object': obj
#         })
