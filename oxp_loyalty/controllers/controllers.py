# -*- coding: utf-8 -*-
from odoo import http, _
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal


class WebsiteAccount(CustomerPortal):

    @http.route('/my/loyalties', auth='user', website=True)
    def portal_my_loyalties(self):
        params = {
            'pack_ids': request.env['loyalty.pack'].sudo().search([])
        }
        return request.render('oxp_loyalty.portal_my_loyalties', params)

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if 'loyalty_count' in counters:
            values['loyalty_count'] = request.env.user.partner_id.loyalty_amount
        return values

class Loyalties(http.Controller):

    @http.route('/loyalties/convert/<int:pack>', auth='user', website=True)
    def loyalty_convert_pack(self, pack):
        pack = request.env['loyalty.pack'].sudo().browse(pack)

        error = False
        my_loyalties = request.env.user.partner_id.loyalty_amount

        if my_loyalties >= pack.oxp:
            coupon = pack._convert()
            return request.redirect('/loyalties/thanks/%s/%s' % (pack.id, coupon.id))

        error = _('Not enough Oxp! You have %s Oxp, but %s Oxp is needed') % (my_loyalties, pack.oxp)
        return request.render('oxp_loyalty.loyalties_coupon', {
            'error': error,
            'coupon': False,
            'pack': pack,
        })

    @http.route('/loyalties/thanks/<int:pack_id>/<int:coupon_id>', auth='user', website=True)
    def loyalty_thanks(self, coupon_id, pack_id):
        pack = request.env['loyalty.pack'].sudo().browse(pack_id)
        coupon = request.env['coupon.coupon'].sudo().browse(coupon_id).exists()
        error = False

        if not coupon:
            error = _("Coupon Not found")
        elif coupon.partner_id != request.env.user.partner_id:
            error = _("Unmatch User")

        return request.render('oxp_loyalty.loyalties_coupon', {
            'error': error,
            'coupon': not error and coupon,
            'pack': pack,
        })
