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
        states={},
        copy=True,
    )

    def action_increment_lebel(self):
        for rec in self:
            self.env.cr.execute(
                "UPDATE account_move_line SET no_of_lebel = no_of_lebel + 1 WHERE id = %s",
                (rec.id,)
            )
            rec.invalidate_recordset(['no_of_lebel'])

    def action_decrement_lebel(self):
        for rec in self:
            if rec.no_of_lebel > 0:
                self.env.cr.execute(
                    "UPDATE account_move_line SET no_of_lebel = no_of_lebel - 1 WHERE id = %s",
                    (rec.id,)
                )
                rec.invalidate_recordset(['no_of_lebel'])

