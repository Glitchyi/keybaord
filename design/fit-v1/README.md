# Drawing-based fit study

Editable native assembly: `keypad-fit-v1.blend`. All dimensions come from `spec/resolved.json` and the source-derived Waveshare meshes referenced there. Earlier concepts remain preserved.

The plate top is Z=0, X points right, and Y points rear. Default assembly is 4°. Named collections retain the alternative 7° bar and the overlay concept. The overlay has a dial notch and no engineered reader or formed-sheet mechanics.

The caps are hollow custom shallow-dish shells with separate white inlays and provisional cross sockets. The 2u Space has one switch and stabilizer axes at ±11.9 mm. Switch exterior dimensions, plate openings, nominal travel and purchased component envelopes follow the recorded sources. The controller and USB adapter retain the manufacturer CAD tessellation; the USB mouth has the explicitly selected 0.65 mm recess. PCB routing and physical validation are outside this study.

## Outputs

- `assembled.png`: assembled appearance.
- `underside.png`: exploded underside and actual component envelopes.
- `section.png`: display section of custom geometry; purchased internals are not reverse engineered.
- `rear-usb.png`: sourced socket mouth and case aperture.
- `assembly.mp4`: 12 seconds, exploded assembly and reassembly. Soldered parts stay together; removing caps does not remove switch stems.
- `switch-motion.mp4`: 4 seconds, nominal 3.6 mm A and Space travel. The independent checker also sweeps all 28 cap shells through the 3.9 mm worst-case travel envelope.
- `glow.mp4`: 8 seconds, illustrative white brightness and RGB base feedback. This is not an optical simulation or live host-volume reading.
- `geometry-manifest.json`: actual mesh hashes/bounds and source IDs.
- `model-report.json` / `native-verification.json`: nominal checks and explicit unknown interfaces, tied to the shared source/geometry hashes.

The native timeline has three ranges at 24 fps: assembly 1–288, switch motion 289–384, glow 385–576. The default file opens assembled at frame 1 with the full-assembly clip camera; a separate beauty camera is retained.

## Reproduce

From the repository root:

```sh
/Applications/Blender.app/Contents/MacOS/Blender --background --python design/fit-v1/build_scene.py
/Applications/Blender.app/Contents/MacOS/Blender --background design/fit-v1/keypad-fit-v1.blend --python design/fit-v1/verify_scene.py
/Applications/Blender.app/Contents/MacOS/Blender --background design/fit-v1/keypad-fit-v1.blend --python design/fit-v1/render_outputs.py
```

The final command renders stills with Cycles, clips with Eevee, and encodes H.264 with the local ffmpeg. `-- --preview` renders one quick image; `-- --stills-only` omits clips. Frame intermediates are rebuildable output.

## Limits

A passing drawing check does not establish printability, strength, cable compatibility, LED diffusion or manufacturing fit. The BOX internal guide/cap boss interface, keycap retention, stabilizer exterior and wire dynamics, FPC contact side/folding/bend radius, rubber compression/adhesion, magnet force and electronics remain unvalidated. Nominal custom supports, clearances and fastener pockets describe the model, not a manufacturing release.
