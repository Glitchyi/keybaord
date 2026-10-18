# Compact navy / frosted-base appearance study

Revision 3 preserves all 28 original key positions and returns to the provisional 148 × 118 mm footprint. A small top-row dial replaces revision 1's wide empty control gutter. Keycaps are deeper navy, the upper panel is black, and the entire lower enclosure is frosted translucent material. Lighting beneath the PCB is intended to shine through that shell toward the desk and hand-facing front edge.

## Files

- `navy-lighting-v3.blend`: editable Blender 5.2.2 scene, named objects/collections and self-contained materials.
- `navy-lighting-v3.png`: three-quarter assembled studio view.
- `build_scene.py`: reproducible scene and render, using Blender's bundled Python.

```sh
/Applications/Blender.app/Contents/MacOS/Blender --background --python design/concepts/navy-lighting-v3/build_scene.py
```

The first concept and the existing browser visualization are preserved. Generating this revision runs Blender in a separate background process and does not replace the scene open in the desktop app.

## Design intent and references

The integrated dial is inspired by the [NuPhy Air75 V3](https://nuphy.com/products/nuphy-air75-v3). This concept uses ordinary mechanical MX-style clicky switches; the reference does not change the switch architecture to low-profile hardware.

The compact control layout and diffusing enclosure draw inspiration from [Work Louder Creator Micro 2](https://worklouder.cc/creator-micro-2), whose product description identifies a sandblasted polycarbonate body. This is a rectangular 28-key gaming/macro keypad, with no copied engineered dimensions or claims that a printed material will reproduce injection-moulded or sandblasted optics.

The knob is provisionally 16 mm in diameter at layout coordinates (134, 17.5) mm. Its top is close to the keycap height. The original `5` key ends at x = 120.25 mm, leaving 5.75 mm between its rectangular cap envelope and the knob's 8 mm radius. The adjacent `T` key below remains separate in the top-view geometry. These are visual plan clearances, not encoder-package, finger-clearance, switch-travel or manufacturing acceptance.

The assignable control targets remain turn for volume, Fn + turn for key brightness, press for mute, and Fn + press for profiles. Modifier combinations and a configuration application may add more lighting and macro controls. A small Windows helper is planned to report actual host volume. Base lighting should show settings feedback temporarily and return to soft ambient lighting. These renders show ambient white only; firmware, the helper, software macro functions and animated feedback are not implemented.

## What is modeled

All 28 keycaps and separate emissive white legends remain individually editable. The single frosted lower shell has an open upper cavity and a conceptual bottom/walls. Black top panel, knob, feet, connector and hardware remain visual placeholders. A hidden collection contains the conceptual PCB and underside LED strips; toggle that collection to inspect them. A downward area light approximates soft light reaching the desk through the base.

## Limits

This is an appearance study, not fabrication-ready Fusion CAD, a PCB design or a printable keycap model. Legend geometry is emissive surface text rather than printable translucent inlays; stems, switch sockets, stabilisers, mounting bosses and electrical routing are absent. No separate perimeter lens bands remain in this revision.

The frosted material is a render approximation. Its transmission, thickness, LED spacing, hotspots, diffusion, brightness, thermal behaviour and the actual desk glow require material samples and physical testing. It does not prove that a particular print service or resin/filament will produce this effect. No manufacturing exports, component purchasing or electrical validation are included.

There are no external fonts, texture files or linked libraries. Native scene construction, successful render and reopen checks establish only Blender artifact integrity.

## Removable angle supports

The default scene shows a 4° typing angle with two removable screw-on rear support concepts and rubber desk-contact pads. The complete keypad assembly is rotated coherently; support tops meet its tilted bottom plane and rubber pads reach the studio ground. The front remains open for the diffused glow toward the hand. These are support feet, not a palm rest and not fold-out feet.

The [WALLHACK K-001 angle-adjustment guide](https://wallhack.gorgias.help/en-US/how-do-i-adjust-the-typing-angle-on-my-wallhack-k-001-7753049) is the reference for removable screw-on risers and 0°, 4° and 7° options. No fastener dimensions are copied. The mounting arrangement is independently provisional; the reference does not establish that these particular supports fit or are strong enough.

Named collections contain installed 4° risers, contact pads, hidden 7° alternative risers, and hidden flat-mode pads. They are editable visual alternatives, not an automatic angle selector. To inspect 7°, hide the 4° supports, reveal the alternatives and change the assembly rotation to 7°; front-pad fit needs subsequent refinement. For a flat study, rotate the assembly to 0°, hide installed risers/contact pads and reveal the flat pads.

Threads, insert geometry, screw length, load capacity, tip resistance, desk grip and optical performance remain unengineered. The model contains no final screw-on manufacturing interface. Fit coupons and a physical stability test are required before a full enclosure print.
