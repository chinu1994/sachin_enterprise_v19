{
    'name': 'Insabhi Rank Filter',
    'version': '1.0',
    'summary': 'Filter partner based on customer_rank and vendor_rank',
    'depends': [
        'sale',
        'purchase',
        'account',
        'stock'
    ],
    'data': [
        'views/sale_order_view.xml',
        'views/purchase_order_view.xml',
        'views/account_move_view.xml',
        'views/stock_picking_view.xml',
    ],
    'installable': True,
    'application': False,
}