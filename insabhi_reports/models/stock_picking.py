from odoo import models, fields

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    job_sheet_no = fields.Char(string="Job Sheet No.")
    box_no = fields.Char(string="Box No.")
    total_box = fields.Char(string="Total Box")
    box_type = fields.Char(string="Box Type")
    box_size = fields.Char(string='Box Size')