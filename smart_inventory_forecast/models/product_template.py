from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    qty_nhom_a = fields.Float(string='Qty Nhóm A', default=0.0)
    qty_nhom_b = fields.Float(string='Qty Nhóm B', default=0.0)
    qty_nhom_c = fields.Float(string='Qty Nhóm C', default=0.0)

    ai_safety_stock = fields.Float(string='Safety Stock', default=0.0)

    is_perishable = fields.Boolean(string='Hàng tươi (không lưu kho)')

    package_size = fields.Float(string="Quy cách đóng gói", default=1.0)