from odoo import models, fields

class MaterialUsage(models.Model):
    _name = 'material.usage'
    _description = 'Material Usage Analytics'

    product_id = fields.Many2one('product.product', string="Nguyên liệu")

    today_qty = fields.Float("Hôm nay")
    yesterday_qty = fields.Float("Hôm qua")

    week_qty = fields.Float("7 ngày gần nhất")
    last_week_qty = fields.Float("7 ngày trước")

    month_qty = fields.Float("30 ngày gần nhất")
    last_month_qty = fields.Float("30 ngày trước")

    trend_day = fields.Char("Xu hướng ngày")
    trend_week = fields.Char("Xu hướng tuần")
    trend_month = fields.Char("Xu hướng tháng")