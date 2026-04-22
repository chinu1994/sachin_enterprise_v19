from odoo import models, api, _
from odoo.exceptions import UserError


ALLOWED_FIELDS = ['lst_price', 'list_price', 'standard_price']


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.model
    def create(self, vals):
        if self.env.user.has_group('insabhi_product_access.group_product_price_only'):
            raise UserError(_("You are not allowed to create products."))
        return super().create(vals)

    def write(self, vals):
        if self.env.user.has_group('insabhi_product_access.group_product_price_only'):
            for field in vals:
                if field not in ALLOWED_FIELDS:
                    raise UserError(_("You can only modify Sales Price and Cost."))
        return super().write(vals)


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.model
    def create(self, vals):
        if self.env.user.has_group('insabhi_product_access.group_product_price_only'):
            raise UserError(_("You are not allowed to create product variants."))
        return super().create(vals)

    def write(self, vals):
        if self.env.user.has_group('insabhi_product_access.group_product_price_only'):
            for field in vals:
                if field not in ALLOWED_FIELDS:
                    raise UserError(_("You can only modify Sales Price and Cost."))
        return super().write(vals)