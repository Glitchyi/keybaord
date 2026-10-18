# keybaord

A wired 28-key gaming keypad and macro-pad learning project: deep navy shine-through caps, glossy black top, frosted illuminated base, a grid-aligned dial and rounded magnetic 4°/7° risers.

[Open the Anatomy homepage](https://glitchyi.github.io/keybaord/). It includes the interactive layout, native Blender previews, dimensioned engineering drawings and a dated INR parts list.

## Current delivery

Fit-v1 is a source-referenced dimensional study. Standard Kailh BOX Jade switches, one 2u Space, controller/remote USB boards and selected support parts share a millimetre specification. The case is nominally128.3 × 109.25 mm. Purchased parts use linked manufacturer drawings/CAD; custom fits and unverified dimensions are labelled provisional.

The model does not establish physical fit, printability, magnet retention or optical diffusion. PCB routing, firmware, power design, automatic macro-sheet detection and manufacturing files remain future work. The macro sheet is a visual concept; browser profiles do not configure a device. EasyEDA and Fusion remain the intended PCB/enclosure learning tools.

## Preview and checks

Node.js22 recommended; no package installation is needed.

```sh
npm run build
npm test
npm run audit
npm start
```

Open `http://127.0.0.1:8766/keybaord/`. The generated `dist/` directory is the GitHub Pages artifact. Root `index.html` and `index-light.html` are also generated standalone previews. The website uses plain HTML/CSS/JavaScript and SVG with the vendored Anatomy kit.

## Project files

- [Implementation plan](docs/implementation-plan.md): settled decisions, ownership and acceptance gates.
- [Build brief](docs/brief.md): requirements and the later learning sequence.
- [Shared assembly dimensions](spec/keypad.json), [parts/sources](spec/parts.json), [resolved specification](spec/resolved.json).
- [Blender fit model](design/fit-v1/keypad-fit-v1.blend), build/render scripts and native verification reports under `design/fit-v1/`.
- [Parts and BOM evidence](docs/parts-and-bom.md): dated 18 October 2026. Known purchase subtotal ₹1,353.30; remaining quotes, printing, PCB, shipping and other costs are excluded. This is not the final project cost.
- [Verification record](docs/visual-verification.md): what was actually checked and what remains unknown.
- `scripts/web/` and `scripts/engineering/`: interactive homepage and unique-part drawing generators.
- `.github/workflows/pages.yml`: build, checks and Pages deployment on main.
- `design/concepts/`: preserved earlier appearance studies, including the low-profile and older USB/riser concepts. They are historical references.
- `vendor/anatomy/`: retained geometry helpers and their MIT license.

For Blender regeneration, see the fit-model build scripts. The published site contains rendered previews, not native CAD download links. Review the concrete design and supplier quotes before ordering any parts or fabrication.
