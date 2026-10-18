# Robu local quote bundle

Frozen fit-v1 custom geometry, nominal millimetres, for budgetary quotation only. At export time, no uploads, messages or orders had been performed; the export manifest preserves that point-in-time scope. Four cost-study uploads were subsequently approved by the user and completed. Current selections, prices and calculation status are recorded in [Robu estimates](../robu-estimates.json) and [quote status](../../docs/robu-quote-status.md). Every part remains **not print ready**. No PCB Gerber is supplied: the source PCB is unrouted.

Start with `first-candidates.json`: two closed riser body STLs are the strongest budgetary candidates. The closed knob and lower-case files can support a clearly labelled cost study, but contain known manufacturing defects. Do not use a calculator price as manufacturing approval.

`quote-manifest.json` is the complete per-part audit; `quote-parts.csv` is the quantity/dimension/volume schedule. `stl/` contains separate components at nominal mm, with no studio, annotations, assembly tilt or purchased components. STL does not encode units; select millimetres. Each file has its lowest point at Z=0. Integral source submeshes are exactly unioned on transient copies; source geometry is not thickened, remeshed or redesigned.

Both alternative risers are listed once; they are not simultaneously installed. The 27 single-unit cap shells differ because their legend apertures differ; Space is a separate 2u shell. Separate white inlays and knob index are included to expose, not solve, the undecided manufacturing process. The two USB clamps share one file, quantity 2. One capture-ring geometry is used six times across the case and alternative risers, with two frosted and four navy pieces.

## Provider constraints supplied by current Robu page audit

The industrial banner calls for wall thickness greater than 1.2 mm and thinnest features at least 0.8 mm. The guide additionally gives minimum walls of 1.0 / 1.5 / 2.0 mm for part sizes up to 50 / 100 / 200 mm, minimum detail 0.8 mm, minimum hole 1.0 mm, static clearance 0.2 mm and moving clearance 0.5 mm. Supplier interpretation and material/process suitability still require confirmation. This is a targeted feature audit, not an exhaustive minimum-thickness proof.

## Known blockers

- Cap shells: nominal 0.7 mm walls and 0.75 mm boss walls; stem, stabilizer and legend fits are unvalidated. Separate glyphs contain narrow features and islands without sprues or assembly fixtures. Source navy/white intersection volumes are reported without silently removing the overlap.
- Lower case: USB pocket skin about 0.523 mm and support-post nut-trap radial wall about 0.210 mm. Frosted diffusion, trapped-nut assembly, screw loads and cradle strength are unvalidated.
- Plate: thickness 1.5 mm at 128.3 mm maximum size is below the guide's 2.0 mm wall guidance. The sourced switch installation references a metal frame; resin stiffness and switch retention are unvalidated. Mirror-black finish needs a separate supplier assessment.
- Knob: 0.24 mm grip cylinders and about 0.02 mm proudness are below detail guidance. The actual D-flat seat is geometrically inconsistent with the planned 4.65 mm parameter and needs reconciliation before manufacture. White index geometry is 0.08 mm thick, overlaps the knob, and has no engineered attachment.
- USB clamps: 1.0 mm thick, below the banner's wall requirement; screw openings break out through an end. Capture rings: 0.15 mm thick and 0.3 mm radial wall.
- Risers: the 0.8 mm locating-key height is at the minimum detail threshold. Magnet closure, magnetic force, slip, rubber adhesion, tolerances and actual strength are unvalidated. Separate thin capture rings remain blocked even if the riser bodies receive prices.

Material and finish options have been chosen for the four cost studies; the [estimate records](../robu-estimates.json) and [quote status](../../docs/robu-quote-status.md) document those selections and the resulting quotes. These selections do not validate material suitability or manufacturing readiness. Navy/white matching, heavy frost, optical diffusion and mirror finish remain unknowns.

## Reproduce locally

From the repository root, with the frozen native and spec inputs present:

```sh
/Applications/Blender.app/Contents/MacOS/Blender --background design/fit-v1/keypad-fit-v1.blend --python procurement/robu/export_quote_bundle.py
```

The exporter reads but never saves the native scene. It verifies the source/native and media-manifest hashes remain unchanged. Its mesh audit checks actual serialized triangles, signed volume, dimensions, connected components and edge incidences; this does not establish tolerances, fit or printability. There is no repair or support-generation step.

## Completed mesh audit

64 unique STL files represent 70 custom pieces when both alternative risers are counted. 59 files pass the closed, consistently wound, positive-volume triangle audit. Five fail: cap-1u-esc, legend-esc, cap-1u-3 and legend-3 contain degenerate triangles; knob-index-white has degenerate faces and invalid edge incidence/winding. No repair was made. All 64 files retain matching dimensions and volumes through serialization within the stated audit tolerance.

Every one of the 28 navy cap/white inlay pairs has a measured source intersection (approximately 0.130–0.601 mm³). This confirms that the distinct-material fit needs engineering before manufacture. These components are excluded from budgetary instant-quote candidacy even where their individual STL topology passes.

`first-candidates.zip` contains the first four closed files and their immediate manifest. `quote-bundle.zip` contains the full local audit bundle, including blocked files with explicit defects. These archives and the remaining generated STLs are local, ignored outputs reproducible with the command above. Only the four quoted STLs—`riser-4deg.stl`, `riser-7deg.stl`, `knob.stl` and `lower-case.stl`—are tracked for CI. The export audit itself implies no prices or supplier acceptance; later quote results belong to the linked records.
