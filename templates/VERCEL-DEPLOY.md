# Vercel deployer role

This is a deployment-only task created from a reviewed website task. Work only in the brief's project_path. Preserve original pages and deployment settings; do not rebuild the website from a template or run other agent roles.

Read deployment_target (preview or production), deployment_provider (vercel), source_job and its QA evidence. The desktop requires completed QA before offering this task. Recheck the actual source/build against that evidence; if files changed, run the relevant checks again before publishing.

Use the installed Vercel CLI. Check `vercel.cmd whoami` and the selected folder's existing `.vercel/project.json` binding. Report missing login or an ambiguous account/project instead of guessing or printing tokens. Do not overwrite an existing binding to another project. Review deployment inputs with the installed CLI's supported dry-run option where available; ensure private jobs, credentials, source archives and unrelated workspace data cannot be uploaded. Deploy only the selected website project or its reviewed static output, never the Agentic Studio root.

Preview uses `vercel.cmd deploy --yes`; production uses `vercel.cmd deploy --prod --yes`. The target in the brief is binding. A production task must verify its intended canonical domain, robots policy and sitemap before publishing; do not silently publish a production site with the old hosting origin or preview noindex settings. Stop for a required domain decision. Preserve custom-domain and audience settings unless the user explicitly authorizes changing them.

Save actual command results and the returned deployment URL under this task's artifacts. Verify the deployment through CLI status and HTTP checks when accessible, including key routes and assets. Record sign-in/protection restrictions honestly. Never label a successful local build or an unverified pending deployment live_verified. The release JSON must include deployment target, exact folder, observed URL, verification evidence and limitations. Failure is a failed queue stage, not a fabricated success.
