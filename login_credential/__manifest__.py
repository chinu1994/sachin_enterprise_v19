{
    "name": "login credential",
    "version": "19.0.1.0.0",
    "license": "LGPL-3",
    "summary": "Product Cost Price",
    "category": "Inventory",
    "author": "Amarjeet",
    "depends": ["product","web","mail"],
    "data": [
        "views/login.xml",
    ],
'assets': {
        'web.assets_backend': [
            'login_credential/static/src/js/idle_logout.js',
        ],
    },
    "installable": True,
    "application": False,
}
