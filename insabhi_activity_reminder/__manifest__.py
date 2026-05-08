# -*- coding: utf-8 -*-
{
    'name': 'Insabhi Activity Reminder',
    'version': '19.0.1.0.0',
    'category': 'Tools',
    'author': 'Insabhi',
    'summary': 'Send reminder emails to chatter followers on activity deadline',
    'depends': ['mail'],
    'data': [
        'data/ir_cron.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}