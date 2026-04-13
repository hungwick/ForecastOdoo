from odoo import models, fields


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    is_ai_generated = fields.Boolean(string='AI Generated', default=False, readonly=True)
    forecast_id = fields.Many2one('smart.forecast', string='Forecast Ref', readonly=True)

