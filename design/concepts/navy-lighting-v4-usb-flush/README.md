# Flush rear USB-C appearance variant

This narrow variant changes only the rear USB-C visual placeholder in the accepted ortholinear v4 scene. Earlier files remain preserved. The 28-key grid, knob, glossy black upper panel, heavily frosted base, magnetic triangular rear bar and 72-frame lighting timeline are unchanged.

The metal receptacle mouth sits flush with the rear frosted enclosure's outer plane: keypad-local y = 54.625 mm, with zero outward projection. A close-fitting rounded aperture is cut through the actual rear wall. The socket has a thin metal ring, a dark interior and a tongue; there is no projecting exterior surround or bulky housing. The mouth is at the exterior surface rather than deeply recessed. The existing horizontal position is retained.

- `navy-lighting-v4-usb-flush.blend`: self-contained editable native variant, preserving the accepted beauty camera and animation settings; includes an additional rear close-up camera.
- `rear-usb-flush-closeup.png`: rendered rear close-up.
- `update_usb_flush.py`: reproducibly loads the accepted v4 file and writes this variant plus the close-up. It does not modify the source scene or interact with an open Blender window.

Run from the repository root:

```sh
/Applications/Blender.app/Contents/MacOS/Blender --background --python design/concepts/navy-lighting-v4-usb-flush/update_usb_flush.py
```

The approximately 12.2 × 4.8 mm metal mouth, aperture and internal shapes are visual references only. A real connector, cable plug clearance, retaining method, PCB position, wall strength and tolerances remain unselected and unengineered. This is not manufacturing CAD and does not establish that an actual cable or USB-C receptacle fits. No switch-height or overlay choice is changed. The lighting animation is retained; its MP4 is not rerendered for this rear-only visual change.
