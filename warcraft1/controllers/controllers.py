# -*- coding: utf-8 -*-
# from odoo import http


# class Warcraft1(http.Controller):
#     @http.route('/warcraft1/warcraft1', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/warcraft1/warcraft1/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('warcraft1.listing', {
#             'root': '/warcraft1/warcraft1',
#             'objects': http.request.env['warcraft1.warcraft1'].search([]),
#         })

#     @http.route('/warcraft1/warcraft1/objects/<model("warcraft1.warcraft1"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('warcraft1.object', {
#             'object': obj
#         })
