# Lighting options

Research date: 2026-10-18. Preliminary planning evidence for the 28-key keypad; not a shopping list, supplier quote or validated circuit.

## Per-key lighting

Both white LEDs with a suitable PWM driver and addressable RGB LEDs support individual brightness and animated effects. White does not inherently mean fixed brightness or fewer effects.

| Approach | Supplier evidence | Parts-only illustration for 28 keys |
| --- | --- | --- |
| Ordinary white LEDs + external driver | Robu generic 0805 white listed around ₹2 each; fresh stock not confirmed. DigiKey India lists an IS31FL3731 QFN driver around ₹154 at quantity one. | Around ₹210 for LEDs and driver; optical placement and assembly unresolved. |
| Reverse-mount white LEDs + external driver | Robu LTW-C230DS category listed ₹14; an older product snapshot showed ₹12 at quantity 10+. Conflicting snapshots require a checkout recheck. | Around ₹490–546 including the illustrative driver. |
| Addressable RGB | Robu WorldSemi WS2812B-2020 listed ₹8; XINGLIGHT compatible listed ₹9 at quantity 10+. The latter search snapshot said in stock. | Around ₹224–252 for LEDs, with drivers integrated. |
| Addressable RGBW | Suitable small-quantity, keyboard-compatible sourcing remains unresolved. An Indian listing for SK6812 3535 neutral-white showed ₹127.40 each at a 100-piece tier. | No useful 28-piece quote established. |

These examples do not establish comparable brightness or mechanical fit. Ordinary top-emitting 0805/2020 parts are not substitutes for a reverse-mount keyboard LED without changing placement. Switch housing, LED opening, keycap legend position and PCB footprint must be checked together. No stocked Indian MINI-E source was verified.

Primary supplier links:

- [Robu SMD LED catalogue](https://robu.in/product-category/smd-led/)
- [Robu LTW-C230DS reverse-mount white LED](https://robu.in/product/ltw-c230ds-lite-on-20ma-315mcd-yellow-lens-reverse-mount-30%E2%84%8385%E2%84%83-white-130-72mw-3-2v-1206-led-indication-discrete-rohs/)
- [DigiKey India IS31FL3731-QFLS2-TR](https://www.digikey.in/en/products/detail/lumissil-microsystems/IS31FL3731-QFLS2-TR/4286473)
- [Robu RGB catalogue](https://robu.in/product-category/rgb-led/)
- [Robu XINGLIGHT WS2812B-compatible 2020 LED](https://robu.in/product/1-month-warranty-953/)
- [LionCircuits SK6812 3535 RGBW listing](https://www.lioncircuits.com/parts/S35354RGBWSK6812MINID001)

Robu product pages sometimes returned only an empty product shell. Prices and availability above combine accessible listings and indexed product snapshots; recheck exact quantities, taxes and stock before ordering.

## Circuit and firmware trade-offs

- **White:** a separate driver, its support circuit and LED matrix routing are needed. QMK LED Matrix supports IS31FL3731 and individual brightness. The quoted QFN driver is difficult to hand-solder; package and assembly method need a deliberate choice.
- **RGB:** each pixel integrates its driver, simplifying control to a serial chain with power and ground. Tiny LED packages remain an assembly challenge. Mixed RGB white can vary in tint.
- **RGBW:** adds a dedicated white emitter. QMK supports RGBW conversion through its WS2812 driver, but package, sourcing and firmware configuration still need verification.

Sources: [QMK LED Matrix](https://docs.qmk.fm/features/led_matrix), [IS31FL3731 driver](https://docs.qmk.fm/drivers/is31fl3731), [WS2812/RGBW driver](https://docs.qmk.fm/drivers/ws2812).

## Diffused side lighting

[Robu's 1 m, 60 LED/m, 5 V WS2812B strip](https://robu.in/product/1m-ws2812b-5v-addressable-rgb-non-waterproof-led-strip-light-60leds-m/) was listed around ₹489 including GST, with Add to Cart in a recent catalogue snapshot; live product stock was not confirmed. Budget the full purchased metre even if only a short section is used. A 20–30 cm section contains approximately 12–18 pixels.

The enclosure needs a diffuser channel, LED clearance and a light-blocking arrangement. USB power allocation and firmware brightness limits must cover both key lighting and ambient lighting. Strip length and diffusion quality remain prototype decisions.

## Printable shine-through keycaps

- [Keycap Legend Generator](https://github.com/arylise/keycap-generator): browser workflow, MX-style stems, sizes including 2u, transparent legend/stem option, two-part 3MF. Author recommends top-face-down printing. The 2u option is not explicitly documented as a convex spacebar. Code/models use CC BY-NC-ND 4.0; do not assume unrestricted modification or redistribution rights. [Live generator](https://vostoklabs.github.io/SVG-keycap-generator/).
- [Keycap Playground](https://github.com/riskable/keycap_playground): configurable OpenSCAD keycaps, Cherry stems, separate transparent legends/stems, adjustable length and inverted dish for spacebars. Source includes stabilizer locations at ±12 mm for 2u keys. Author recommends side printing with removable stem supports and notes fit problems with upright stems printed using a 0.4 mm nozzle.

Print and test **one 1u cap first** using the intended printer, material, switch and LED. Check stem fit, strength, feel, light leakage and legend readability. Then test the 2u Space with the chosen stabilizer before printing the set.

[Robu Services](https://robu.in/services/) may be a route for outsourced samples, but service availability, transparent/navy material options and a price for our actual files have not been verified here. Obtain a quote after supplying the sample geometry, material and colour requirements; do not assume transparent filament or two-material printing is available.

## Cost boundary

All illustrative subtotals exclude PCB fabrication, assembly, passives, any required level conversion, connectors, wiring, diffuser printing/material, keycap printing, tooling, failed samples, shipping and supplier taxes not explicitly included. They are not a total project estimate. Select the optical and assembly approach before requesting a final BOM and prototype quote.
