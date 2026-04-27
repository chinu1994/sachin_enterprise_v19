from odoo import models, fields, api,_

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    insabhi_note = fields.Html(string="Default Terms & Conditions")
