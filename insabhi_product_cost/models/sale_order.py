# -*- coding: utf-8 -*-

from odoo import models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        # Call original behavior
        res = super(SaleOrder, self)._onchange_partner_id()

        # Recompute taxes on all order lines
        for order in self:
            if order.order_line:
                order.order_line._compute_tax_ids()

        return res