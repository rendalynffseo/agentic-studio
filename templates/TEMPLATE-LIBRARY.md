# Automatic template selection

All 13 templates from the user's gallery are installed under `vendor/templates/library/`. The full ZIP and source-file hashes are retained. The agent can work from the local source without downloading a template for every job.

Create a task normally in Agentic Studio. `workflow.mjs init` ranks the installed templates from the brief, saves `artifacts/template-selection.json`, and records a **template_selected** activity event. The desktop app uses this same queue command, so no desktop rebuild is needed.

`design_template_id: "auto"` gives the agent the choice. `design_selected_template_id` records the result, while `design_template_name` and the selection report make it readable. An explicit ID such as `t8` pins the user's choice. Existing completed/deployed jobs are not silently switched.

## What the agent considers

| ID | Template | Useful visual/layout signals |
| --- | --- | --- |
| t1 | Promo Landing | One-page layout, red/gold, campaign-style hero |
| t2 | App Guide | Documentation, app explanations, reading sidebar |
| t3 | Casino Lobby | Navy catalog, sidebar, portrait cards |
| t4 | Casino Portal | Orange/light portal, category pages |
| t5 | Teal Glow | Teal/gold gradients, carousel, section chips |
| t6 | Green Lobby | Green/yellow directory, tabs, navigation |
| t7 | Green Dashboard | Dashboard, search, three-column workspace |
| t8 | Royal VIP | White/purple/gold, tabs and tiles |
| t9 | Free Credit | Charcoal/yellow, comparison tables and grids |
| t10 | Rose Lounge | Cream/rose/maroon, magazine-style bands |
| t11 | Neon Teal | Navy/neon teal, comparison grid |
| t12 | Red Gold Guide | Red/black, searchable articles and topic clusters |
| t13 | Sky Glow | Sky blue, glossary and knowledge base |

Names identify the source templates. Imported copy, links, identities, trackers, and deployment instructions must be adapted to the approved task scope. Choosing a visual template does not authorize publishing its starter content.

The ranking uses purpose, palette, and layout rules in `config/template-profiles.json`. It is a reproducible recommendation, not an AI worker run or a prediction of rankings, CTR, safety, or performance. Weak/tied matches are identified; a brief with no useful signals gets a provisional fallback. The planning agent reviews the report and may record a reasoned override for automatic choices.

Optional preferences in a brief:

```json
{
  "design_template_id": "auto",
  "design_preferences": {
    "site_type": "dashboard",
    "palette": ["green", "gold"],
    "layout": "three column"
  }
}
```

Free-text task instructions also contribute signals. You do not need to fill these fields for every task.

## Agent commands

```powershell
npm run templates
node scripts/template-agent.mjs recommend --brief path/to/brief.json
node scripts/template-agent.mjs choose --job jobs/my-task
node scripts/template-agent.mjs choose --job jobs/my-task --template t13 --reason "The approved architecture is a glossary."
node scripts/template-agent.mjs prepare --job jobs/my-task
```

`list` verifies the archive and all imported source files. `recommend` is read-only. `choose` refreshes the task's selection report and event; an override cannot replace an explicit user pin. `prepare` verifies the selected source and saves the original CSS/provenance for the developer. It does not execute a downloaded script, build the site, or publish anything.

The developer must read/adapt the selected source, write `artifacts/template-adaptation.md`, and include the provenance as the stage-07 deliverable's `design` object. Completion checks match the selected ID, library version, installed source hash, and selection evidence. Reopen stage 07 before changing a template once implementation has started or passed review.

## Refresh the library

When the gallery changes, review its live catalog and profiles, download the new complete ZIP to `vendor/templates/catalog-all.zip`, then run:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts/import-template-library.ps1
node scripts/index-template-library.mjs
npm run templates
```

The importer checks paths, duplicates, symlinks, size, and file hashes before accepting the library. It uses a bundle-hash version directory and preserves earlier versions. Downloaded scripts are not run. Older selections must be reviewed against the new version before completing a new design stage.
