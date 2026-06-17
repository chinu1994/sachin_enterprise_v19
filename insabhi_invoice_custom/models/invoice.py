from odoo import api, fields, models


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

    def _sync_attachments_to_chatter(self):
        """
        Ensure all attachments linked in custom fields
        are also linked to the account.move record.
        """
        for move in self:
            attachments = (
                move.insabhi_packing_list_doc_ids |
                move.insabhi_LR_copy_doc_ids |
                move.insabhi_MTC_doc_ids
            )

            attachments.write({
                'res_model': 'account.move',
                'res_id': move.id,
            })

    @api.model_create_multi
    def create(self, vals_list):
        moves = super().create(vals_list)
        moves._sync_attachments_to_chatter()
        return moves

    def write(self, vals):
        res = super().write(vals)

        attachment_fields = {
            'insabhi_packing_list_doc_ids',
            'insabhi_LR_copy_doc_ids',
            'insabhi_MTC_doc_ids',
        }

        if attachment_fields.intersection(vals.keys()):
            self._sync_attachments_to_chatter()

        return res