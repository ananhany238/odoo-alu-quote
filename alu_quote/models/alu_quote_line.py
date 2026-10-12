from odoo import api, fields, models
from odoo.exceptions import ValidationError


class AluQuoteLine(models.Model):
    _name = "alu.quote.line"
    _description = "Aluminum Profile Quote Line"

    quote_id = fields.Many2one("alu.quote", required=True, ondelete="cascade")
    currency_id = fields.Many2one(related="quote_id.currency_id")
    profile_name = fields.Char(string="Profile", required=True)
    length_m = fields.Float(string="Length (m)", default=1.0)
    quantity = fields.Integer(default=1)
    weight_per_m = fields.Float(string="Weight (kg/m)")
    price_per_kg = fields.Monetary(currency_field="currency_id")
    weight = fields.Float(
        compute="_compute_amounts", store=True, string="Weight (kg)"
    )
    subtotal = fields.Monetary(
        compute="_compute_amounts", store=True, currency_field="currency_id"
    )

    @api.depends("length_m", "quantity", "weight_per_m", "price_per_kg")
    def _compute_amounts(self):
        for line in self:
            line.weight = line.length_m * line.quantity * line.weight_per_m
            line.subtotal = line.weight * line.price_per_kg

    @api.constrains("length_m", "quantity", "weight_per_m", "price_per_kg")
    def _check_positive_values(self):
        for line in self:
            if (
                line.length_m <= 0
                or line.quantity <= 0
                or line.weight_per_m < 0
                or line.price_per_kg < 0
            ):
                raise ValidationError(
                    "Length and quantity must be positive; weight and price cannot be negative."
                )
