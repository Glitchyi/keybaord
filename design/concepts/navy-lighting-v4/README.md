# Ortholinear keypad / magnetic rear-bar appearance study

The confirmed concept is a 6-column × 5-row ortholinear grid at 19.05 mm pitch. It contains 28 standard mechanical clicky MX-style key positions plus one rotary knob. The provisional enclosure is 128.30 × 109.25 mm, using a 7 mm border around six/five pitch cells. This replaces the staggered layout in earlier concepts, which remain preserved.

| Row | Column 1 | Column 2 | Column 3 | Column 4 | Column 5 | Column 6 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Esc | 1 | 2 | 3 | 4 | Knob |
| 2 | Tab | Q | W | E | R | T |
| 3 | Caps | A | S | D | F | G |
| 4 | Shift | Z | X | C | V | B |
| 5 | Ctrl | Alt | Space | Space continued | Fn | 5 |

Space spans two pitch cells with a 36.05 mm visual cap; single-cell caps are 17 mm wide. Keycap, legend and switch objects remain individually editable. Deep navy keycaps have white legend previews above a glossy mirror-black top panel. The entire heavily frosted lower enclosure houses the electronics and diffuses white light; there are no separate side-strip lens bands or visible individual LED dots.

## Deliverables

- `navy-lighting-v4.blend`: self-contained editable scene, keyed lighting timeline and named component collections.
- `navy-lighting-v4.png`: assembled beauty still at 1600 × 1200.
- `navy-lighting-v4-underside.png`: underside view with the full-width rear bar separated downward to show its magnetic seats.
- `navy-lighting-v4-lighting.mp4`: six-second 960 × 720 H.264 lighting illustration at 12 fps.
- `build_scene.py`: reproducible geometry, stills and animation frames using Blender 5.2.2's bundled Python.
- `verify_scene.py`: native structural and timeline checks.

Rebuild from the repository root:

```sh
/Applications/Blender.app/Contents/MacOS/Blender --background --python design/concepts/navy-lighting-v4/build_scene.py
/Applications/Blender.app/Contents/MacOS/Blender --background design/concepts/navy-lighting-v4/navy-lighting-v4.blend --python design/concepts/navy-lighting-v4/verify_scene.py
/opt/homebrew/bin/ffmpeg -y -framerate 12 -i design/concepts/navy-lighting-v4/frames/frame_%04d.png -c:v libx264 -pix_fmt yuv420p -crf 20 -movflags +faststart design/concepts/navy-lighting-v4/navy-lighting-v4-lighting.mp4
```

The native timeline runs frames 1–72: ambient white, brightness adjustment, illustrative host-volume feedback, then ambient white. Key legends brighten during the adjustment phase. A soft mask grows across the frosted base during volume feedback. A broad white light illustrates light spilling onto the front desk/hand area. Play the timeline using rendered viewport shading for the intended appearance; material-color/solid view does not display rendered optical effects. The MP4 provides the rendered preview without waiting for interactive convergence.

## Magnetic rear bar

A full-width triangular rear support bar sits beneath the rear edge. The default assembly is tilted 4°. Named collections contain the installed 4° bar, hidden 7° alternative bar, hidden flat-mode pads and paired magnet/recess placeholders in the shell and bar. The bar uses magnetic attachment; there are no mounting screws for the riser. Rubber contacts meet the desk and leave the front diffuser unobstructed.

The hidden alternatives are editable studies rather than an automatic angle selector. A 7° study needs the assembly rotated accordingly and front-pad fit reviewed; flat mode removes the bar and uses the flat pads. The shell/bar magnet disks and seats show placement intent only. Magnet dimensions, polarity, holding force, anti-slip behaviour, structural stability, recess depth and shell thickness have not been engineered or tested. Magnet placeholders can intersect the concept shell and do not constitute fabrication bores.

The earlier angle-option reference was the [WALLHACK K-001 guide](https://wallhack.gorgias.help/en-US/how-do-i-adjust-the-typing-angle-on-my-wallhack-k-001-7753049), which describes screw-on 0°/4°/7° options. This revision adopts the owner's magnetic triangular-bar direction instead; no reference screw lengths or attachment details are copied. Compact dial and diffusion references remain [NuPhy Air75 V3](https://nuphy.com/products/nuphy-air75-v3) and [Work Louder Creator Micro 2](https://worklouder.cc/creator-micro-2), without copied engineered dimensions.

## Implementation limits

This scene illustrates the accepted visual direction. It is not Fusion manufacturing CAD, printable keycaps, a PCB layout, device firmware or the Windows helper. Legends are emissive surface geometry, not verified translucent inserts; MX stems, stabilisers, switch mounting, detailed electronics and final mechanical interfaces are absent. Hidden PCB/underside-strip objects show the architecture only.

Whole-shell frost, transmission, mask and external soft light are visual approximations of the intended effect. The underside PCB LEDs are not a measured optical simulation. Actual materials, hotspots, power draw, thermal behaviour, brightness, diffuser thickness and desk illumination need component selection and physical samples. The volume fraction is scripted illustration, not a live Windows reading. Future controls/macros/profile switching and actual host-volume synchronisation remain unimplemented.

The scene uses built-in text and self-contained materials with no external textures, fonts or linked libraries. Previous concepts and the browser visualization remain unchanged. No manufacturing exports or purchases are included.
