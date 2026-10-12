from odoo import api, fields, models
from odoo.exceptions import UserError


class AluQuote(models.Model):
    _name = "alu.quote"
    _description = "Aluminum Profile Quote"
    _order = "date desc, id desc"

    name = fields.Char(string="Reference", required=True, copy=False)
    partner_id = fields.Many2one("res.partner", string="Customer", required=True)
    date = fields.Date(default=fields.Date.context_today)
    state = fields.Selection(
        [("draft", "Draft"), ("confirmed", "Confirmed"), ("cancelled", "Cancelled")],
        default="draft",
        required=True,
    )
    currency_id = fields.Many2one(
        "res.currency", default=lambda self: self.env.company.currency_id
    )
    line_ids = fields.One2many("alu.quote.line", "quote_id", string="Profiles")
    total_weight = fields.Float(
        compute="_compute_totals", store=True, string="Total Weight (kg)"
    )
    total_amount = fields.Monetary(
        compute="_compute_totals", store=True, currency_field="currency_id"
    )

    @api.depends("line_ids.weight", "line_ids.subtotal")
    def _compute_totals(self):
        for quote in self:
            quote.total_weight = sum(quote.line_ids.mapped("weight"))
            quote.total_amount = sum(quote.line_ids.mapped("subtotal"))

    def action_confirm(self):
        for quote in self:
            if not quote.line_ids:
                raise UserError("Add at least one profile line before confirming.")
            quote.state = "confirmed"

    def action_cancel(self):
        self.write({"state": "cancelled"})

    def action_draft(self):
        self.write({"state": "draft"})
