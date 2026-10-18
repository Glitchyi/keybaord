# Fit-v1 implementation plan

Decision date: 18 October 2026. This is the accepted drawing-based design scope, incorporating the selected grid, switches, finish, lighting and removable risers. The repository remains the existing `Glitchyi/keybaord` project. Earlier concepts are retained.

## Decisions

- 28 soldered Kailh BOX Jade switches on a 19.05 mm grid, six columns by five rows. The upper-right cell holds a Ø16 mm encoder knob. A single 2u Space preserves the wider thumb target.
- Uniform shallow-dish deep navy caps with white legend inlays, a glossy black 1.5 mm mounting plate and heavily frosted lower case. Nominal case footprint: 128.3 × 109.25 mm. These custom dimensions are design values, not supplier tolerances.
- Separate per-key white LEDs and an addressable RGB base strip normally set to white. Animations illustrate the intended front/desk glow; they do not predict diffusion, brightness or USB power consumption.
- Bourns PEC11R-4215F-S0024 encoder; Waveshare RP2040-Tiny V1.1 main and remote USB boards. Manufacturer CAD establishes the board solids and socket mouth. The rear mouth is nominally recessed 0.65 mm for wall thickness and PCB clearance, without an external cradle lip.
- Flat use plus alternative full-width magnetic 4° and 7° rear bars. Blunt noses, rounded edges/ends, captive magnet pockets, locating keys and rubber contacts. Retention, slip, surface protection and screw access remain sample checks.
- Macro sheets have a knob notch and geometric icons. They are explicitly a concept overlay. Formed-sheet mechanics, material, optical masking and automatic profile detection are deferred. Browser profile changes are manual previews.
- EasyEDA PCB routing, Fusion manufacturing CAD, QMK firmware and a Windows volume helper are later implementation phases. This delivery contains an unrouted dimensional PCB carrier and editable Blender scenes, not fabrication-ready hardware.

## Shared source and ownership

1. Parts owner: `spec/parts.json`, `spec/references/`, `docs/parts-and-bom.md`. Record exact part codes, source URLs/revisions, dimension status and dated INR pricing. Imported component surfaces remain identifiable as third-party references.
2. Lead: `spec/keypad.json`, `scripts/resolve-spec.mjs`, integration checks, plan/verification documentation and GitHub deployment. Establish all millimetre datums, part positions, allowances and poses before downstream builds. A source hash links every output to the same contract.
3. Blender owner: `design/fit-v1/` only. Build from the resolved specification, including source controller/USB meshes, switch envelopes/movement, hollow caps, legend openings, 2u stabilizer axes, cable route and rounded risers.
4. Website owner: website generators, drawing generators and generated HTML/dist only. Build the Anatomy homepage and unique-part drawings from the same resolved contract. Work in parallel with Blender only after the contract is frozen; integration corrections require a new shared hash and both rebuilds.

## Source hierarchy

Manufacturer dimensioned drawings and official CAD govern selected purchased components. `docs/parts-and-bom.md` links the Kailh, CHERRY, Waveshare, Bourns, Kingbright, Lumissil, Vishay, TI, Adafruit, K&J, 3M and fastener references. Supplier listings establish dated price/stock evidence only. Undimensioned switch internals, printed socket fits, cable neutral axis/bend radius, cap printing and optical paths remain provisional. Never convert a missing dimension or quote into a verified value.

## Deliverables

- `spec/keypad.json` + `spec/parts.json` → generated `spec/resolved.json`, all in millimetres, with source and geometry hashes.
- Editable `design/fit-v1/keypad-fit-v1.blend`, reproducible build/render scripts, model and native-verification reports.
- Assembled, rear USB, section and underside stills; 24 fps 960 × 720 exploded/reassembly (12 s), switch movement (4 s) and glow (8 s) clips. Soldered switches stay with the plate/PCB during ordinary disassembly; caps and knob lift separately. Switch travel moves the cap and stem together.
- Anatomy homepage with dark/light themes, keyboard/pointer controls, top/isometric views, riser poses, brightness preview, manual macro-sheet preview and reduced-motion support. Native stills/videos are displayed below.
- Dimensioned engineering drawing catalogue covering each unique part/variant, including both risers and the 2u cap/stabilizer. Provisional geometry and component reference boundaries remain visible. On-screen zoom is not an actual-size measurement.
- Dated INR BOM: quantities, supplier links, stock status, pack quantities and known purchase subtotal. Unknown fabrication/printing/component quotes are explicitly excluded; no false final total.
- Existing GitHub repository made public as authorized. GitHub Pages deploys only generated `dist/` website previews; the homepage has no native CAD downloads. Earlier concepts remain in the repository.

## Acceptance gates

1. Source integrity: 28 keys, complete 30-cell occupancy including 2u Space and knob, source/geometry hash consistency, all dimensions in mm, manufacturer reference hashes preserved.
2. Mechanical model: source solid counts, nominal/worst-case switch travel, cap roof/skirt clearance, 2u axes, actual mesh sweep against external switch housing, USB mouth/wall position, reference cable clearance in all poses, FPC route length and controller clearance, riser contact/nose calculations. Clearly report excluded interfaces and unknowns.
3. Visual review: inspect all four stills and sampled frames from all three clips. Correct visible assembly collisions, port protrusion, clipping, illegible labels and misleading source geometry before release.
4. Website: build both themes, run source/drawing audit and static checks; test current Chrome at desktop, intermediate and 390 px widths, keyboard/pointer interactions, focus-loss release, profile overlay, riser poses, reduced motion, video metadata and runtime errors. Drawing audit scope is digital presentation, not manufacturability.
5. Release: review the staged content, run required hooks without bypass, commit/push the existing main branch, enable Pages Actions, wait for a successful deployment, then repeat live hash/media/browser checks at the deployed URL.

## Following physical review

Before any purchase/fabrication, obtain actual quotes and make small coupons for BOX socket/plate, 2u stabilizer, USB/cradle, magnetic joint and diffuser. Check full key movement under a formed overlay, magnet capture/strength, fastener access, tolerances and LED power/optics. A successful digital check does not establish these outcomes.
