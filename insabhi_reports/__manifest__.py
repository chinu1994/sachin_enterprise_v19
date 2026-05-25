{
    'name': 'Insabhi Reports',
    'version': '1.0',
    'category': 'Invoicing',
    'summary': 'Invoicing Report',
    'depends':  ['account'],
    'data': [
            "report/custom_invoice_report.xml",
            "report/tax_invoice_report.xml",

    ],

    # 'assets': {
    #     'web.assets_backend': [
    #     ],
    # },
    'installable': True,
}