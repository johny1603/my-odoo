{
    'name' : 'Bikes',
    'version' : '1.1',
    'summary': 'Bike information',
    'sequence': 1,
    'description': """
    """,
    'category': 'Bike',
    'website': '',
    'images' : [],
    'depends' : [
        'mail','base','web','website',
    ],
    'data': [
        'security/customer_security.xml',
        'security/ir.model.access.csv',
        'data/template.xml',
        'data/res.config.xml',
        'data/schedule_action_views.xml',
        'data/cron_template.xml',
        'data/ir_sequence.xml',
        'views/report/customer_report.xml',
        'views/report/report.xml',
        'wizard/gender_based_report_views.xml',
        'views/bike_views.xml',
        'views/customer_views.xml',
        'views/service.xml',
        'views/payment_views.xml',
        'views/res_config_view.xml',
        'views/client_action_views.xml',

    ],
    'demo': [
    ],
    'qweb': [
        "static/src/xml/*.xml",
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}