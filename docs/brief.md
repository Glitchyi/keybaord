# Build brief

## Intent

Build a simple wired gaming keypad for Valorant, Overwatch and similar games: left hand on keypad, right hand on mouse. Learn PCB and enclosure design through doing the work personally, with guidance and review.

## Current baseline

28 standard-height Kailh BOX Jade mechanical clicky switches are the reference for the drawings-based fit study. The low-profile direction has been superseded. Earlier Blender scenes are retained as appearance studies. USB-C controller module soldered or socketed onto a custom switch PCB. A diode matrix handles simultaneous keys. No wireless, screen or Hall sensing in the first version. Lighting and a volume knob are now requested; their electronics remain to be designed. Browser remapping and three onboard profiles remain goals; rapid trigger and software-adjustable actuation are unavailable with ordinary digital switches.

Profile configuration should use a separate vendor-defined HID interface. Normal keyboard reports must continue independently. Device flash should save only on explicit configuration changes, with versioning and recovery. Firmware is not implemented yet, and the current visualization uses volatile in-memory profiles only.

## Updated design direction

- Rear USB-C follows the owner-supplied close-fitting frosted-wall reference. Fit-v1 uses the actual Waveshare adapter CAD and a nominal0.65mm mouth recess, leaving about0.52mm outer skin with0.1mm PCB clearance. The cradle stays inside the case. Connector engagement, insertion strength and the unselected cable overmould remain physical checks.

- New exploration: retain the normal labelled keycaps and add a removable membrane-like sheet carrying macro icons, with a stepped cutout provisionally interpreted as knob clearance. Detect the installed sheet to switch automatically into macro mode. Multiple identified sheets/profiles are the goal. The knob remains uncovered, and the sheet should hide the original letters with illuminated macro icons. NFC or another detector, material and manufacture remain unresolved; the current fit study includes only a labelled concept layer. Physical overlay labels and firmware mappings must agree. The linked Amazon cover could not be inspected, so no specific construction or fit is assumed.

- PCB design lessons use EasyEDA; enclosure design uses Fusion 360, which the owner already knows.
- Deep, very dark navy blue printed keycaps with white shine-through legends, a mirror-like glossy black top panel and a heavily frosted translucent lower case housing the PCB and electronics. Online printing service required; Robu is a candidate, not a verified provider or quote.
- Individually controlled per-key brightness and effects are desired. Dedicated white key LEDs with individual brightness are selected, with an RGB ambient base strip normally set to white.
- A frosted translucent lower enclosure acts as the diffuser. An LED strip mounted underneath the PCB shines into the lower shell and toward the desk/front edge near the hand. This underglow provides ambient light and temporary feedback for volume, brightness and other setting changes. Avoid a visibly exposed strip or individual LED hotspots; material, spacing and optical performance need sample testing.
- Windows is the primary host; QMK is a firmware candidate. A small Windows helper is accepted to synchronise actual system volume with the diffused base lighting. Integration remains to be validated; standard volume key commands alone do not establish the current level.
- The keypad should also function as a software-programmable macro pad. Target remappable keys, modifier shortcuts and multi-step macros, plus assignable dial rotation/press actions in onboard profiles. Simple keyboard actions should run on-device after configuration. OS/application-specific actions may require a host helper; the configuration protocol, limits and persistence remain to be designed. QMK with VIA-compatible dynamic keymaps/macros is a candidate, not an implemented commitment; reference: https://caniusevia.com/docs/configuring_qmk/.
- Accepted grid: six columns × five rows, all keys aligned, with 28 keys plus an integrated top-right dial. Bottom row: Ctrl, Alt, 2u Space, Fn, 5. Top row: Esc, 1, 2, 3, 4, dial. No dedicated extra macro key. See docs/decisions/0001-sketch-enclosure-and-magnetic-riser.md for the exact map.
- Height adjustment uses alternative full-width triangular magnetic rear riser bars for 4° and 7°, with flat use when removed. Magnetic attachment replaces the earlier screw-on K-001-inspired supports. The rear underside provides a mating seat; magnets, locating geometry and rubber pads are conceptual pending retention and fit testing.
- NuPhy Air75 V3 and Work Louder Micro are visual references for compact controls and frosted material, not hardware compatibility claims. New footprint dimensions follow the aligned grid; older concept dimensions are historical.
- A separate editable Blender concept explores appearance. Upper-right knob location is accepted for the concept. Provisional controls: turn for volume, Fn+turn for lighting brightness, press for mute, Fn+press to cycle onboard profiles. The front-visible base glow briefly indicates the setting being changed before returning to ambient lighting. Fn+turn controls key backlight brightness; additional modifier combinations may control ambient brightness and effects, with exact bindings still to be agreed. A readable volume/level pattern through the frosted base remains to be prototyped. Diffuser geometry and lighting effects remain provisional, not manufacturing geometry.

## Current implementation scope

One shared millimetre specification drives a source-referenced Blender fit model, three animation clips, the Anatomy homepage, a unique-part engineering drawing catalogue and dated INR BOM. Use manufacturer drawings and explicit nominal custom geometry; no parts have been measured or physically tested. The enclosure can grow to fit the parts. Switches are soldered; caps use a uniform shallow dish. PCB routing, firmware, final manufacturing files, real diffuser performance and magnetic retention are outside this implementation. The existing personal repository will be made public and GitHub Pages will publish a website-only artifact with previews.

## Budget under review (previous ₹4,000 target)

| Item | Spending cap |
| --- | ---: |
| Switches and spares | ₹400 |
| USB-C controller module | ₹400 |
| Diodes, headers, wire and solder supplies | ₹200 |
| Basic or reused keycaps | ₹400 |
| One bare-PCB batch | ₹1,000 |
| Lightweight case, plate and small fit sample | ₹600 |
| Cable, screws and feet | ₹200 |
| Shipping | ₹300 |
| Contingency | ₹500 |
| Total | ₹4,000 |

The owner has relaxed the hard ₹4,000 ceiling while requirements are settled, with cost optimisation to follow. The table above is the original baseline allocation; it excludes the newly requested lighting, knob and any additional printing costs and must be re-quoted. These are allocations, not confirmed prices. Includes all planned physical prototypes and parts; assumes borrowed tools, DIY assembly and component reuse. A second full PCB order or large case reprint can exceed the ceiling. The PCB is larger than common 100 × 100 mm promotional pricing; quote the actual outline before ordering. Do not purchase or fabricate without reviewing the concrete files and actual quotes with the owner.

## Learning sequence

1. Review game bindings and print a full-size layout; check reach, the aligned grid, relocated 5 key and thumb position.
2. Wire a few switches to the controller and learn GPIO, pull-ups, diodes and debouncing.
3. Draw the schematic in EasyEDA, reviewing power, matrix, controller headers and debug access.
4. Place one switch cell and diode, replicate the matrix, route and review ERC/DRC. Preserve rework access.
5. Model the enclosure in Fusion 360 using the same key coordinates. Fit-test a small plate/USB/mounting coupon before printing the full case.
6. Implement keyboard firmware, explicit profile saves and browser configuration; test rollover and reconnect persistence.

## Original browser design study (historical layout)

72 solids: shell, deck, four feet, four screw heads, three connector detail parts, three indicator lenses, 28 switch collars and 28 keycaps. Static assembled geometry is audited. The keypress illustration moves caps over concealed collars and is a visual gesture, not a mechanically complete switch model. Four corner labels frame the keyboard; legends on caps are necessary for layout review.

Row staggering is familiar in direction but modifier widths and positions are provisional. Connector detail is a space reservation, not the final rear-wall USB opening. The three indicator lenses illustrate a possible profile indication and are optional pending the parts budget.
