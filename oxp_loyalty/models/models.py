# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class oxp_loyalty(models.Model):
#     _name = 'oxp_loyalty.oxp_loyalty'
#     _description = 'oxp_loyalty.oxp_loyalty'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
