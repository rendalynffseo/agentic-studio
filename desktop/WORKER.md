# Run agents without VS Code

1. Open Agentic Studio, create or select a task, and choose **Start / continue task**. **AI** in the left rail also opens worker settings.
2. The panel detects `codex.exe` and checks its signed-in account. VS Code does not have to be running, even if the detected executable was installed with its extension. You can choose a separate Codex CLI executable with **Choose engine**. Node.js must be installed on PATH.
3. If needed, choose **Sign in** and follow the one-time device sign-in instructions shown in the panel. Account credentials stay with the Codex CLI; the app does not ask for or store an API key. Device sign-in output is not saved to task logs.
4. Click **Start / continue**. A new hidden Codex process performs the next role and saves its deliverable. The desktop independently checks the evidence before starting the next separate process. Progress and robot activity follow the real queue.

**Pause after current agent** lets the active role finish and then stops handoffs. **Stop worker** terminates the active process tree, preserves partial files, and marks interrupted work for review. Review failures, use **Retry current task** in the main panel, and Start again. Ordinary internet/account usage limits and normal execution permissions still apply; the worker does not bypass sandboxing or approvals. Missing access is reported as a blocker rather than a fake completion.

Closing the worker panel while work is active hides it; the main app keeps running. Open it again with AI. Pause or stop before closing the main app. A workspace lock prevents another window from launching duplicate workers. A reopened panel can read the active job log and send pause/stop controls to its existing desktop worker. If a stage was interrupted and no worker remains, **Recover interrupted stage** marks it failed for review after your confirmation; it does not delete files or automatically retry it.

Task data, logs and worker status stay in `jobs/<id>/`. Engine path settings are local in `desktop/worker-settings.json`. These files are excluded from GitHub. The runner never treats an engine's successful exit or text claiming success as evidence that the job completed. Failed, missing or invalid deliverables stop the handoff.

Desktop runs use `codex --search exec --json --sandbox workspace-write ...`; model choice comes from your existing Codex configuration. No bypass or full-access flags are used. Each task's deployment authorization remains binding; a local build is not a published site.

Diagnostics: `node scripts/desktop-worker.mjs doctor`. Automated runtime tests are part of `npm test`. The explicitly invoked `node scripts/test-desktop-worker-live.mjs --run` uses the signed-in model for one temporary intake task, validates its real artifact, and removes that isolated task; it is not part of normal tests or app startup.
