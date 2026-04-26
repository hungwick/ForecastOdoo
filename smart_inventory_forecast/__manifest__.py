{
    'name': 'Dự báo Nhu cầu & Tối ưu Tồn kho',
    'version': '1.0',
    'category': 'Inventory',
    'summary': 'Hệ thống dự báo nhu cầu nguyên liệu và tối ưu chuỗi cung ứng thông minh',
    'description': """
        Module hỗ trợ dự báo nhu cầu nguyên liệu cho cửa hàng Bánh mì.
        - Phân tích lịch sử bán hàng.
        - Phân rã định mức nguyên liệu (BoM).
        - Dự báo tồn kho và cảnh báo nhập hàng.
    """,
    'author': 'Lương Mạnh Hùng',
    'depends': ['base', 'sale_management', 'stock', 'mrp','purchase'],
    'data': [
        'security/ir.model.access.csv',
        'views/forecast_view.xml',
        'views/product_template_view.xml',
        'views/sales_analytics_view.xml',
        'views/sales_dashboard.xml',
        'views/sales_analytics_chart.xml',
        'views/material_usage_view.xml'
    ],
    'installable': True,
    'application': True,
    "external_dependencies": {
        "python": ["joblib", "pandas"],
    },
}