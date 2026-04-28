from odoo import models, api, fields, _
class SaleOrder(models.Model):
    _inherit = 'sale.order'

    insabhi_term_condition = fields.Html(string="Notes")