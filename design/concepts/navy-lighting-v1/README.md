# Navy lighting appearance study

An editable Blender 5.2.2 concept for the 28-key left-hand gaming keypad. The original HTML visualization is preserved.

- `navy-lighting-v1.blend`: editable scene with named collections, materials, camera and studio lights; opens in the volume preview state.
- `navy-lighting-v1.png`: three-quarter studio view with approximately two thirds of the continuous side strip lit to illustrate a hypothetical host volume.
- `navy-lighting-v1-ambient.png`: same view with continuous steady white ambient lighting.
- `build_scene.py`: reproducible scene and render generation, using Blender's bundled Python without third-party packages or external assets.

Run from the repository root:

```sh
/Applications/Blender.app/Contents/MacOS/Blender --background --python design/concepts/navy-lighting-v1/build_scene.py
```

## Design decisions illustrated

All 28 key positions, widths and 19.05 mm row pitch are copied from `scripts/build.mjs`. Dark navy caps have white illuminated legends. Each cap and legend is independently editable. A top-right rotary knob reserves space away from the original keys. The assignable controls currently target turn for volume, Fn + turn for brightness, press for mute, and Fn + press for profiles. Firmware is not implemented.

The provisional shell expands from the original 148 × 118 mm study to 174 × 118 mm to accommodate the knob. That expansion has not been ergonomically accepted. Frosted lenses run along the front and sides. A smooth right-side material mask illustrates a temporary host-volume display; ambient mode illuminates the full band. The strip is white in these appearance previews. White versus RGB hardware and its cost/complexity remain undecided; both directions target independent per-key brightness/effects.

A small Windows helper is accepted as the target for reading actual host volume and synchronising the strip, including changes made outside the knob. That helper and communication path are not implemented or validated. The approximately two-thirds level in the render is purely illustrative.

## Subsequent enclosure direction

The owner prefers a frosted translucent lower shell that itself diffuses light from an LED strip mounted beneath the PCB, producing a glow near the desk and hand/front edge. This replaces the separate lens-band approach as the enclosure design target. Base lighting should briefly show volume, brightness and other setting changes, then return to ambient lighting. Fn and modifier combinations with the dial will control key brightness and other lighting settings. This v1 scene still illustrates exterior lens bands; it has not been revised to model the new lower shell or validate its optics.

## Limits

This is an appearance study, not manufacturing CAD. The keycaps are rounded visual solids with separate emissive legend geometry placed on their top surfaces. They do not yet contain printable translucent inserts, cut-through legends, MX stems or verified switch clearances. The rendered white legends are not proof of light transmission or a printable keycap method.

The frosted lighting is an exterior material preview. Diffuser wall thickness, LED spacing, hotspots, PCB placement, controller support, electrical power and current limits have not been engineered or tested. The knob, switches, screws, connector and feet are visual placeholders. No PCB, firmware, print-service acceptance or fabrication validation is implied.

There are no linked assets, external fonts or texture files. The blend contains its geometry and materials directly. Render generation tests Blender scene construction and rendering only.
