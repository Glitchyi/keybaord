# Parts, drawing evidence and purchase BOM

Research and listing date: 2026-10-18. The shared catalogue is [`spec/parts.json`](../spec/parts.json). Assembly coordinates and final custom dimensions come from the assembly specification. This is a drawing-based visual model and an unrouted PCB study. It does not establish printed fit, switch feel, optics, retention strength, electrical operation or manufacturing readiness.

## Selected drawing references

| Part | Exact reference | Critical drawing dimensions, mm | Evidence boundary |
| --- | --- | --- | --- |
| 28 switches | Kailh BOX Jade CPG1511F01S11-1, Rev B | Top 15.60 × 13.90; mounting body 13.95 ±0.05 square; plate seat 5.00 above PCB; housing roof 11.20 above PCB; stem projects 3.80; nominal stem tip 15.00 above PCB. | Standard-height soldered switch. Additional sourced profile: latch width14.87±0.5; opposite-view body height10.70; center postØ3.85+0/−0.1, projection1.40. The0.50 base datum difference is derived11.20−10.70, not a separately toleranced callout. Taper/window/terminals are undimensioned approximate contours. |
| Switch plate | Same Kailh drawing, actual PDF p11 / printed p10 | Cutout 14.00 ±0.05 square, corner R0.30 maximum; **plate thickness 1.50 ±0.10**; travel 3.60 ±0.30; pretravel 1.80 ±0.30. | The 1.50 dimension is metal-frame thickness. It is not a Kailh PCB-thickness callout. |
| 2u stabilizer | CHERRY G99-0742 PCB-mount, catalogue printed pp70–71 | Support axes 23.8 apart, ±11.9 from switch; PCB 1.50 ±0.14; PCB hole pairs 15.24 apart; local Y −7.00 / +8.24, holes Ø3.05 +0.10/−0 and Ø4 +0.05/−0. | Exact sourced mounting pattern; small housing/stem shapes are drawing approximations. Indian stock/quote unknown. Do not substitute a generic ±12 stem spacing. |
| Main controller | Waveshare RP2040-Tiny V1.1 | Official STEP overall 18.016649 ×23.517258 ×2.875103, PCB component top z0 / bottom−1.000003; highest model feature1.8751 above PCB. | Corrects prior2.1 envelope assumption. Highest feature appears to be the FPC actuator; its closed state is not established. Catalogue now uses2.87511 as a conservatively rounded model envelope. |
| Remote USB board | Waveshare RP2040-Tiny-Adapter V1.1 | Nominal PCB 18 ×18; assembled envelope 18.02 ×18.02 ×4.25. | Extracted mouth center[178.990038,124.981722,1.669522] in original STEP, normal+Y. Mouth outer8.94×3.16, inner8.54×2.76. See adapter-datums.json. A whole-board bbox cannot establish the mouth center. |
| Encoder | Bourns PEC11R-4215F-S0024 | Body 12.5 ×13.4; mounting shoulder 6.5 above PCB; L15 shaft above shoulder, nominal shaft tip 21.5 above PCB; shaft Ø6 ±0.1, D-flat 4.5 +0/−0.05; bushing length 5, flat length 7; push 0.5; pins 3.7 below PCB. | Use PEC11R-4xxxF-Sxxxx drawing, current REV04/26 PDF p2 lower figure and p3 shaft table. 24 detents, 24 pulses. |
| White LED | Kingbright APT1608QWF/D | 1.6 ×0.8 ×0.75 package. | Top-emitting package. Physical passage through the switch and cap is unverified. |
| Matrix diode | Vishay1N4148W-E3-08, SOD-123 | Body2.7 ±0.15 ×1.55 ±0.15; height1.175 ±0.175; lead span3.7 ±0.15. | 28 installed; future distributor cut-tape MOQ/spares unknown. |
| White driver | Lumissil IS31FL3236-QFLS2-TR | QFN44, 5 ×5. | Package and support-circuit placement only; unrouted board. |
| RGB strip | Adafruit 2969, white PCB, 144 pixels/m | Covered section 10.4 wide ×4.3 high; bare flex width 7.5; nominal pixel pitch 1000/144 ≈6.944. | Covered and bare envelopes differ. Installed cut length belongs to assembly; purchased reel 1m. |
| Riser magnets | K&J D42 | Axial N42, Ø6.35 ×3.175, ±0.1 dimensional tolerance. | Two case magnets plus two in each alternative bar = six total. Thick-steel pull figures do not establish this joint's retention. |
| Desk contacts | 3M SJ5302, 3M ID7100006189 | Clear hemispherical foot, Ø7.94 ×2.2. | Four case feet and two per alternative bar = eight total. Compression/adhesion unverified. |
| Enclosure screws | RS PRO293-280, M2×6 DIN912 | Nominal head Ø3.8 ×2, thread M2×0.4, underhead length6. | Six total: four enclosure screws plus two external USB cradle/clamp screws. Exact fastener tolerance and length stack remain to check. |
| Captive nuts | RS PRO248-4551, M2 DIN934 | Height1.6, nominal across-flats4.0. | Six total matching screws. Custom captive pocket clearance follows assembly. |
| Flex interconnect | Supplied Waveshare 8-pin FPC | Approximate length150. | Contact-side arrangement, flex thickness/width and minimum bend radius are not verified. An illustrated bend is a nominal clearance study. |

Primary drawing sources: [Kailh BOX Jade PDF](https://cdn-shop.adafruit.com/product-files/5149/BOX_Jade.pdf), [CHERRY manufacturer catalogue](https://datasheet.octopart.com/0G990742-Cherry-datasheet-26580244.pdf), [Waveshare main STEP](https://files.waveshare.com/upload/9/94/RP2040-Tiny-Step_V1.1.zip), [Waveshare adapter STEP](https://files.waveshare.com/upload/1/1e/RP2040-Tiny-Adapter-Step_V1.1.zip), [Waveshare cable instructions](https://www.waveshare.com/wiki/RP2040-Tiny), [Bourns PDF](https://www.bourns.com/docs/product-datasheets/pec11r.pdf), [Kingbright PDF](https://www.kingbrightusa.com/images/catalog/spec/APT1608QWF-D.pdf), [Lumissil PDF](https://www.lumissil.com/assets/pdf/core/IS31FL3236_DS.pdf), [Vishay diode PDFp4](https://www.vishay.com/docs/86356/1n4148w.pdf), [Adafruit strip](https://www.adafruit.com/product/2969), [K&J D42](https://www.kjmagnetics.com/d42-neodymium-disc-magnet), [3M foot](https://www.3m.com.my/3M/en_MY/p/d/v000180779/), [RS screw drawing](https://docs.rs-online.com/3718/A700000007946802.pdf), [RS nut](https://uk.rs-online.com/web/p/hex-nuts/2484551).

The official Waveshare source archives were inspected locally. Portable dimensional records and tessellated inspection geometry are under `spec/references/waveshare/`, with source URLs and SHA256 provenance. The archives contained STEP files without an explicit redistribution license, so the raw archives/STEP files were moved outside the public repository after inspection. They are third-party component references, not project-authored manufacturing designs. `adapter-datums.json` provides the exact socket mouth plane/center and PCB datum, identifies no screw mounting holes, and labels the FPC exit plane provisional.

## Dated INR purchase evidence

| Item | Needed | Purchased basis | Price evidence | Extended known amount |
| --- | ---: | --- | ---: | ---: |
| BOX Jade |28|3 ten-packs =30 switches|₹280/pack, including GST; in stock on dated check|₹840.00|
| RP2040-Tiny kit |1|1 kit, main+adapter+supplied FPC|₹435+18% GST =₹513.30; listing showed **zero stock**|₹513.30|
| All other lines |See catalogue|Exact supplier quantity not quoted|Unknown; JSON `null`|Excluded|
| **Known purchase subtotal** |||| **₹1,353.30** |

Sources: [Meckeys BOX Jade ten-pack](https://meckeys.com/shop/accessories/keyboard-accessories/key-switches/kailh-box-jade-switch/), [Hubtronics RP2040-Tiny kit](https://hubtronics.in/rp2040-tiny-kit). These are dated listings, not checkout quotes. The kit price is evidence for an out-of-stock listing. Shipping, imports, all null-priced components, PCB fabrication/assembly, printing and finishing, passives, cable and supplies are excluded. This subtotal is **not the project cost**. Adapter and FPC are included in the kit price and must not be charged twice.

For a future purchase quote, request the exact stabilizer, encoder, 28 LEDs and 28 diodes plus spares, driver/support passives, buffer, RGB strip reel, six exact magnets, eight feet, six screws and six nuts, USB data cable, PCB batch, plate, enclosure, both risers, 27 custom1u caps and one2u Space, legend printing/inlays, knob and any overlay material. Include minimum order quantities, tax, shipping and failed-print/sample allowance. No purchases are authorized by this catalogue.

## Custom dimensions and unresolved interfaces

The catalogue lists24 lines, with22 null-priced lines. `riser_4` and `riser_7` each represent one separately quoted printed bar; the case price excludes both bars. Shared magnets and feet are counted on their own lines.

The case integration envelope 128.3 ×109.25, plate1.5, PCB1.5 and custom caps18 ×18 /37.05 ×18 with0.7 nominal walls are design choices. Their presence in a model is not an external supplier claim. The root assembly specification controls exact geometry and can supersede these placeholders.

The source BOX Jade profile does not dimension the stem cross section or the inside of its BOX guide. A nominal custom cross socket and boss cannot be certified by subtracting solid external housing boxes: the real guide has a cavity. Mark the stem/boss interface **provisional**, show the cavity explicitly where appropriate, and preserve a precise unresolved fit check. Roof/skirt full-travel clearance can be checked independently against3.9mm maximum travel; that still does not prove stem insertion, material strength or friction.

The extracted adapter socket rim center is1.669522 above its PCB component surface; full-shell bbox midpoint1.169522 is incorrect because mounting tabs extend below the PCB. Use the actual adapter socket mouth as the rear-wall datum, a supported adapter cradle for insertion load, and a plug-overmould clearance volume. The reference external USB-C data cable and its overmould dimensions are not selected or source-verified. Do not label an invented12×6mm overmould as a manufacturer dimension. Flex cable routing must avoid LED channel and fasteners; minimum bend radius remains a labelled assumption until the exact supplied cable is specified.

Magnet pockets need keyed locating geometry to carry shear and a positive retaining closure to keep the magnets captive. Pocket diameter/depth, cover thickness, adhesive and fit allowance are custom nominal values. The default catalogue supplies no retention-force guarantee.

LED brightness, diffuser material, white legends, strip spacing and USB power allocation remain untested. A render can show a lighting concept without validating optical efficiency, uniformity or power delivery. Automatic overlay identification remains conceptual.
