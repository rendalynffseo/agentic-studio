# Start your first website job

## Windows desktop app

Double-click **Agentic Studio.exe** or **Start-Agentic.cmd** in this workspace. The native desktop app shows a 3D agent operations room, live queue stages, task briefs, activity, and deliverables. It works without a browser or local HTTP server. See [desktop instructions](desktop/README.md).

## Run agents from the desktop

Create or select a task, open **Start / continue task**, confirm the engine is signed in, and click **Start / continue**. VS Code can remain closed. The native AI worker provides live output, pause, stop, sign-in and engine selection. See [worker instructions](desktop/WORKER.md).

## Optional browser dashboard

Run `npm start` from this workspace, then open **http://127.0.0.1:4311**. Keep the server running while using it. The dashboard reads real job files every three seconds, shows agent stages and activity, opens saved deliverables, and lets you save the initial brief and retry failed intake. It binds only to this computer.

The dashboard does not launch AI workers. After saving your brief and retrying intake, ask your coding agent to continue the job. Changes made by that agent appear automatically. It does not display simulated completion or SEO metrics.

## Run a job

All 13 gallery templates are installed locally. A new task automatically gets a ranked template choice and a saved selection report. Give the task's purpose and any color/layout preferences; the agent can choose without asking you for a template ID. See [automatic template selection](templates/TEMPLATE-LIBRARY.md).

New jobs inherit the design catalog at `https://igaming-templates.vercel.app`. The agent chooses a suitable template automatically. To choose explicitly, set `design_template_id` in the brief (`t1` through `t13`); for example, `t2` is App Guide. The current Gaming App King site uses that dark ink-and-gold template.

Fill in `templates/brief.json` or make a copy for your business. Then run:

```powershell
node workflow.mjs init --brief templates/brief.json --job jobs/my-site
node workflow.mjs next --job jobs/my-site
```

For an external coding-agent runner instead of the native worker, use this optional prompt:

```text
Execute the SEO website workflow for jobs/my-site.
Read ORCHESTRATOR.md and agents/roles.md first.
Use workflow.mjs to claim, validate, and complete stages sequentially.
Use separate worker agents for the roles if your environment supports them;
otherwise perform the roles as separate sequential passes and disclose this.
Save real deliverables and evidence before each handoff.
Ask only for essential missing business information and continue independent work.
Follow the brief and my existing authorization for external actions.
Finish with the website location, release status, QA findings, and measurement plan.
```

Queue validation can be rerun with:

```powershell
node --test workflow.test.mjs
```

These tests verify handoff control, evidence requirements, failure/retry behavior, and downstream invalidation. They do not verify the quality or rankings of any generated website.
