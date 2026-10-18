# Robu quote check — 18 October 2026

This procurement check is separate from the frozen fit-v1 geometry and its historical priced subtotal. A listed price, an automatic model estimate and a supplier-reviewed quotation are different evidence. No order or payment is authorized.

## Current one-riser budget

Budget one 4° bar provisionally: lower case ₹3,159 + knob ₹252 + riser ₹1,087 = **₹4,498 including GST**, before delivery, finishes and all other parts. The 7° bar replaces it if selected, making the same three-body subset ₹5,346. The four-upload total ₹6,433 below is preserved quotation evidence, not the current purchasing scope.

One build needs four magnets (two case/two bar) and six feet (four case/two bar), plus six screws and six nuts. Positive magnet closures and USB clamps remain separate unquoted custom pieces. See the [full-keyboard cost audit](full-keyboard-cost-audit.md) for every remaining group.

## Current results

- Exact purchased parts: see [component listing check](robu-components-2026-10-18.md). Robu lists a packaging-suffix alternative Vishay1N4148W-E3-18 at ₹8 including GST for 1–49:28 would be ₹224 before delivery. It is not yet an approved replacement for -08.
- Industrial printing: Robu requires one STL, STEP/STP or3MF part per upload, at most100 MB. The currently loaded quote UI offers SLA and other processes/materials, including transparent8001 resin and black resins. The user approved and completed uploads of four quote-only meshes. Live prices are recorded below. Current model exports are a dimensional study, not a manufacturing release.
- PCB: Robu's calculator rejected the outline-only attempt with “Please upload your Gerber file first.” The current project has no routed Gerbers, so no honest board fabrication quotation is available yet. The nominal outline is120.3 × 101.25 mm. The form offers1.6 mm, but not the selected1.5 mm; any change needs stack/stabilizer review. A quantity-five,2-layer FR-4, green, lead-free HASL configuration was considered for budget purposes only; it yielded no price.
- BOM tool: opening Robu's BOM tool redirects to a login page. No account was created or contact information submitted. A local exact-part enquiry CSV is prepared at `procurement/robu-purchased-parts.csv`.

## Manufacturing issues exposed by the supplier check

The live [Robu industrial quote form](https://robu.in/product/industrial-3d-printing/) says wall>1.2 mm and thinnest feature≥0.8 mm. Its fully loaded [printing guide](https://robu.in/3d-printing-guide/) gives size-dependent minimum walls:1 mm up to50 mm parts,1.5 mm up to100 mm and2 mm up to200 mm. It also lists0.8 mm minimum detail,1 mm minimum holes,0.2 mm static-part clearance,0.5 mm moving clearance, and ±0.2 mm or ±0.3% general SLA tolerance with holes ±0.3 mm. These are published process limits, not acceptance of our geometry; the product banner and guide differ, so the stricter applicable limit needs supplier confirmation.

Existing cap walls are nominal 0.7 mm and the blind USB-wall skin approximately0.523 mm. Small legend inlays, capture rings and retaining pieces also need review. Do not present an online price for these meshes as confirmation that they can be printed, assembled or lit as intended. A supplier-reviewed exception or a separate manufacturing revision is required before ordering. No dimensions have been silently thickened for this quote check.

For the base, 8001  Resin with its Translucent option was selected for the cost study. Request a deliberately heavily frosted finish and a small optical sample; this colour selection alone does not validate diffusion. For the top, request the1.5 mm plate as a separately manufactured part with glossy black finish rather than double-counting it in the case price. Ask for exact processes and finish thickness, not only a resin colour name. Navy opaque caps with translucent white legends need an explicit multi-part/coating/inlay process quote; a black resin shell price does not include that result. Macro sheets remain concept-only and have no manufacturable file.

Robu quotes a15–20 business-day lead time for industrial printing after manufacture. Taxes, shipping, finishing, support removal, dimensional acceptance and any minimum-order fees must be explicit in the final quotation. No final project total is available.

## Enquiry scope

Request one frosted lower case, one glossy black support plate, one riser bar (4° provisionally; 7° is an alternative, not a second purchase), one knob,27 navy1u caps and one 2u Space with white translucent legends, plus required custom retention pieces. Magnets, rubber feet, screws and nuts are separate purchased items. Request thin-wall/small-feature review before accepting this design. Ask for quantities and unit/line prices, GST, delivery, lead time, material identity and a list of rejected features or proposed modifications.

### Completed instant estimates

| Quoted mesh, quantity1 each | Process/material | INR including GST |
| --- | --- | ---: |
| Lower case | SLA 8001  Resin, Translucent |₹3,159|
|4° riser body | SLA Black Resin, Grayish Black |₹1,087|
|7° riser body | SLA Black Resin, Grayish Black |₹1,935|
| Knob | SLA Black Resin, Grayish Black |₹252|
| **Four-model subtotal** |**Partial cost study only**|**₹6,433**|

The values were read from completed Robu calculator responses, with each row quantity1 and “Prices shown are inclusive of GST.” The selected list showed₹6,433. No cart, checkout, order, payment, contact details or manual supplier enquiry was submitted. Translucent is a selected colour option, not confirmation of heavy frost or validated diffusion. The four file digests are pinned in `procurement/robu-estimates.json`. The [completed Robu quote screenshot](../procurement/evidence/robu-four-models-2026-10-18.png) preserves the four model lines and supplier subtotal. Other evidence captures are under `/private/tmp/keybaord-robu/`.

This subtotal excludes the top plate, all 28 caps/inlays, magnets, feet, clamps/capture rings, electronics, PCB, custom finishes, shipping and manufacturing revisions. The₹224 diode listing estimate is separate and unapproved as a replacement. Do not add these figures into a final keyboard bill or interpret a calculator response as supplier acceptance of the known defects. The supplier site lists a15–20 business-day lead time for industrial printing; delivery to a destination remains unquoted.
