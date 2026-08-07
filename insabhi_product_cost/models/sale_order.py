# -*- coding: utf-8 -*-

from odoo import models, api, _
from odoo.exceptions import AccessError


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

    def unlink(self):
        if not self.env.user.has_group('insabhi_product_cost.group_sale_order_delete'):
            raise AccessError(_(
                "You do not have the necessary permissions to delete Sale Orders. Please contact your administrator for access."
            ))
        return super().unlink()