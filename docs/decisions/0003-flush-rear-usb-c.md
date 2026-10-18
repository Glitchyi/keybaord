# Flush rear USB-C socket

Status: accepted appearance target; fit-v1 drawing-based implementation added below.
Date: 2026-10-18

The owner supplied a photo showing a USB-C receptacle through a close-fitting frosted rear wall. Adopt a socket mouth flush with the outside rear case surface, without a projecting surround or deep access tunnel. Keep the existing accepted grid, materials, magnetic risers and animation. This change is independent of the unresolved legend overlay and exact low-profile switch selection.

The Blender revision should contain a real opening in the visual case geometry and an editable receptacle approximation. Final USB-C part, wall thickness, PCB alignment, cable plug clearance and insertion-load support must be designed and checked later. A flush-looking render does not prove cable fit or connector strength.

## Fit-v1 integration

The selected reference is the Waveshare RP2040-Tiny-Adapter V1.1 official CAD. Its mouth sits nominally0.65 mm behind the exterior plane. A PCB clearance of 0.1 mm leaves an outer wall skin of approximately 0.523 mm; the supporting cradle has no external lip. This practical near-flush interpretation supersedes the earlier exactly-flush approximation and the0.05 mm recess trial, which left an unusably thin wall. The board has no screw mounting holes; two external clamp screws retain its nominal cradle. Source FPC contact position and actual insertion-load strength remain unvalidated. Standard BOX Jade switches supersede the low-profile reference in the original note.
