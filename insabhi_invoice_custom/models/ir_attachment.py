from odoo import models


class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    def unlink(self):
        moves = self.env['account.move'].search([
            '|', '|',
            ('insabhi_packing_list_doc_ids', 'in', self.ids),
            ('insabhi_LR_copy_doc_ids', 'in', self.ids),
            ('insabhi_MTC_doc_ids', 'in', self.ids),
        ])

        for move in moves:
            move.write({
                'insabhi_packing_list_doc_ids': [(3, att.id) for att in self],
                'insabhi_LR_copy_doc_ids': [(3, att.id) for att in self],
                'insabhi_MTC_doc_ids': [(3, att.id) for att in self],
            })

        return super().unlink()