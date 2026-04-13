from odoo import models, fields, api, exceptions
import os
import joblib
from odoo.modules.module import get_module_path


class SmartForecast(models.Model):
    _name = 'smart.forecast'
    _description = 'AI Demand Forecast System'

    name = fields.Char(default='New', readonly=True)
    product_id = fields.Many2one('product.product', required=True)
    forecast_date = fields.Date(default=fields.Date.context_today, required=True)

    predicted_qty = fields.Selection([
        ('Nhom_A', 'Low'),
        ('Nhom_B', 'Medium'),
        ('Nhom_C', 'High')
    ], readonly=True)

    current_stock = fields.Float(readonly=True)
    suggested_qty = fields.Float(readonly=True)
    adjusted_qty = fields.Float()

    purchase_order_id = fields.Many2one('purchase.order', readonly=True)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Forecasted'),
        ('po_created', 'PO Created')
    ], default='draft')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = 'FORECAST/' + fields.Datetime.now().strftime('%Y%m%d%H%M%S')
        return super().create(vals_list)

    def action_run_forecast(self):
        module_path = get_module_path('smart_inventory_forecast')
        model_path = os.path.join(module_path, 'data', 'ai_model_universal.pkl')

        try:
            model = joblib.load(model_path)
        except Exception as e:
            raise exceptions.UserError(f"Cannot load AI model: {str(e)}")

        for record in self:
            product = record.product_id
            template = product.product_tmpl_id

            # ===== FEATURE =====
            thu = record.forecast_date.weekday()
            thang = record.forecast_date.month
            cuoi_tuan = 1 if thu == 6 else 0

            try:
                # ===== PREDICT =====
                prediction = model.predict([[thu, thang, cuoi_tuan]])
                predicted_class = str(prediction[0])
                record.predicted_qty = predicted_class

                # ===== STOCK =====
                stock_on_hand = product.qty_available

                if template.is_perishable:
                    stock_on_hand = 0.0

                record.current_stock = stock_on_hand

                import math

                # ===== BASE DEMAND =====
                if predicted_class == 'Nhom_C':
                    base_qty = template.qty_nhom_c
                elif predicted_class == 'Nhom_B':
                    base_qty = template.qty_nhom_b
                else:
                    base_qty = template.qty_nhom_a

                # ===== SAFETY =====
                safety_stock = template.ai_safety_stock

                # ===== STOCK =====
                stock_on_hand = product.qty_available

                if template.is_perishable:
                    stock_on_hand = 0.0

                record.current_stock = stock_on_hand

                # ===== NET REQUIREMENT =====
                required_qty = base_qty + safety_stock - stock_on_hand
                required_qty = max(required_qty, 0.0)

                # ===== PACKAGE ROUNDING =====
                package_size = template.package_size or 1.0

                if required_qty > 0:
                    order_qty = math.ceil(required_qty / package_size) * package_size
                else:
                    order_qty = 0.0

                # ===== FINAL =====
                record.suggested_qty = order_qty
                record.adjusted_qty = order_qty

                # ===== CHỐNG NHẬP DƯ =====
                if stock_on_hand >= (base_qty + safety_stock):
                    record.suggested_qty = 0
                    record.adjusted_qty = 0
                record.state = 'done'

            except Exception as e:
                raise exceptions.UserError(f"AI error: {str(e)}")


    def action_create_po(self):
        for record in self:
            if record.adjusted_qty <= 0:
                raise exceptions.UserError("Quantity must be > 0")

            seller = record.product_id.seller_ids and record.product_id.seller_ids[0].partner_id
            if not seller:
                raise exceptions.UserError("No vendor found")

            po_vals = {
                'partner_id': seller.id,
                'is_ai_generated': True,
                'forecast_id': record.id,
                'order_line': [(0, 0, {
                    'product_id': record.product_id.id,
                    'name': record.product_id.name,
                    'product_qty': record.adjusted_qty,
                    'product_uom_id': record.product_id.uom_id.id,
                    'price_unit': record.product_id.standard_price or 1.0,
                    'date_planned': fields.Datetime.now(),
                })]
            }

            po = self.env['purchase.order'].create(po_vals)
            record.purchase_order_id = po.id
            record.state = 'po_created'

    # ==============================
    # VIEW PO
    # ==============================
    def action_view_purchase_order(self):
        self.ensure_one()

        if not self.purchase_order_id:
            raise exceptions.UserError("Chưa có đơn mua!")

        return {
            'name': 'Đơn Mua Hàng',
            'type': 'ir.actions.act_window',
            'res_model': 'purchase.order',
            'view_mode': 'form',
            'res_id': self.purchase_order_id.id,
        }