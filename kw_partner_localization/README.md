# Kuwait Partner Localization (Odoo 16)

Extends partners, sales, and website checkout to capture Kuwait-specific address data (areas, blocks, PACI, map links) and surface it in back-office forms and reports.

## Features
- New `area` model linked to Kuwait states/governorates; menu under Contacts → Localization.
- Partner address extensions: area, block, avenue, building number, additional info, floor, flat, PACI number, Google Map, Kuwait Finder links.
- Sale orders inherit the partner fields as related readonly values for quick reference and search.
- Website checkout restricted to Kuwait (`KW`) with required state/area/building data; area dropdown filters by selected state.
- Sale order and delivery reports print the Kuwait address details.

## Requirements
- Odoo 16.0 with modules: `base`, `contacts`, `sale`, `website_sale`.

## Installation
1. Place this module in your Odoo addons path (e.g., `addons/kw_partner_localization`).
2. Update the app list and install **Kuwait Partner Localization** from Apps, or install via CLI:
   - `./odoo-bin -c <config> -d <database> -i kw_partner_localization`

## Configuration
- Define Areas: Contacts → Configuration → Localization → Area. Each area must be linked to a state.
- Assign address details on partners; sale orders will mirror these fields automatically.
- Website: ensure the website uses this checkout (module depends on `website_sale`). Customers must choose state and area; ZIP/City are hidden/optional.

## Usage Notes
- Checkout JS (`static/src/js/website_sale.js`) loads areas based on the selected state and toggles optional PACI/map link fields.
- Mandatory billing fields are adjusted to require state, area, and building info instead of ZIP/City.
- Reports (`report/sale_order_report.xml`) include the Kuwait address blocks for quotations, orders, and deliveries.

## Access Rights
- Group `Create / Edit Area` controls who can manage areas.
- Model access for `area` is granted for read/create/write/unlink via `security/ir.model.access.csv`.