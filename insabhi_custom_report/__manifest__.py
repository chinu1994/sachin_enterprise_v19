{
    'name': 'Insabhi Custom Report',
    'version': '1.0',
    'category': 'Sales',
    'summary': 'Sale Order Report',
    'depends':  ['sale','sale_management'],
    'data': [
        "views/sale_order_views.xml",
        "views/res_config_settings_views.xml",
        "report/custom_report.xml",
    ],
    'installable': True,
}