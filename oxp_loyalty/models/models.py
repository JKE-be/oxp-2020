# -*- coding: utf-8 -*-

from odoo import fields, api, models, _


class LoyaltyPack(models.Model):
    _name = "loyalty.pack"
    _description = "Loyalty Pack"

    name = fields.Char(required=1)
    oxp = fields.Integer(default=100, required=1)
    program_id = fields.Many2one('coupon.program', required=1)

    def _convert(self, send_mail=True):
        partner = self.env.user.partner_id
        assert partner.loyalty_amount >= self.point

        coupon = self.env['sale.coupon'].create({
            'program_id': self.program_id.id,
            'partner_id': partner.id,
        })

        self.env['loyalty.history'].create({
            "partner_id": partner.id,
            "amount": -1 * self.point,
            "order_id": False,
            "name": _('Pack %s: %s' % (self.name, coupon.code)),
            "status": 'confirm',
            "coupon_id": coupon.id,
        })
        if send_mail:
            template = self.env.ref('sale_coupon.mail_template_sale_coupon', raise_if_not_found=False)
            self.env['mail.thread'].message_post_with_template(
                template.id, composition_mode='comment',
                model='sale.coupon', res_id=coupon.id,
                email_layout_xmlid='mail.mail_notification_light',
            )
        return coupon


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

    def action_cancel(self):
        res = super().action_cancel()

        # get back all loyalties for this order
        for loy in self.loyalty_ids.filtered(lambda l: l.amount > 0):
            self.env['loyalty.history'].create({
                "partner_id": self.partner_id.id,
                "amount": -1 * loy.amount,
                "order_id": self.id,
                "name": 'Cancel order %s' % self.id,
            })
        return res

    def action_confirm(self):
        res = super().action_confirm()
        self.env['loyalty.history'].sudo().create({
            "partner_id": self.partner_id.id,
            "amount": self._get_amount_loyalty(),
            "order_id": self.id,
            "name": "Order %s" % self.name,
        })
        return res

    def _get_amount_loyalty(self):
        return sum(self.order_line.filtered(lambda r: r.product_id.product_tmpl_id.allow_loyalty).mapped('price_total') * 100)
