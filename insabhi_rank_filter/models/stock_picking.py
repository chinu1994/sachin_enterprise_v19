from odoo import models, fields, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    partner_id_domain = fields.Char(
        compute='_compute_partner_id_domain',
        store=False,
    )

    @api.depends('picking_type_code')
    def _compute_partner_id_domain(self):
        for picking in self:
            if picking.picking_type_code == 'outgoing':
                picking.partner_id_domain = "[('customer_rank', '>', 0)]"
            elif picking.picking_type_code == 'incoming':
                picking.partner_id_domain = "[('supplier_rank', '>', 0)]"
            else:
                picking.partner_id_domain = "[]"