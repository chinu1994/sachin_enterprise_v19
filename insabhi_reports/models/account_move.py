from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = 'account.move'

    po_no = fields.Char(string="PO No")
    manufacturing_no = fields.Char(string="Manufacturing No", compute="_compute_manufacturing_no")

    def _compute_manufacturing_no(self):
        for rec in self:
            mo_name = False
            sale_orders = rec.invoice_line_ids.mapped('sale_line_ids.order_id')
            mos = self.env['mrp.production'].search([
                ('origin', 'in', sale_orders.mapped('name'))
            ], limit=1)

            if mos:
                mo_name = mos.name

            rec.manufacturing_no = mo_name


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    no_of_lebel = fields.Integer(
        string='No of Label',
        default=0,
    )