from odoo import models, fields


class AccountMove(models.Model):
    _inherit = 'account.move'

    insabhi_packing_list_doc_ids = fields.Many2many(
        'ir.attachment',
        'account_move_packing_list_rel',
        'move_id',
        'attachment_id',
        string='Packing Lists'
    )

    insabhi_LR_copy_doc_ids = fields.Many2many(
        'ir.attachment',
        'account_move_lr_copy_rel',
        'move_id',
        'attachment_id',
        string='LR Copy'
    )

    insabhi_MTC_doc_ids = fields.Many2many(
        'ir.attachment',
        'account_move_mtc_rel',
        'move_id',
        'attachment_id',
        string='MTC'
    )