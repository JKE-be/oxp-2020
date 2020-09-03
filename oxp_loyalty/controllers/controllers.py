# -*- coding: utf-8 -*-
# from odoo import http


# class OxpLoyalty(http.Controller):
#     @http.route('/oxp_loyalty/oxp_loyalty/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/oxp_loyalty/oxp_loyalty/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('oxp_loyalty.listing', {
#             'root': '/oxp_loyalty/oxp_loyalty',
#             'objects': http.request.env['oxp_loyalty.oxp_loyalty'].search([]),
#         })

#     @http.route('/oxp_loyalty/oxp_loyalty/objects/<model("oxp_loyalty.oxp_loyalty"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('oxp_loyalty.object', {
#             'object': obj
#         })
