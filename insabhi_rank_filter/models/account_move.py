from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    partner_id_domain = fields.Char(
        compute='_compute_partner_id_domain',
        store=False,
    )

    @api.depends('move_type')
    def _compute_partner_id_domain(self):
        for move in self:
            if move.move_type in ('out_invoice', 'out_refund'):
                move.partner_id_domain = "[('customer_rank', '>', 0)]"
            elif move.move_type in ('in_invoice', 'in_refund'):
                move.partner_id_domain = "[('supplier_rank', '>', 0)]"
            else:
                move.partner_id_domain = "[]"