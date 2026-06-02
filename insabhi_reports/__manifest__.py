{
    'name': 'Insabhi Reports',
    'version': '1.0',
    'category': 'Invoicing',
    'summary': 'Invoicing Report',
    'depends':  ['account','stock'],
    'data': [
            "report/custom_invoice_report.xml",
            "report/tax_invoice_report.xml",
            "report/delivery_report.xml",
            "views/stock_picking_views.xml",
            "views/res_compnay_views.xml",
    ],

    # 'assets': {
    #     'web.assets_backend': [
    #     ],
    # },
    'installable': True,
}