# -*- coding: utf-8 -*-
{
    'name': 'Kuwait Partner Localization',
    'version': '16.0.0.0.0',
    'category': 'Generic Modules/Human Resources',
    'summary': 'Kuwait partner localization',
    'description': 'This module extends the partner model to include Kuwait localization.',
    'author': 'Advanced Solutions',
    'company': 'Advanced Solutions',
    'maintainer': 'Advanced Solutions',
    'website': 'https://www.advanced-sol.com/',
    'license': 'LGPL-3',
    'depends': ['base', 'contacts', 'sale','website_sale'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/area.xml',
        'views/sale_order.xml',
        'views/views.xml',
        'views/templates.xml',
        'report/sale_order_report.xml'
    ],
    'installable': True,
    'application': False,
    'auto_install': False,

    'assets': {
        'web.assets_frontend': [
            'kw_partner_localization/static/src/js/website_sale.js',
        ],
    }
}
