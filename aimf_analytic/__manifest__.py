# -*- coding: utf-8 -*-
{
    'name': 'AIMF analytic',
    'version': '1.0.7',
    'summary': 'AIMF analytic customisation',
    'description': """
AIMF analytic customisation
""",
    'depends': [
        'analytic',
        'account',
        'account_accountant',
        'web',
    ],
    'data': [
        # views
        'views/analytic_account_views.xml',
        'views/account_move_inherit.xml',
        'views/analytic_cost_item_view.xml',
        'views/analytic_account_line_aux_views.xml',
        'views/account_analytic_line_inherit.xml',
        'views/account_analytic_group_inherit.xml',
        'views/analytic_account_line_aux_result.xml',
        'views/status_aimf.xml',
        'views/programation_aimf.xml',

        'views/res_config_settings_inherit.xml',
        #wizards
        'wizards/account_analytic_reassignment_views.xml',
        # datas
        'data/sequence.xml',
        'data/account_analytic_tag.xml',
        # security
        'security/ir.model.access.csv',
        # reports
        'reports/report_invoice_inherit.xml',
    ],
    'qweb': [
    ],
    'test': [
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
