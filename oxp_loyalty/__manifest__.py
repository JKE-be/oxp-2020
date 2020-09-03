# -*- coding: utf-8 -*-
{
    'name': "oxp_loyalty",
    'author': "Odoo SA - Jeremy Kersten",
    'website': "https://www.odoo.com",

    'category': 'Website/Website',
    'version': '0.1',
    'license': 'LGPL-3',

    'description': """
        Win 'Oxp' during your online shopping and convert it into coupon !
    """,

    'depends': ['base', 'website_sale_coupon'],  # website_sale + coupon

    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'data/data.xml',
    ],
}
