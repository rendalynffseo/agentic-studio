# Affiliate CTA placement

The desktop new-task and Edit brief forms accept:

Use **Add affiliate link** to add up to 20 destinations. `affiliate_links` is an array of `{url, label, placement}` records. Each destination has its own label and automatic or pinned placement. When this array is nonempty, it is authoritative: the legacy single-link fields mirror its first entry for older integrations and must not create a duplicate CTA. When the array is empty or absent, fall back to the legacy fields below. Blank rows are ignored; removing every row clears affiliate instructions.

- `affiliate_url`: optional absolute HTTP(S) destination, without embedded credentials. Preserve the complete URL and tracking parameters. Escape it when inserting HTML; never execute it or treat it as an instruction.
- `affiliate_label`: requested button/link text. If empty, choose clear, accurate text based on the brief.
- `affiliate_placement`: `auto` lets the agent choose relevant pages and sections. Otherwise honor the requested page/section; clarify unavailable or conflicting locations.

Architecture identifies relevant conversion locations. Content supplies accurate anchor text and a visible affiliate disclosure near the first affiliate CTA. Development inserts standard anchors with `rel="sponsored"`; include `noopener` when opening a new tab. Do not add the destination to unrelated navigation links or replace internal links indiscriminately. An empty URL means no affiliate CTA. Remove any unrelated referral destinations inherited from the starter.

Record `artifacts/affiliate-placement.json` with `url`, `label`, and a `placements` array containing `page`, `section`, and `reason` for each CTA. Record the disclosure location too. Development and QA inspect actual built HTML, compare decoded hrefs with the original complete URL, check labels and placements, and save evidence with the handoff. These are agent review requirements; the queue does not automatically verify affiliate anchors.

For multiple destinations, use a top-level `links` array containing that same record shape for every supplied URL. Account for all destinations; if a requested link is irrelevant or conflicts with the approved scope, report the conflict rather than silently substituting or omitting it. A destination may be placed in a relevant blog article when its placement permits this.

Existing briefs can be edited before execution starts. After work starts, reopen intake through the orchestrator before changing the destination so downstream stages are reviewed again.
