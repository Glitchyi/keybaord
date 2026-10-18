# Build brief

## Intent

Build a simple wired gaming keypad for Valorant, Overwatch and similar games: left hand on keypad, right hand on mouse. Learn PCB and enclosure design through doing the work personally, with guidance and review.

## Current baseline

28 standard mechanical clicky switches. USB-C controller module soldered or socketed onto a custom switch PCB. A diode matrix handles simultaneous keys. No RGB, wireless, display or Hall sensing in the first version. Browser remapping and three onboard profiles remain goals; rapid trigger and software-adjustable actuation are unavailable with ordinary digital switches.

Profile configuration should use a separate vendor-defined HID interface. Normal keyboard reports must continue independently. Device flash should save only on explicit configuration changes, with versioning and recovery. Firmware is not implemented yet, and the current visualization uses volatile in-memory profiles only.

## ₹4,000 total ceiling

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

These are allocations, not confirmed prices. Includes all planned physical prototypes and parts; assumes borrowed tools, DIY assembly and component reuse. A second full PCB order or large case reprint can exceed the ceiling. The PCB is larger than common 100 × 100 mm promotional pricing; quote the actual outline before ordering. Do not purchase or fabricate without reviewing the concrete files and actual quotes with the owner.

## Learning sequence

1. Review game bindings and print a full-size layout; check reach, row staggering and the thumb position.
2. Wire a few switches to the controller and learn GPIO, pull-ups, diodes and debouncing.
3. Draw the schematic in KiCad, reviewing power, matrix, controller headers and debug access.
4. Place one switch cell and diode, replicate the matrix, route and review ERC/DRC. Preserve rework access.
5. Model the enclosure in the owner's chosen CAD tool using the same key coordinates. Fit-test a small plate/USB/mounting coupon before printing the full case.
6. Implement keyboard firmware, explicit profile saves and browser configuration; test rollover and reconnect persistence.

## Design study

72 solids: shell, deck, four feet, four screw heads, three connector detail parts, three indicator lenses, 28 switch collars and 28 keycaps. Static assembled geometry is audited. The keypress illustration moves caps over concealed collars and is a visual gesture, not a mechanically complete switch model. Four corner labels frame the keyboard; legends on caps are necessary for layout review.

Row staggering is familiar in direction but modifier widths and positions are provisional. Connector detail is a space reservation, not the final rear-wall USB opening. The three indicator lenses illustrate a possible profile indication and are optional pending the parts budget.
