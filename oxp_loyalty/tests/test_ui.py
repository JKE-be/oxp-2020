# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import odoo.tests
from unittest.mock import patch


@odoo.tests.tagged('post_install', '-at_install')
class TestUi(odoo.tests.HttpCase):
    def test_oxp(self):
        TransferPayment = odoo.addons.payment_transfer.models.payment.TransferPaymentTransaction
        with patch.object(TransferPayment, '_transfer_form_validate', lambda self, data: self._set_transaction_done()):
            self.start_tour("/", 'oxp_loyalty_tour', login='portal')
