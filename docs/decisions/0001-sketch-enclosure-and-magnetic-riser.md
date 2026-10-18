# Sketch enclosure and magnetic riser

Status: accepted for the next Blender appearance study; engineering remains provisional.
Date: 2026-10-18

## Decision

Use a tight ortholinear six-column, five-row arrangement with 28 mechanical keys and an integrated top-right dial. Keep a 2u Space key, without a dedicated extra macro key. Every key and dial action remains a software-remapping target.

```text
Esc    1     2     3     4    Knob
Tab    Q     W     E     R     T
Caps   A     S     D     F     G
Shift  Z     X     C     V     B
Ctrl  Alt   [  Space  ]  Fn    5
```

The top panel has a mirror-like glossy black appearance. Deep dark navy caps have white illuminated legends. A heavily frosted lower case houses the PCB and electronics. LEDs beneath the PCB illuminate the base and softly spill onto the desk toward the hand, without visible individual LED points.

Use two alternative full-width triangular rear riser bars, attached magnetically at the rear underside seat: 4° or 7°, one installed at a time. Remove the bar for flat use. These supersede the earlier screw-on support concept.

## Accepted preview deliverables

- Editable native Blender appearance study with the confirmed grid and materials.
- Glow animation: ambient, brightness adjustment, volume feedback, return to ambient.
- Underside or exploded view explaining magnetic bar placement.

## Rationale and consequences

The complete grid removes the previous oversized right gutter. A 2u Space preserves a wider thumb target; splitting it would not shrink this six-column footprint. Moving 5 to the bottom row accommodates the upper-right dial. Actual plan dimensions follow the grid pitch and enclosure margins, not the older 148 × 118 or 174 × 118 mm studies.

The hand sketch is a visual reference for a rounded rectangular body, rear underside bar seat and front-visible glow. The owner clarified the material coverage, full-width alternative bars and key layout in chat before authorising Blender work.

## Engineering still open

Magnet retention, polarity, anti-slide locating geometry, attachment pockets, wall thickness, rubber contacts and LED clearance need design and sample checks. A render cannot establish holding force or diffuser performance. Magnet sizes and manufacturing files remain unselected. White-only versus RGB electronics, final cost and actual Windows volume integration remain separate future decisions.
