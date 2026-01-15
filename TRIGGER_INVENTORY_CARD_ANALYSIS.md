# Trigger Inventory + Change Card - Cognitive Overload Analysis

## Context
The current card uses a strong title, three step sections, tinted backgrounds, and repeated labels. The user feedback is that the title is visible but the inside text is not, and the card feels cognitively overloaded.

## Findings (ordered by impact)
1) No single visual entry point after the title. The eye hits the header, then sees three equally weighted blocks with similar size, border weight, and padding, so there is no obvious "next" action.
2) Primary action and recommended trigger compete. Both are highlighted with emphasis colors and step badges, so the user cannot immediately tell which line is the decision vs supporting inventory.
3) Redundant information increases load. The recommended trigger name appears in the action block and again in the recommended block, forcing re-reading without new information.
4) Label/value contrast is too low. Labels and values use similar size and weight, making scanning hard (e.g., "Set Data Tag trigger" vs the trigger name).
5) Excess tinting reduces legibility. Three separate colored blocks create visual noise and reduce text contrast in a dark UI.
6) Secondary inventory is not clearly optional. "Other Available Triggers" looks equally important because it is a full block with a header, border, and badge.
7) The "Keep ce_purchase as a dedicated purchase trigger" instruction is ambiguous. It does not explicitly attach to the current trigger name, so it reads like a generic rule.
8) Low-signal metadata is repeated. "Used by 0 tags" is shown in multiple places; repeated zero-value data increases noise without added clarity.

## Usability Gaps
- The card mixes two tasks in one plane: "Do this now" vs "Reference inventory." Without a stronger separation, users must parse both at once.
- The action block is not visually dominant even though it is the decision point.
- The recommended trigger is presented as a separate section instead of a direct choice in the action line, which forces context switching.
 - Primary, secondary, and tertiary content are not visually distinct; all sections use similar borders, spacing, and headings.
 - The eye has no clear "next step" indicator after the title, so scanning stalls.

## Recommendations (design intent, not implementation)
- Create a single action line as the dominant element: "Confirm Data Tag trigger -> ce_ecom (ID 307)" and a secondary line "Keep ce_purchase as a dedicated purchase trigger (if needed)."
- Downshift inventory into a collapsed or smaller "Reference" area with lighter styling and a compact count (e.g., "Other triggers (1)").
- Use stronger typographic contrast: value in bold/larger size, label in muted small text.
- Remove repeated trigger names where possible; the action line should be the only place that states the new trigger.
- Hide zero-usage rows by default or group them under a "Show unused triggers" toggle.
- Make Step badges smaller or replace with a single "Now" vs "Reference" separator to reduce competing signals.

## Minimalistic Hierarchy Plan
Primary (main object):
- One action block only. One sentence, one decision. Example: "Confirm Data Tag trigger: ce_ecom (ID 307)."
- Secondary line: "Keep ce_purchase as a dedicated purchase trigger (if needed)." Keep it short, no extra metadata.

Secondary (supporting evidence):
- One recommended trigger card with only the trigger name and a single usage note if non-zero.
- No duplicate trigger name outside this card.

Tertiary (reference inventory):
- Collapsed by default. Title shows count, e.g., "Other available triggers (1)".
- Only show usage if > 0. Hide zero-usage rows unless expanded.

## Success Criteria
- A user can answer "What do I change?" in under 3 seconds without reading the inventory.
- The recommended trigger is visible but does not compete with the action line.
- Reference inventory is available but optional. Nothing else steals attention.

## Gaps Against Current Image
- The "STEP" pills add a competing visual system on top of the card title, so the eye bounces between badges and sections instead of following a single path.
- The Action row labels and values are the same weight and size, so the target trigger does not stand out as the decision.
- The recommended trigger card repeats the same trigger name immediately after the action block, creating redundancy without added clarity.
- Three colored blocks in a small space create low contrast boundaries; the card reads as busy rather than structured.
- The "Other Available Triggers" block looks as important as Action because it has a full header, border, and status badge.
- Status chips (UPDATE/KEEP) add micro-labels that compete with the actual instruction text.

## Improvements Specific To This Card
- Replace "STEP" pills with a single hierarchy: Action (primary), Recommended (secondary), Reference (tertiary).
- Make the action value the only bold, high-contrast element inside the card; keep labels small and muted.
- Remove repeated trigger name from the recommended block if it is identical to the action line; keep only usage evidence there.
- Use one accent color total (orange for action) and grayscale for the rest to avoid color competition.
- Collapse or minimize the "Other Available Triggers" section by default with a simple count label.
- Move UPDATE/KEEP into a single status line or remove them entirely if the action text is clear.
