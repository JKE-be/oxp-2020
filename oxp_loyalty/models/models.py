# -*- coding: utf-8 -*-

from odoo import fields, api, models, _


class LoyaltyHistory(models.Model):
    _name = "loyalty.history"
    _description = "Loyalty History"
    _order = 'id desc'

    name = fields.Char()
    partner_id = fields.Many2one('res.partner', required=1)
    amount = fields.Integer()
    order_id = fields.Many2one('sale.order')
    coupon_id = fields.Many2one('coupon.program')


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    allow_loyalty = fields.Boolean(default=True, help="Offer Oxp when customer buy it")

    def _compute_label(self):
        self.ensure_one()
        return self.allow_loyalty and _('Win %s Oxp by buying this product', self.price * 100) or ''


class ResPartner(models.Model):
    _inherit = 'res.partner'

    loyalty_ids = fields.One2many('loyalty.history', 'partner_id')
    loyalty_amount = fields.Integer(compute='_compute_loyalties', store=True)

    @api.depends('loyalty_ids', 'loyalty_ids.amount')
    def _compute_loyalties(self):
        for p in self:
            # could by done in groupby if displayed in multi
            p.loyalty_amount = sum(p.loyalty_ids.mapped('amount'))


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    loyalty_ids = fields.One2many('loyalty.history', 'order_id')
