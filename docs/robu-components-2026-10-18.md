# Robu component listing check — 18 October 2026

Observed on 2026-10-18. Read-only research of Robu public product/category listings for the current selected BOM. No cart, purchase, account change, quotation request or vendor message was submitted. The frozen parts catalogue and its prices have not been replaced.

**Result:** no complete Robu quote for the selected exact BOM was established. Several nearby alternatives have public price evidence, but most exact manufacturer codes did not have an accessible Robu sales listing. “Not found” means not verified in this search, not a claim that Robu cannot source the part. Missing prices and stock are unknown, never zero or “out of stock” by inference.

## Exact selected parts

Quantities below come from `spec/parts.json`. Each unresolved row has unknown Robu SKU, pack/MOQ, price, GST basis and stock unless stated otherwise.

| Catalogue item | Exact selected manufacturer code | Required purchase quantity | Robu result and direct evidence |
| --- | --- | ---: | --- |
| Switch | Kailh CPG1511F01S11-1 / standard BOX Jade |30 switches for28 installed|No exact Robu sales listing found. No Robu price or stock established.|
| Stabilizer | CHERRY G99-0742 |1|No exact Robu sales listing found.|
| Controller kit | Waveshare RP2040-Tiny V1.1 + Adapter + supplied FPC |1 kit|No exact Robu sales listing found. Pimoroni **Tiny2040** is a different board, despite its similar name; it is not the selected remote-USB arrangement.|
| USB adapter | Waveshare RP2040-Tiny-Adapter V1.1 |1, included in kit|No separate exact Robu listing found. Do not add a separate adapter charge to a kit price.|
| FPC cable | Waveshare kit-supplied8-pin, approximately150mm |1, included in kit|No exact standalone Robu cable listing verified. Pin count alone would not establish contact sides, thickness or compatibility.|
| Encoder | Bourns PEC11R-4215F-S0024 |1|No exact Robu sales listing found. Generic EC11 module below is a dimension-changing alternative.|
| White LED | Kingbright APT1608QWF/D |28|No exact Robu sales listing found. Lite-On/generic0603 options below are different parts.|
| White LED driver | Lumissil IS31FL3236-QFLS2-TR |1|No exact Robu sales listing found. No Robu quote established.|
| RGB strip | Adafruit2969, Mini Skinny144pixels/m,1m white PCB |1 reel|No exact Robu sales listing found. The accessible Robu strip below is60pixels/m, not144.|
| Logic buffer | TI SN74AHCT1G125DBVR |1|Robu hosts a [datasheet mentioning the exact code](https://robu.in/wp-content/uploads/2025/02/2410121853_Texas-Instruments-SN74AHCT1G125DBVR_C7484.pdf), but no exact accessible **sales listing** or price/stock was verified. A hosted datasheet is not inventory evidence.|
| Matrix diode | Vishay1N4148W-E3-08 |28|No exact -08 listing verified. Robu lists **1N4148W-E3-18**, a different reel-packaging suffix, below.|
| Magnets | K&J D42, Ø6.35×3.175mm axial N42 |6|No exact Robu sales listing found. A nominal6×3mm generic magnet would change dimensions, retention allowance and provenance. No such alternative is priced here.|
| Feet | 3M SJ5302 /7100006189, Ø7.94×2.2mm |8|No exact Robu sales listing found. No generic rubber pad is assumed equivalent.|
| Screws | RS PRO293-280 M2×6 socket cap |6|No exact RS PRO Robu listing found. An M2×8 button-head pack below changes length/head geometry. An older M2×6 EasyMech result is recorded separately as historical only.|
| Nuts | RS PRO248-4551 M2 DIN934 |6|No exact RS PRO Robu listing found. Bundled generic nuts have not been verified against the selected nut traps.|

## Nearby Robu alternatives — no substitutions made

All these observations were made on2026-10-18. Prices are public listing evidence, not checkout quotations. Category pages sometimes show a price while the product page yields only a navigation shell. That supports the existence of a listing and its displayed category price, but does not verify stock, tax basis, pack quantity or delivery. Older indexed pages are identified separately below.

| Candidate and direct Robu URL | Robu SKU / MPN | Quantity or pack | Visible price and GST basis | Stock evidence | Match and required change |
| --- | --- | --- | --- | --- | --- |
| [Vishay1N4148W-E3-18](https://robu.in/product/1n4148w-e3-18-vishay-1n4148w-e3-18-small-signal-diode-single-100-v-150-ma-1-2-v-4-ns-2-a/) |R194430 /1N4148W-E3-18|Package includes1×diode;28 required|Browser-rendered product listing: **₹8 each inclGST for1–49; ₹7 for50–99; ₹6 for100+**. **28×₹8=₹224 inclGST**, before delivery. This supersedes the category₹6 figure for our quantity.|**In Stock**, visible in rendered browser UI on2026-10-18|**Packaging-code alternative.** Selected -08 and listed -18 are both Vishay1N4148W SOD-123 variants. Different reel-packaging suffix; no automatic replacement. ₹224 is a dated listing estimate, not a formal quotation.|
| [Lite-On LTW-C191UC5 white0603 LED](https://robu.in/product/ltw-c191uc5-lite-on-5ma-yellow-lens-20%E2%84%8380%E2%84%83-white-130-72mw-0603-led-indication-discrete-rohs/) |R250624 /LTW-C191UC5|Product evidence says one part, cut tape; reel5000 is a reel tier, not required purchase quantity|Current [SMD category](https://robu.in/product-category/smd-led/) displays₹4.46, GST basis not shown. A **much older product response** says₹7 inclGST for1–9 and₹6 for10–4999. Conflicting snapshots; **no single current quote established**.|Older product response says in stock; current stock not verified|**Different LED.** Same0603 size class does not establish selected0.75mm height, land pattern, polarity, tint, brightness/current or optical fit. Needs datasheet/PCB/optical review.|
| [TI SN74AHCT1G125DCKR](https://robu.in/product/sn74ahct1g125dckr-texas-instruments-8ma-1-4-5v5-5v-8ma-1-sc-70-5-buffers-drivers-receivers-transceivers-rohs/) |Robu SKU unavailable; MPN given in listing title|Unknown|Price and tax unknown; product page returned navigation only|Unknown|**Package-changing alternative.** DCK/SC-70-5 differs from selected DBV/SOT-23-5; PCB footprint/model would change.|
| [EC11 Rotary Encoder Module with Knob Cap](https://robu.in/product/EC11%20Rotary%20Encoder%20Module%20with%20Knob%20Cap%20for%20Development%20Boards/) |Robu SKU/manufacturer code unavailable|One module implied by title; package contents not verified|₹99 in [current encoder category](https://robu.in/product-category/rotary-encoder/); GST basis not displayed there|Unknown; product page returned navigation only|**Dimension-changing module.** Not the exact Bourns bare encoder; breakout board, pin layout, shaft and knob are not verified compatible.|
| [1m WS2812B5V60LED/m non-waterproof strip](https://robu.in/product/1m-ws2812b-5v-addressable-rgb-non-waterproof-led-strip-light-60leds-m/) |Robu SKU/manufacturer code unavailable|1m,60pixels/m from title|₹489 in [current strip category](https://robu.in/product-category/rgb-led-strip/); GST basis not displayed there|Unknown; product page returned navigation only|**Dimension/lighting-changing alternative.** Pitch≈16.67mm versus selected≈6.94mm. Fourteen pixels would occupy≈233mm rather than≈97mm, so it cannot replace the modelled segment unchanged. Width, thickness and electrical behaviour require review.|
| [M2×8 SS304 button-head screws,10pcs](https://robu.in/product/m2-x-8mm-socket-button-head-cap-allen-ss-304-screw-dia-2mm-length-8mm-10-pcs/) |Robu SKU unavailable|10 screws from title; nuts not included by verified evidence|₹74 per listed pack in [current screw category](https://robu.in/product-category/socket-head-cap-screw-allen-bolt/); GST basis not displayed there|Unknown; product page returned navigation only|**Dimension-changing alternative.** Selected screw is6mm socket cap; this is8mm button head. Counterbore, thread engagement and interference need revision; no assumed nut equivalence.|

The diode-only listing estimate is₹224 inclGST for28 units, before delivery. No combined alternative total is calculated: the candidates are neither mutually verified nor a complete compatible set. Shipping, tax where unspecified, MOQ rounding, lead time and destination delivery remain unquoted.

## Historical leads excluded from current quotes

These leads appeared in older indexed Robu pages, not a current detailed product response. They can guide a later Robu lookup, but must not be promoted into current prices or stock:

- EasyMech M2×6 socket-cap bolt/nut set, Robu SKU56219: older Robu category evidence showed₹224 inclGST and “12pcs.” The current clean category redirected to the new catalogue, where this specific item was not visible in the retrieved results. Exact count of bolts versus nuts, current product URL/stock and price remain unverified. Its stated3.7mm head diameter also differs from the selected nominal3.8mm RS PRO reference.
- [Generic0603 white LED listing](https://robu.in/product/0603-surface-mount-led-white-50pcs/), Robu SKU827882: older category evidence showed₹2 inclGST. The URL retains “50pcs,” while a newer category title omitted a pack quantity; current product response exposed no details. Price basis and pack size are unresolved, so neither₹56 for28 nor₹2 per50-pack is justified.

## Evidence limits and next quote inputs

Searches covered exact manufacturer codes plus the current Robu diode, LED, encoder, strip and socket-screw categories. Robu search URLs were inaccessible through the web reader; several product pages returned only the navigation/footer, and a public HTML fetch received HTTP403. No protected endpoint or account was used. Search snippets, old indexed responses and current category responses are distinguished above rather than merged into an invented current stock/price assertion. Subsequent browser UI verification fully loaded the Vishay diode page after JavaScript rendered it; that current detailed price, quantity tiers, stock and SKU supersede the sparse web-reader/category evidence for that row.

An exact Robu quote still needs their response or an accessible detailed listing for the selected codes, purchase quantities and pack sizes. Provide the exact BOM above, ask whether the Tiny kit includes the same V1.1 adapter/FPC, request cut-tape quantities for28 LEDs/diodes and1 IC of each type, and ask separately about exact versus proposed alternatives. Any approved substitution must be checked against the frozen geometry before replacing its source or cost record.

Custom case, plate, caps, legend finishing, knob, risers, overlay, PCB fabrication/assembly and support passives are outside this component-listing check. The existing₹1,353.30 known subtotal comes from other suppliers and remains separate; it is not a Robu quotation or a complete project price.
