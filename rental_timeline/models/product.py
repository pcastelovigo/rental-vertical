# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    product_timeline_ids = fields.One2many(
        "product.timeline",
        "product_id",
        "Time Lines",
    )
