from odoo import models, fields, api
from datetime import date, timedelta, datetime
from datetime import datetime, time
import pytz

class SalesAnalytics(models.Model):
    _name = 'sales.analytics'
    _description = 'Sales Analytics'

    product_id = fields.Many2one('product.product', string="Sản phẩm")

    today_qty = fields.Float("Hôm nay")
    yesterday_qty = fields.Float("Hôm qua")

    week_qty = fields.Float("7 ngày gần nhất")
    last_week_qty = fields.Float("7 ngày trước đó")

    month_qty = fields.Float("30 ngày gần nhất")
    last_month_qty = fields.Float("30 ngày trước đó")

    trend_day = fields.Char("Xu hướng ngày")
    trend_week = fields.Char("Xu hướng tuần")
    trend_month = fields.Char("Xu hướng tháng")



    def _get_sales_qty(self, date_from, date_to, product):
        # timezone user (VN)
        tz = pytz.timezone(self.env.user.tz or 'UTC')

        # đầu ngày (00:00:00)
        start = tz.localize(datetime.combine(date_from, time.min)).astimezone(pytz.utc)

        # cuối ngày (23:59:59)
        end = tz.localize(datetime.combine(date_to, time.max)).astimezone(pytz.utc)

        lines = self.env['sale.order.line'].search([
            ('product_id', '=', product.id),
            ('order_id.state', '=', 'sale'),
            ('order_id.date_order', '>=', start),
            ('order_id.date_order', '<=', end),
        ])

        return sum(lines.mapped('product_uom_qty'))

    def compute_analytics(self):
        today = date.today()

        products = self.env['product.product'].search([
            #('sale_ok', '=', True),
            ('bom_ids', '!=', False)
        ])

        material_usage = {}

        for product in products:
            record = self.search([('product_id', '=', product.id)], limit=1)
            if not record:
                record = self.create({'product_id': product.id})

            # ===== DAY =====
            today_qty = self._get_sales_qty(today, today + timedelta(days=1), product)

            yesterday_qty = self._get_sales_qty(
                today - timedelta(days=1),
                today,
                product
            )

            # ===== WEEK =====
            week_qty = self._get_sales_qty(
                today - timedelta(days=7),
                today + timedelta(days=1),
                product
            )

            last_week_qty = self._get_sales_qty(
                today - timedelta(days=14),
                today - timedelta(days=7),
                product
            )

            # ===== MONTH =====
            month_qty = self._get_sales_qty(
                today - timedelta(days=30),
                today + timedelta(days=1),
                product
            )

            last_month_qty = self._get_sales_qty(
                today - timedelta(days=60),
                today - timedelta(days=30),
                product
            )

            record.write({
                'today_qty': today_qty,
                'yesterday_qty': yesterday_qty,
                'week_qty': week_qty,
                'last_week_qty': last_week_qty,
                'month_qty': month_qty,
                'last_month_qty': last_month_qty,
                'trend_day': self._calc_trend(today_qty, yesterday_qty),
                'trend_week': self._calc_trend(week_qty, last_week_qty),
                'trend_month': self._calc_trend(month_qty, last_month_qty),
            })

            today_bom = self._compute_bom_consumption(product, today_qty)
            yesterday_bom = self._compute_bom_consumption(product, yesterday_qty)

            week_bom = self._compute_bom_consumption(product, week_qty)
            last_week_bom = self._compute_bom_consumption(product, last_week_qty)

            month_bom = self._compute_bom_consumption(product, month_qty)
            last_month_bom = self._compute_bom_consumption(product, last_month_qty)

            for mat_id in set(list(today_bom.keys()) + list(month_bom.keys())):
                if mat_id not in material_usage:
                    material_usage[mat_id] = {
                        'today': 0,
                        'yesterday': 0,
                        'week': 0,
                        'last_week': 0,
                        'month': 0,
                        'last_month': 0,
                    }

                material_usage[mat_id]['today'] += today_bom.get(mat_id, 0)
                material_usage[mat_id]['yesterday'] += yesterday_bom.get(mat_id, 0)

                material_usage[mat_id]['week'] += week_bom.get(mat_id, 0)
                material_usage[mat_id]['last_week'] += last_week_bom.get(mat_id, 0)

                material_usage[mat_id]['month'] += month_bom.get(mat_id, 0)
                material_usage[mat_id]['last_month'] += last_month_bom.get(mat_id, 0)

        # ===== SAVE MATERIAL USAGE =====
        self.env['material.usage'].search([]).unlink()

        for mat_id, data in material_usage.items():
            self.env['material.usage'].create({
                'product_id': mat_id,

                'today_qty': data['today'],
                'yesterday_qty': data['yesterday'],

                'week_qty': data['week'],
                'last_week_qty': data['last_week'],

                'month_qty': data['month'],
                'last_month_qty': data['last_month'],

                'trend_day': self._calc_trend(data['today'], data['yesterday']),
                'trend_week': self._calc_trend(data['week'], data['last_week']),
                'trend_month': self._calc_trend(data['month'], data['last_month']),
            })

    def _calc_trend(self, current, previous):
        if previous == 0:
            if current > 0:
                return "Tăng mới"
            return "Không có dữ liệu"
        change = (current - previous) / previous * 100

        if change > 10:
            return f"Tăng mạnh (+{round(change,1)}%)"
        elif change > 0:
            return f"Tăng (+{round(change,1)}%)"
        elif change < -10:
            return f"Giảm mạnh ({round(change,1)}%)"
        elif change < 0:
            return f"Giảm ({round(change,1)}%)"
        else:
            return "Ổn định"

    def _compute_bom_consumption(self, product, qty):
        result = {}

        bom = self.env['mrp.bom'].search([
            ('product_tmpl_id', '=', product.product_tmpl_id.id)
        ], limit=1)

        if not bom:
            return result

        for line in bom.bom_line_ids:
            material = line.product_id
            required_qty = line.product_qty * qty

            result[material.id] = result.get(material.id, 0) + required_qty

        return result

