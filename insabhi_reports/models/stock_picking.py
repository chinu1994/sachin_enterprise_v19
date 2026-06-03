from odoo import models, fields

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    job_sheet_no = fields.Char(string="Job Sheet No.")
    box_no = fields.Char(string="Box No.")
    total_box = fields.Char(string="Total Box")
    box_type = fields.Char(string="Box Type")
    box_size = fields.Char(string='Box Size')
    po_no = fields.Char(string="PO No", compute="_compute_po_no")

    def _compute_po_no(self):
        for rec in self:
            invoice = rec.sale_id.invoice_ids.filtered(lambda inv: inv.po_no)[:1]
            rec.po_no = invoice.po_no if invoice else False