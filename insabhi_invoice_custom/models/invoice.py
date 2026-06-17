# -*- coding: utf-8 -*-

from odoo import models, fields


class AccountMove(models.Model):
    _inherit = 'account.move'

    insabhi_packing_list_doc_ids = fields.Many2many('ir.attachment', string='Packing Lists')
    insabhi_LR_copy_doc_ids = fields.Many2many('ir.attachment', string='LR Copy')
    insabhi_MTC_doc_ids = fields.Many2many('ir.attachment', string='MTC')