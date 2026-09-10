from odoo import models, api, fields, _
from odoo.exceptions import ValidationError


class InsabhiDeliveryDays(models.Model):
    _name = "insabhi.delivery.days"

    name = fields.Char('Name')

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    insabhi_term_condition = fields.Html(string="Notes")
    delivery_days = fields.Many2one('insabhi.delivery.days', 'Delivery Days')
    bom_restrictions_remove = fields.Boolean(
        string='BoM Restriction Remove',
        default=False,
    )
    @api.model
    def default_get(self, fields):
        res = super(SaleOrder, self).default_get(fields)

        if 'incoterm' in fields:
            res['incoterm'] = self.env.ref('account.incoterm_EXW').id
        if 'incoterm_location' in fields:
            res['incoterm_location'] = 'MUMBAI'

        return res

    def action_confirm(self):
        for order in self:

            # ==========================================================
            # BOM RESTRICTION
            # If "BoM Restriction Remove" is enabled, skip this check.
            # ==========================================================
            if not order.bom_restrictions_remove:

                product_lines = order.order_line.filtered(
                    lambda line: line.product_id and not line.display_type
                )

                missing_bom_lines = product_lines.filtered(
                    lambda line: not line.bom_id
                )

                if missing_bom_lines:
                    products = '\n'.join(
                        f'- {line.product_id.display_name}'
                        for line in missing_bom_lines
                    )

                    raise ValidationError(_(
                        'You cannot confirm this Sale Order.\n\n'
                        'BoM is missing for the following product(s):\n%s'
                    ) % products)

        return super().action_confirm()


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    bom_id = fields.Many2one(
        'mrp.bom',
        string='BoM',
        copy=True,
        check_company=True,
        domain="""
            [
                '|',
                ('product_id', '=', product_id),
                '&',
                ('product_tmpl_id', '=', product_template_id),
                ('product_id', '=', False)
            ]
        """,
        help="Select the BoM to use when creating the Manufacturing Order."
    )

    @api.constrains('product_id', 'bom_id')
    def _check_bom_product(self):
        for line in self:
            if not line.product_id or not line.bom_id:
                continue

            bom = line.bom_id

            # Variant-specific BoM
            if bom.product_id and bom.product_id != line.product_id:
                raise ValidationError(_(
                    'The selected BoM "%(bom)s" does not belong to product "%(product)s".',
                    bom=bom.display_name,
                    product=line.product_id.display_name,
                ))

            # Template BoM
            if bom.product_tmpl_id != line.product_id.product_tmpl_id:
                raise ValidationError(_(
                    'The selected BoM "%(bom)s" does not belong to product "%(product)s".',
                    bom=bom.display_name,
                    product=line.product_id.display_name,
                ))

    def _prepare_procurement_values(self):
        """
        Pass the BoM selected on the Sale Order Line
        to the manufacturing procurement.
        """
        values = super()._prepare_procurement_values()

        self.ensure_one()

        if self.bom_id:
            values['bom_id'] = self.bom_id

        return values


class StockMove(models.Model):
    _inherit = 'stock.move'

    bom_id = fields.Many2one(
        'mrp.bom',
        string='BoM',
        copy=False,
    )

    def _prepare_procurement_values(self):
        values = super()._prepare_procurement_values()

        if self.bom_id:
            values['bom_id'] = self.bom_id

        return values


class StockRule(models.Model):
    _inherit = 'stock.rule'

    def _get_stock_move_values(
        self,
        product_id,
        product_qty,
        product_uom,
        location_dest_id,
        name,
        origin,
        company_id,
        values,
    ):
        move_values = super()._get_stock_move_values(
            product_id,
            product_qty,
            product_uom,
            location_dest_id,
            name,
            origin,
            company_id,
            values,
        )

        if values.get('bom_id'):
            move_values['bom_id'] = values['bom_id'].id

        return move_values





