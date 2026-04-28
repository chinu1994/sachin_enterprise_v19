from odoo import models, fields, api,_

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    insabhi_note = fields.Html(string="Default Terms & Conditions")

    def set_values(self):
        super().set_values()
        self.env['ir.config_parameter'].set_param(
            'insabhi.insabhi_note',
            self.insabhi_note or ''
        )

    @api.model
    def get_values(self):
        res = super().get_values()
        res.update(
            insabhi_note=self.env['ir.config_parameter'].sudo().get_param(
                'insabhi.insabhi_note', default=''
            )
        )
        return res
