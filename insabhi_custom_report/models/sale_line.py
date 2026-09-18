from odoo import models, api, fields, _
from odoo.exceptions import ValidationError

class SaleOrderLines(models.Model):
    _inherit = 'sale.order.line'

    bom_id = fields.Many2one(
        'mrp.bom',
        string='BoM',
        copy=True,
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
