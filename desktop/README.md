# Agentic Studio for Windows

Double-click **`Agentic Studio.exe`** in the workspace root, or use **`Start-Agentic.cmd`**. This is a native WPF desktop window with a native 3D scene; it does not embed a browser, use Electron, or need the dashboard server.

Keep the executable in this workspace: it uses the adjacent queue scripts, `desktop/Theme.xaml`, templates, and `jobs/` directory. Requires Windows .NET Framework 4.x and Node.js 18+ on PATH. These were available on this computer when built.

## Use the room

New tasks use a specialist team with one assigned worker per role: 14 core agents and up to four optional agents for blog strategy, blog writing, affiliate placement, and exact-content placement. Open **Agent team** for individual responsibilities, instructions, status, and handoff recipients. **Copy this agent task** gives the next worker its inputs, required outputs and commands. The external coding agent runner performs the work; the desktop does not launch model processes.

Each assigned role has its own robot. Optional roles absent from the task are hidden. Only the role with a real running queue task shows working activity. Existing queued tasks offer **Use specialist team** before execution begins; active and completed tasks keep their existing assignments.

New tasks automatically choose from all 13 installed source templates. The choice appears as a **TEMPLATE SELECTED** event and `template-selection.json` deliverable. Include your preferred palette or layout in the task instructions to guide the selection. The planning agent reviews the choice before development. This behavior is supplied by the queue script, so the existing desktop executable picks it up without a rebuild.

### Move around

- **Left-drag** empty room space to orbit and tilt the view. Choose **Move** to make left-drag pan instead.
- **Right-drag, middle-drag, or Shift + left-drag** pans the view.
- **Scroll** to zoom, or use the **− / ＋ buttons and zoom slider**. Zoom is limited to 55–190%.
- **Reset view**, **R**, or double-click empty room space restores the camera.
- When the scene has keyboard focus: arrow keys rotate/tilt, Shift + arrows pans, + / − zooms, and Space toggles motion.
- Touch manipulation supports pan, pinch zoom, and rotation. Physical touch gestures were not verified on this computer.

### Agents and motion

Every station has a robot with articulated arms, legs, head movement, and blinking indicators. Standby robots patrol locally; blocked robots wait with amber eyes. A station with an actual `running` task sends its robot to a desk, animates typing, and shows moving activity packets along its corridor. Those work packets stop when the task is no longer running. Completed stations show green robot indicators.

Station labels distinguish **Standby**, **Needs input**, **Working**, and **Complete**. The robots' ambient movements are decoration, not progress or evidence that an AI worker is connected. The queue counters and agent statuses remain authoritative.

**Motion: on/off** pauses or resumes the robots and rotating hub. Camera controls continue to work while motion is paused. Animation updates are skipped while the app is minimized.

### Manage tasks

Use **Content writer** to paste your own copy. Choose exact supplied content or supplied content with agent-written gap sections. Add multiple blocks and leave page/section on auto for the agent to decide placement. Saving requeues stage 06 and later checks; it does not publish changes. The same option is included in New task. See [user-content instructions](../templates/USER-CONTENT.md).

- **New task** opens a native website brief form. Enter the website name, business/topic, and offer. Creating a task initializes a real queue job.
- Click **Dock, Planning, Research, Review, Work, or Complete** to filter the agent handoffs. The number at a station is the number of unfinished stages assigned there; it is not a count of active AI processes.
- The top counters show completed stages, tasks actually marked running, and failed tasks needing attention. There are no simulated usage, ranking, or performance numbers.
- **Edit brief** edits a job before execution starts. Saving a previously failed intake brief returns it to the queue.
- **Open folder** opens the actual job folder. Deliverables open as text in a native window; HTML is not executed.
- The app checks the job files every two seconds. Keep your coding agent working on the selected job and watch its actual handoffs appear.

The app is a queue monitor and brief editor. An AI worker service is not connected, so it does not execute research or build sites on its own. To execute a task, give your coding agent:

```text
Continue jobs/<job-id> using ORCHESTRATOR.md.
Execute roles sequentially and save real evidence before completing each stage.
```

Like the CLI queue, use one writer/orchestrator at a time. The brief locks when any task has started or completed; ask the orchestrator to reopen intake before revising work that has already begun. The app does not publish or deploy sites.

## Rebuild

Close Agentic Studio before rebuilding:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File desktop/build.ps1
```

The compiler is the Windows .NET Framework compiler; no dependency download or administrator installation is required. The executable is unsigned, so Windows may identify it as an unrecognized app when moved to another computer.

The native data/interoperability check is `Agentic Studio.exe --self-test`; it saves `desktop/self-test-result.txt`. Queue and local dashboard tests remain available with `npm test`.

`Agentic Studio.exe --scene-test` checks camera transforms, station projections, zoom limits, robot movement, queue-linked work effects, and animation toggling without changing jobs. `desktop/check-ui.ps1` verifies physical mouse orbit/pan/zoom and native controls against an open app; it briefly moves the pointer during the check.
