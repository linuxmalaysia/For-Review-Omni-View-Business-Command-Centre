---
title: "Jules Turndown & Antigravity Transition Closet"
description: "Historical record of Google Jules turndown and agentic migration to Google Antigravity."
type: "spatial_closet"
id: ".agents/brain/wings/wing_omni_view/hall_events/room_brain_history/closet.md"
dsom_governance:
  domain: "AI"
  context_tier: "L2-Detail"
tags:
  - "closet"
  - "jules"
  - "turndown"
  - "antigravity"
  - "history"
  - "export"
topics:
  - "closet"
  - "jules"
  - "turndown"
  - "antigravity"
  - "history"
  - "export"
related_links:
  - ".agents/brain/palace_registry.md"
  - ".agents/AGENTS.md"
  - "HISTORY.md"
  - "CHANGELOG.md"
nav_order: 7
layout: "default"
---

# 🚪 Room Closet: Jules Turndown & Google Antigravity Transition

## 📅 Turndown Timeline & Milestone Dates

- **Announcement Date:** October 29, 2026
- **Session Availability Window:** Users have until November 11, 2026 to continue finishing up sessions.
- **Read-Only Transition:** After November 11, 2026, Jules turns to read-only mode until the end of the year.
- **Official Wind Down:** December 31, 2026

## 🚀 Successor Platform: Google Antigravity

Jules was launched as an experiment to explore how asynchronous coding agents empower engineering teams to tackle backlogs and accelerate delivery. Learnings and agentic patterns pioneered by Jules are directly integrated into Google's agent-first platform: **Google Antigravity**.

Future autonomous agent sessions, architectural reviews, and memory sync operations transition to Google Antigravity.

---

## 💾 Jules Data Export Protocol

Users and autonomous agents can export all data known to Jules into a private local directory:
- Account settings (`user-settings.json`)
- Environment variables (`env-variables.json`)
- Scheduled tasks (`scheduled-tasks.json`)
- Connected repositories (`sources.json`)
- Memories per repository (`memories.json`, `memories.md`)
- Latest setup scripts (`setup.sh`) and test commands (`test-command.txt`)
- Complete session histories (`session.json`, `activities.json`, `patch-*.diff`, `summary.md`)

### Setup Instructions

1. Install Jules CLI:
   ```bash
   npm install -g @google/jules
   ```
2. Authenticate:
   ```bash
   jules login
   ```
3. Connect GitHub Account:
   Ensure GitHub target is linked at `https://github.com/apps/google-labs-jules/installations/select_target`.

### Export Script (`jules_export.py`)

To run the export:
1. Save the Python script below to a file in your user home directory (e.g. `~/jules_export.py`).
2. Run the script using Python 3:
   ```bash
   python3 ~/jules_export.py
   ```
3. The script exports all data into a dedicated, user-restricted destination outside the repository (`~/jules-export`) with strict directory permissions (`0700`).

```python
import base64, json, os, pathlib, re, subprocess, sys, urllib.error, urllib.parse, urllib.request


def get_token():
    for cmd in [["security", "find-generic-password", "-s", "jules-cli", "-a", "default", "-w"],
                ["secret-tool", "lookup", "service", "jules-cli", "username", "default"]]:
        try:
            out = subprocess.check_output(cmd, stderr=subprocess.DEVNULL).decode("utf-8").strip()
            if out.startswith("go-keyring-base64:"):
                out = base64.b64decode(out.split(":", 1)[1]).decode("utf-8")
            if out:
                return json.loads(out)["access_token"]
        except Exception:
            pass
    p = pathlib.Path.home() / ".jules/cache/oauth_creds.json"
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))["access_token"]
    sys.exit("Run `jules login` first.")


TOKEN = get_token()
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
RPC = "https://aida.googleapis.com/$rpc/language_labs.aida.swebot.proto.SweBotService"
REST = "https://aida.googleapis.com/v1/swebot"

# Export outside of the repository to user's home directory with secure permissions
OUT = pathlib.Path.home() / "jules-export"
OUT.mkdir(mode=0o700, parents=True, exist_ok=True)
try:
    os.chmod(OUT, 0o700)
except Exception:
    pass

errors = []


def rpc(m, b=None):
    req = urllib.request.Request(f"{RPC}/{m}", data=json.dumps(b or {}).encode("utf-8"), headers=HEADERS, method="POST")
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode("utf-8") or "{}")


def get(path, **params):
    q = ("?" + urllib.parse.urlencode(params)) if params else ""
    with urllib.request.urlopen(urllib.request.Request(f"{REST}{path}{q}", headers=HEADERS), timeout=60) as r:
        return json.loads(r.read().decode("utf-8") or "{}")


def paged(fetch, key):
    items, token = [], None
    while True:
        resp = fetch(token)
        items += resp.get(key, [])
        token = resp.get("nextPageToken")
        if not token:
            return items


def safe(s):
    return re.sub(r"[^a-zA-Z0-9._-]", "_", s)


def dump(path, obj):
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2), encoding="utf-8")
    try:
        os.chmod(path, 0o600)
    except Exception:
        pass


# Account-level data
dump(OUT / "user-settings.json", rpc("GetUserSettings"))
dump(OUT / "env-variables.json", rpc("ListEnvironmentVariables"))
dump(OUT / "scheduled-tasks.json", rpc("ListScheduledTasks"))

# Repos (sources) and their memories
sources = paged(lambda t: rpc("ListSources", {"pageSize": 100, **({"pageToken": t} if t else {})}), "sources")
dump(OUT / "sources.json", sources)
mem_repos = 0
for src in sources:
    sid = src.get("sourceId") or src.get("id") or src.get("name", "").removeprefix("sources/")
    try:
        mems = paged(lambda t: rpc("ListMemories", {"sourceId": sid, "pageSize": 100, **({"pageToken": t} if t else {})}), "memories")
    except urllib.error.HTTPError as e:
        errors.append(f"memories {sid}: HTTP {e.code}")
        continue
    if mems:
        mem_repos += 1
        d = OUT / "repos" / safe(sid)
        dump(d / "memories.json", mems)
        mem_text = "# Memories\n\n" + "\n".join(
            f"- {m.get('Fact') or m.get('fact') or m.get('content')}" for m in mems if not m.get("archived")
        ) + "\n"
        mem_file = d / "memories.md"
        mem_file.write_text(mem_text, encoding="utf-8")
        try:
            os.chmod(mem_file, 0o600)
        except Exception:
            pass

# Sessions: full detail, activity log, patches, and a readable summary
sessions = paged(lambda t: get("/tasks", pageSize=100, **({"pageToken": t} if t else {})), "tasks")
dump(OUT / "sessions.json", sessions)
setup = {}  # latest setup script / test command seen per repo
patches = 0
for s in sorted(sessions, key=lambda s: s.get("createdAt", "")):
    tid = s["id"]
    d = OUT / "sessions" / tid
    try:
        task = get(f"/tasks/{tid}").get("task", {})
        acts = paged(lambda t: get(f"/tasks/{tid}/activities", pageSize=100, **({"pageToken": t} if t else {})), "activitySteps")
    except urllib.error.HTTPError as e:
        errors.append(f"session {tid}: HTTP {e.code}")
        continue
    dump(d / "session.json", task)
    dump(d / "activities.json", acts)
    commits = [o["gitCommit"] for o in task.get("outputs", []) if "gitCommit" in o]
    for i, c in enumerate(commits, 1):
        if c.get("patch", {}).get("unidiff"):
            patch_file = d / f"patch-{i}.diff"
            patch_file.write_text(c["patch"]["unidiff"], encoding="utf-8")
            try:
                os.chmod(patch_file, 0o600)
            except Exception:
                pass
            patches += 1
        meta = c.get("repoMetadata", {})
        if meta.get("environmentSetupScript") or meta.get("testCommand"):
            setup[task.get("sourceId") or meta.get("name") or tid] = meta
    plan = task.get("latestPlan", {}).get("steps", [])
    kinds = {}
    for a in acts:
        for actor, v in a.items():
            if isinstance(v, dict):
                for k in v:
                    kinds[f"{actor}.{k}"] = kinds.get(f"{actor}.{k}", 0) + 1
    lines = [f"# {task.get('title') or s.get('suggestedTitle') or tid}", "",
             f"- **ID:** {tid}", f"- **Repo:** {task.get('sourceId', '')}",
             f"- **Status:** {task.get('taskStatus', '')}", f"- **Created:** {task.get('createdAt', '')}",
             f"- **Completed:** {task.get('completedAt', '')}", "", "## Prompt", "", task.get("description", ""), ""]
    if plan:
        lines += ["## Latest plan", ""] + [f"{p.get('index', 0) + 1}. {p.get('title', '')}" for p in plan] + [""]
    if commits:
        lines += ["## Code outputs", ""] + [
            f"- `patch-{i}.diff`: {c.get('title') or (c.get('commitMessage') or '').split(chr(10))[0]} (branch `{c.get('gitBranchName', '')}`)"
            for i, c in enumerate(commits, 1)] + [""]
    if pub := task.get("latestPublish", {}).get("commitInfo"):
        lines += ["## Published", "", f"- Commit `{pub.get('commitId', '')}` on `{pub.get('branchName', '')}`", ""]
    lines += ["## Activity", "", f"{len(acts)} steps (full log in `activities.json`):", ""] + [f"- {k}: {n}" for k, n in sorted(kinds.items())]
    summary_file = d / "summary.md"
    summary_file.write_text("\n".join(lines) + "\n", encoding="utf-8")
    try:
        os.chmod(summary_file, 0o600)
    except Exception:
        pass

for sid, meta in setup.items():
    d = OUT / "repos" / safe(sid)
    d.mkdir(mode=0o700, parents=True, exist_ok=True)
    if meta.get("environmentSetupScript"):
        f = d / "setup.sh"
        f.write_text(meta["environmentSetupScript"] + "\n", encoding="utf-8")
        try:
            os.chmod(f, 0o600)
        except Exception:
            pass
    if meta.get("testCommand"):
        f = d / "test-command.txt"
        f.write_text(meta["testCommand"] + "\n", encoding="utf-8")
        try:
            os.chmod(f, 0o600)
        except Exception:
            pass

summary_report = {
    "repos": len(sources),
    "repos_with_memories": mem_repos,
    "sessions": len(sessions),
    "patches": patches,
    "repos_with_setup_or_test": len(setup),
    "error_count": len(errors),
    "errors": errors[:10]
}
print(json.dumps(summary_report, indent=2))

if errors:
    print(f"Export encountered {len(errors)} error(s). Partial output saved to {OUT.resolve()}", file=sys.stderr)
    sys.exit(1)

print(f"Exported all Jules data successfully to {OUT.resolve()}")
```
