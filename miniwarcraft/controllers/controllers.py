# -*- coding: utf-8 -*-
# from odoo import http


# class Miniwarcraft(http.Controller):
#     @http.route('/miniwarcraft/miniwarcraft', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/miniwarcraft/miniwarcraft/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('miniwarcraft.listing', {
#             'root': '/miniwarcraft/miniwarcraft',
#             'objects': http.request.env['miniwarcraft.miniwarcraft'].search([]),
#         })

#     @http.route('/miniwarcraft/miniwarcraft/objects/<model("miniwarcraft.miniwarcraft"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('miniwarcraft.object', {
#             'object': obj
#         })
