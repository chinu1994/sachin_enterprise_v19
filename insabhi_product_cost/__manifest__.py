{
    "name": "Insabhi Warehouse",
    "version": "19.0.1.0.0",
    "summary": "Product Cost Price",
    "category": "Inventory",
    "author": "Brishti",
     'depends': ['base','product','sale','sale_management',],
    "data": [
        "security/sale_delete_security.xml",
        "views/groups.xml",
        "views/product.xml"
    ],
# 'assets': {
#     'web.assets_backend': [
#         'insabhi_warehouse/static/src/js/picking.js',
#     ],
# },

    "installable": True,
    "application": False,
}
