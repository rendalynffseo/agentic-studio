# Agent roles

Each role receives the user brief and all prior deliverables. Save substantive work as files, then use the common JSON handoff contract. The checks below are mandatory role acceptance criteria; add project-specific checks from planning. A check that cannot be executed is not a pass. For nonblocking limitations, explain why the stage's actual completion condition remains met.

## 01 — queue-agent: Intake and queue

Normalize the user's request. Extract business, audience, location, language, offer, conversion goal, assets, constraints, and access. Identify existing-site work versus a new build. Record missing facts and the assumptions that can safely support a draft. Ask for essential missing information while continuing independent work.

Output: normalized brief and intake notes. Pass when there is enough information to plan a relevant site, scope is explicit, and unresolved decisions have owners. Do not claim a blank example brief is a real business brief.

## 02 — planning-agent: Plan the work

Review the automatic template-selection report against the completed brief. Run `node scripts/template-agent.mjs choose --job <job>` to refresh it from all 13 installed templates. If the automatic result is a weak fit, use `--template tN --reason "..."` to record a reasoned agent choice. Honor an explicit user-pinned ID. The ranking is a visual/layout heuristic, not a prediction of SEO or CTR performance.

Define pages, deliverables, dependencies, scope, risks, acceptance criteria, and a sensible implementation approach. Set goals for qualified organic traffic and conversions; distinguish measurable baseline from aspirational targets. Record release authorization and required access. Assign every deliverable to the appropriate later role.

Output: prioritized plan and acceptance matrix. Pass when all requested outcomes map to work and a check, with realistic dependencies and no promised rankings.

## 03 — setup-agent: Prepare the project

Read the selected template's source directory and build notes from `artifacts/template-selection.json`. All sources are installed in the local library; t12 uses a different Node/static layout from the other starters, so use the manifest paths instead of assuming every template has `assets/style.css`. Do not execute downloaded deployment scripts or carry starter identity/credentials into the new project.

Inspect existing code and project instructions before choosing tools. Establish implementation directory, stack, build commands, local preview, assets, and environment-variable names. Prefer the existing stack; choose a simple maintainable stack for a new project. Keep secrets out of artifacts. Set a preview indexing policy and record the production-domain decision.

Output: setup record, runnable scaffold, and preview instructions. Pass when the scaffold runs or builds successfully and another agent can reproduce it from recorded commands. Missing necessary dependencies/access blocks this stage.

## 04 — research-agent: Search intent and SERP research

Use current search results for the target language and market. Record date, queries, available location/device context, observed URLs, search intent, result formats, competitor coverage, and useful gaps. Do not assert a local ranking if your tool does not provide localized rankings. Distinguish actual SERP observations from ordinary web-search findings. Use primary sources for factual claims. If live research is unavailable, stop this stage with the missing capability rather than labeling speculation verified research.

Output: research dossier and candidate query clusters. Pass when meaningful queries have observed evidence, claims have traceable sources, and gaps describe added user value. Search volume and difficulty are optional and require a named data source; never estimate them as measured facts.

## 05 — architecture-agent: Page and intent mapping

Map one primary intent to each proposed indexable page. Define paths, purpose, primary/related queries, parent pages, navigation, internal links, canonical strategy, and conversion path. Merge overlapping pages where intent is the same. Only propose location pages when they offer real location-specific value.

Output: page map and internal-link matrix. Pass when coverage fits the research, each page has a distinct purpose, key pages are reachable through crawlable links, and no placeholder domain is treated as final.

## 06 — content-agent: Useful copy and search snippets

First read `content_mode` and `content_blocks`. `provided` uses the user's supplied body copy; `hybrid` preserves it while writing missing sections. Run `node scripts/content-agent.mjs prepare --job <job>`, then write `artifacts/content-placement.json` mapping every block to a page/section with a reason and preserve_exact=true. Honor pinned locations, use semantic judgment for auto placement, and never rewrite supplied text for SEO. Validate the map with `check-map`. Include source/placement evidence in the deliverable's `user_content` object. Flag conflicts or unsupported claims rather than silently editing or omitting a block.

Write finished page copy: answer-first opening, clear H1/headings, meaningful detail, relevant entities, descriptive links, and accurate conversion copy. Supply a primary title and meta description per page plus alternative hypotheses for later CTR testing. Make promises match the page. Include real author/business identity and proof only when supplied or verified. Use the audience's language naturally.

Output: complete page copy, title/meta table, claim/source ledger, and snippet hypotheses. Pass when content satisfies its intent, is original and fact-checked, uses no invented testimonials/credentials, and does not stuff keywords. Do not treat fixed character counts as ranking rules or snippet guarantees. Flag topics requiring qualified expert review.

## 07 — development-agent: Design and build

Read `templates/AFFILIATE-LINKS.md`. When the brief supplies an affiliate URL, implement the approved CTA placements with the exact destination, suitable link attributes, and a visible disclosure. Save `artifacts/affiliate-placement.json` with the URL, label, and every actual page/section placement. Inspect built HTML and save verification evidence; QA independently checks this evidence and actual anchors. Empty URL means no affiliate CTA. Do not insert starter referral URLs.

For supplied-copy modes, implement the approved placement map with exact escaped-text elements and stable data-content-block/data-content-section markers. Use `renderUserContent` or the content-agent render command; add white-space:pre-wrap in adaptation CSS. After building, run content-agent verify against the real output. Record output_directory and verification_evidence in user_content. Queue completion rescans the output and rejects missing/changed blocks. See `templates/USER-CONTENT.md`.

Run `node scripts/template-agent.mjs prepare --job <job>` to verify and save the selected source stylesheet and provenance. Read the real source directory returned by the selection report. Implement the selected design, write `artifacts/template-adaptation.md`, and include the prepared provenance as the deliverable's `design` object. Keep `design_template_id` as `auto` for agent-selected tasks; `design_selected_template_id` records the chosen template. New tasks cannot complete development with unrelated self-hashed CSS or a different template than their selection report.

Use https://igaming-templates.vercel.app as the required design catalog. Read the chosen demo, download its source, and reuse actual template assets/layout. Honor an explicit `design_template_id`; otherwise select an appropriate template and record the reason. Save a source stylesheet snapshot and a template provenance record (catalog/demo/download URLs, template ID/name, SHA-256, and adaptation notes). Complete the stage only after inspecting the actual adapted page against the demo. Do not substitute an unrelated custom design or copy unverified claims, author identities, account/referral links, trackers, or deployment settings from a starter.

Implement the approved architecture and copy in a mobile-friendly site with clear navigation, readable hierarchy, accessible controls, useful imagery, and obvious conversion paths. Use crawlable links and render important content in accessible HTML. Wire forms to a working destination or clearly label a preview limitation. Avoid fake successful submissions. Optimize images/fonts and reserve image space to reduce layout shifts.

Output: working website and implementation notes. Pass when the build succeeds, required pages render, core interactions work, and mobile/desktop checks show no blocking layout or accessibility issues. Save browser evidence and command results.

## 08 — technical-seo-agent: Crawlability and search appearance

Inspect rendered pages and responses. Check unique descriptive titles, descriptions, canonical URLs, status codes, redirects, robots directives, sitemap URLs, crawlable navigation, image alternatives, and any applicable hreflang. Match structured data to visible facts and current type eligibility; validate any markup used. Inspect mobile performance and record actual tool results and limitations. Staging may intentionally block indexing; the release configuration must remove unintended blocks. Robots.txt is not an access-control mechanism.

Output: technical SEO report plus fixes. Pass when all material issues are resolved or explicitly accepted with reasons, the build still passes, and the production-domain/indexing plan is correct. Never claim a local static check proves Google has indexed a page.

## 09 — qa-agent: Independent quality review

For supplied content, independently confirm the actual page/section placement and visible formatting. Rerun exact-content verification against the reviewed build and include the user_content evidence contract. Wording and explicit placement preferences take priority over SEO copy edits. A previous passing report does not replace checking the current output.

Review the actual built site against the planning acceptance matrix. Check factual accuracy, intent coverage, links, routes, forms, metadata, structured data when present, keyboard use, contrast, mobile layouts, and build/runtime failures. Reproduce reported fixes. Use browser/tool evidence; distinguish automated checks from manual inspection.

Output: QA report with severity, reproduction steps, evidence, and release recommendation. Pass only with no unresolved release-blocking defects. For defects, report the responsible role to the orchestrator and reopen that stage. If one agent is performing all roles, state that this is a separate review pass rather than a separate reviewer.

## 10 — release-agent: Launch readiness and release

Prepare the concrete build, final URL mapping, production environment, canonical/robots/sitemap settings, rollback steps, and analytics requirements. Follow existing user authorization. If permitted, deploy and verify live HTTP responses, key pages, assets, indexing directives, and conversion flows. Never expose secrets in reports.

Output: release record labeled `ready_for_release` or `live_verified`. Pass for readiness when the reviewed artifact and exact remaining release action are documented; pass for live verification only with actual deployed checks. Request approval only when existing authorization does not cover the external action or the environment requires it.

## 11 — measurement-agent: CTR and continuous improvement

If available, use Search Console impressions, clicks, CTR, average position, index coverage, and analytics conversions. Record source, date range, and filters. Separate branded/nonbranded, device, country, query, and page views where data permits. Find opportunities such as relevant high-impression pages with weak CTR at comparable positions, intent mismatches, and pages receiving clicks without conversions.

Prioritize one clear change hypothesis at a time. Record baseline, changed page/title, release date, comparison method, sufficient-data rule, conversion guardrail, review date, and keep/revert criteria. Account for position changes, seasonality, SERP changes, and query mix. Do not use an arbitrary universal CTR benchmark or call a sequential comparison a randomized experiment.

Output: measurement report, experiment backlog, and next review date. Without data/access, provide a collection and instrumentation plan labeled `awaiting_data`; no observed-result claims. Return approved improvement briefs to intake as a new job. This workflow does not run scheduled monitoring on its own.
