from odoo.exceptions import UserError, ValidationError
from odoo.tests.common import TransactionCase


class TestAluQuote(TransactionCase):
    def setUp(self):
        super().setUp()
        self.partner = self.env["res.partner"].create({"name": "Test Customer"})
        self.quote = self.env["alu.quote"].create(
            {"name": "Q-001", "partner_id": self.partner.id}
        )

    def _add_line(self, **vals):
        defaults = {
            "quote_id": self.quote.id,
            "profile_name": "Window frame 40x40",
            "length_m": 6.0,
            "quantity": 10,
            "weight_per_m": 0.5,
            "price_per_kg": 100.0,
        }
        defaults.update(vals)
        return self.env["alu.quote.line"].create(defaults)

    def test_line_and_quote_totals(self):
        line = self._add_line()
        # 6 m * 10 pcs * 0.5 kg/m = 30 kg; 30 kg * 100 = 3000
        self.assertAlmostEqual(line.weight, 30.0)
        self.assertAlmostEqual(line.subtotal, 3000.0)
        self._add_line(length_m=3.0, quantity=2, weight_per_m=1.0, price_per_kg=50.0)
        self.assertAlmostEqual(self.quote.total_weight, 36.0)
        self.assertAlmostEqual(self.quote.total_amount, 3300.0)

    def test_confirm_requires_lines(self):
        with self.assertRaises(UserError):
            self.quote.action_confirm()
        self._add_line()
        self.quote.action_confirm()
        self.assertEqual(self.quote.state, "confirmed")

    def test_invalid_quantity_rejected(self):
        with self.assertRaises(ValidationError):
            self._add_line(quantity=0)
