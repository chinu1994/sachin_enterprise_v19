from odoo import models, fields

class ResCompany(models.Model):
    _inherit = 'res.company'

    bank_details = fields.Text(string="Bank Details")
