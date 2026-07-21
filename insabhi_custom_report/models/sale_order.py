from odoo import models, api, fields, _

class InsabhiDeliveryDays(models.Model):
    _name = "insabhi.delivery.days"

    name = fields.Char('Name')

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    insabhi_term_condition = fields.Html(string="Notes")
    delivery_days = fields.Many2one('insabhi.delivery.days', 'Delivery Days')

    @api.model
    def default_get(self, fields):
        res = super(SaleOrder, self).default_get(fields)

        if 'incoterm' in fields:
            res['incoterm'] = self.env.ref('account.incoterm_EXW').id
        if 'incoterm_location' in fields:
            res['incoterm_location'] = 'MUMBAI'

        return res