# Fit-v1 verification

Date: 18 October 2026. Scope: drawings-based millimetre specification, Blender visual/fit model and generated website. No physical samples, routed PCB, firmware or manufacturing release were produced.

## Reproducible checks

```sh
npm run build
npm test
npm run audit
node scripts/integration/check-release.mjs
```

The release-media check requires `ffprobe` and `ffmpeg`. It verifies the specification hashes, four still/three clip digests, complete clip decode,960 × 720 resolution,24 fps and12/4/8 second durations. The browser acceptance script additionally requires a Playwright installation and Chrome:

```sh
PLAYWRIGHT_MODULE=/absolute/path/to/playwright/index.js REQUIRE_MEDIA=1 node scripts/integration/browser-check.mjs
SITE_URL=https://glitchyi.github.io/keybaord/ PLAYWRIGHT_MODULE=/absolute/path/to/playwright/index.js REQUIRE_MEDIA=1 node scripts/integration/browser-check.mjs
```

Browser captures and reports are written outside version control under `/private/tmp/keybaord-browser-check` by default. Override `CHECK_OUTPUT` to preserve separate local/live records.

## Native evidence

`design/fit-v1/model-report.json` records analytical checks and explicit unknowns. `native-verification.json` records checks against the saved Blender geometry. `media-manifest.json` links output digests to the source/geometry hashes. The editable scene and reproducible scripts are in the same directory.

The actual cap-shell sweep samples all28 caps at 14 positions from 0 to 3.9 mm against the external switch housing. It excludes custom stem bosses and the supplier's undimensioned BOX internals. The1u and2u roof/skirt allowances are0.5 mm at worst-case travel. Nominal travel animation is3.6 mm. These checks do not prove printed stem retention, BOX guide clearance or stabilizer feel.

Controller/adapter meshes derive from official source CAD; verification includes their solid counts, module-to-floor separation, cable route/controller intersections and conservative reference USB-plug desk clearance at 0°/4°/7°. The supplied FPC is nominally150 mm; the corrected R3 route is approximately 136.73 mm. Its contact-side arrangement, neutral axis, exact engagement and bend limit remain provisional.

Ordinary explosion leaves the soldered switches/stems with the carrier PCB and plate. Case screws lift before the assembly, and caps/knob lift separately. The FPC end disconnects for separation. The lower shell, LED strip and selected magnetic bar are shown as separate service components. This is an explanatory assembly sequence, not a verified assembly instruction.

## Website evidence

Static checks cover shared source/geometry/instance identity, source reference digests,28 keys/30 occupied cells,27 unique drawing sheets across24 BOM families, both riser variants, INR subtotal arithmetic, unique IDs, module syntax, relative Pages asset paths and a preview-only artifact allowlist.

The SVG audit covers finite drawing geometry, source/grid consistency and shared identities. It is not a comprehensive mesh interference, electrical or manufacturing audit.

Chrome checks cover1440 px desktop,900 px intermediate and390 px mobile widths; themes; assembled/exploded/top views; riser visibility; Space press/release; brightness; icon-sheet preview; component sheet selection; focus-loss release; reduced-motion handling; video metadata and runtime/asset errors. Human visual review includes the hero, overlay, exploded view, switch/riser engineering sheets, all four native stills and sampled frames from all three clips.

## Remaining acceptance outside this delivery

Printed sockets/legend inlays,2u stabilizer housing/wire movement, exact custom fit tolerances, fastener access/length stack, captive magnet assembly/retention, foot adhesion/compression, cable insertion/support, optics/diffusion/hotspots and electrical power/USB operation require further engineering and samples. Automatic sheet identification and real host-volume feedback are future firmware/software work.

The dated ₹1,353.30 purchase subtotal is incomplete. It includes an out-of-stock controller-kit listing and excludes all unknown quote lines, fabrication, printing, shipping and other costs. It is not a checkout quote or final bill.

## Release result

Final source specification: `f3b01f1ca1fa3146d8b8418fa5d1a24e8a6f81fbbec2552a7b0e1b603857a1a7`. Geometry contract: `825c3c4eab495d1b896d61a9102a60e4e80efe6e2b686f5e14f7f0e5f52cc3b4`.

Local acceptance passed on 18 October 2026: both theme builds, shared-spec/website checks, SVG source audit, full MP4 decode/digest checks and Chrome tests with all three videos loaded. The lead independently reran the native verifier: 21 checks passed. The nominal report records 21 passes and 6 explicitly unresolved interfaces, with no failures. Camera bounds cover every assembly/switch frame. All 28 legends have visible white roof geometry.

Screenshots and browser reports: `/private/tmp/keybaord-local-final`. Live acceptance is repeated after the Pages deployment; the repository workflow history records the deployment revision. The website and its manifests expose the same source hash for verification.
