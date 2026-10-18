# keybaord

A left-hand USB-C gaming keypad learning project. The current direction is 28 mechanical clicky keys, a custom switch PCB, and a 3D-printed enclosure, with a ₹4,000 total project ceiling.

The owner designs the PCB and enclosure. Development proceeds through explanations, small experiments, and reviews before fabrication.

## Start the visualization

Requires Node.js 20.10 or newer. No package install is needed.

```sh
npm run build
npm start
```

Open http://127.0.0.1:8766. Select keys, hold them down, switch to the top view, and experiment with three in-memory profile previews. The UI uses a monochrome shadcn-style layout; the keyboard is an isometric SVG built with the vendored Anatomy kit.

`index.html` and `index-light.html` are standalone and can also be opened directly. This is plain HTML, CSS and JavaScript, not a React/shadcn component implementation.

## Scope

- USB-C power and data, using a small controller module on the owner-designed PCB.
- Mechanical clicky switches; fixed switch actuation, without rapid trigger.
- Browser remapping and persistent onboard profiles are firmware goals. The visualization does not connect to a device or save anything to hardware.
- One-switch-per-key matrix with anti-ghosting diodes; controller, pin assignment, firmware and components remain unselected.
- Proposed 148 × 118 mm envelope and 19.05 mm pitch are layout references, not manufacturing dimensions. The thumb row and stabilizer need fit testing.

## Project map

- `scripts/build.mjs`: 72-part isometric geometry, interface and preview interactions.
- `scripts/serve.mjs`: localhost-only preview server.
- `docs/brief.md`: requirements, budget and next learning steps.
- `docs/visual-verification.md`: scope of visual and interaction checks.
- `vendor/anatomy/`: geometry and audit helpers, with their MIT license.

Run `npm run audit` for the visualization geometry audit. This verifies drawing geometry, not PCB electronics, switch mechanics or manufacturability. Browser checks use the locally installed visualization tooling; the resulting screenshots are kept outside version control.
