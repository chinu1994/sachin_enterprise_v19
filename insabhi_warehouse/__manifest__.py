{
    "name": "Insabhi Warehouse",
    "version": "19.0.1.0.0",
    "summary": "Show only internal locations in stock operations",
    "category": "Inventory",
    "author": "Brishti",
    "depends": ["stock", "mrp"],
    "data": [
        # "views/picking.xml",
    ],
'assets': {
    'web.assets_backend': [
        'insabhi_warehouse/static/src/js/picking.js',
    ],
},

    "installable": True,
    "application": False,
}
