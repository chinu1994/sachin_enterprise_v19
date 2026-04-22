{
    'name': 'Insabhi Product Access Control',
    'version': '1.0',
    'category': 'Inventory',
    'summary': 'Restrict product access (only price editable)',
    'depends': ['product'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
}