# Copyright 2016 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models

RENTAL_TIMELINE_VIEW = ("rental_timeline", "Rental Timeline")


class IrUIView(models.Model):
    _inherit = "ir.ui.view"

    type = fields.Selection(selection_add=[RENTAL_TIMELINE_VIEW])
