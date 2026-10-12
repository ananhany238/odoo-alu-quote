# Aluminum Profile Quotes (Odoo 17)

A small custom Odoo module for quoting aluminum profile jobs. Each quote has
profile lines (length, quantity, weight per metre, price per kg); weight and
subtotals are computed automatically.

## What it demonstrates
- Models, computed stored fields, `@api.constrains`, and a draft/confirmed/cancelled workflow
- XML views (list, form, search), menus and actions
- Access rules (`ir.model.access.csv`)
- A QWeb PDF report
- Unit tests with `TransactionCase`

## Run it
```bash
# with an Odoo 17 checkout and PostgreSQL available
./odoo-bin -d alu_test --addons-path=addons,/path/to/odoo-alu-quote -i alu_quote --test-enable --stop-after-init
```
Then start Odoo normally, open **Alu Quotes > Quotes**, and create a quote.

## Notes
- Targets Odoo 17. In Odoo 18+ list views use `<list>` instead of `<tree>`, and view modifiers
  are written the same `invisible="..."` way, so porting is mostly that rename.

## Possible next steps
- Auto-numbering with `ir.sequence`
- Link to `res.partner` contact history and `sale.order`
- Excel export with `xlsxwriter`
