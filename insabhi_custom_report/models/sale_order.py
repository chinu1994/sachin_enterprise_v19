from odoo import models, api, fields, _

class InsabhiDeliveryDays(models.Model):
    _name = "insabhi.delivery.days"

    name = fields.Char('Name')

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    insabhi_term_condition = fields.Html(string="Notes")
    delivery_days = fields.Many2one('insabhi.delivery.days', 'Delivery Days')