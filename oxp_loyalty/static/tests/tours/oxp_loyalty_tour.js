odoo.define('oxp_loyalty.tour', function(require) {
"use strict";

var tour = require('web_tour.tour');

tour.register('oxp_loyalty_tour', {
    url: '/shop/customizable-desk-config-9',
    test: true,
},  [{
    trigger: 'div.product_loyalty:contains("Win 75000.0 Oxp by buying this product")',
    content: "Check loyalty message is displayed",
},{
    trigger: '#add_to_cart',
    content: "Adds the product to the cart",
},
{
    trigger: '.o_oxp_amount:contains("75000")',
    content: "Check Oxp gain is displayed",
}, {
    trigger: 'div.input-group-append .js_add_cart_json',
    content: "Set quantity to 2",
},
{
    trigger: '.o_oxp_amount:contains("120000")',
    content: "Check Oxp gain is cumuled and based on new price",
},
{
    trigger: '.oe_website_sale a.btn.btn-primary',
    content: "Proceed to checkout",
},
{
    trigger: '#o_payment_form_pay',
    content: "Proceed to payment",
},
{
    trigger: '#oe_structure_website_sale_confirmation_1',
    content: "Once on confirmation page, go to portal",
    run: function () { window.location.href = '/my/home'; }
},
{
    trigger: '.o_portal_my_home a[title="Loyalties"]',
    content: "Navigate to Loyalties",
    run: 'click',
},
{
    trigger: '.loyal-summary b:contains("120000")',
    content: "Check that user loyalty is at 120000",
},
]);
});
