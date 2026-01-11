# Engineering Context Playbook (agent-only)

Purpose: produce a fast, reliable engineering context map for any repo.
This is not user-facing documentation. It is a navigation map for an agent.

Output:
- Create `dev_agent_context/context-map.md` using `dev_agent_context/context-map.template.md`.
- Keep it short, factual, and evidence-backed. Do not over-explain.
- Create `dev_agent_context/context-map.md` in Russian lang.

Process (minimal, repeatable):
1) Orientation
   - Read `README*`, `docs/`, and any onboarding/walkthrough files.
   - List root files/dirs; identify language(s) and runtime(s).
   - Note hardware, platforms, or environment constraints.
2) Entry points and run paths
   - Find how to start in prod and local dev (scripts, Docker, services).
   - Identify primary entry modules, CLI commands, or web endpoints.
3) Core flow and state
   - Trace the main execution path from input to output.
   - Identify state machines, jobs, or long-running loops.
4) Structure and ownership
   - Map top-level directories to responsibilities.
   - List key modules and their roles (only the top layer).
5) Data and config
   - Identify config files, env vars, and secrets handling.
   - Map data stores, files, and schemas.
6) Dependencies and integrations
   - External services, APIs, devices, binaries, or models.
7) Ops and quality
   - Logging, metrics, error handling.
   - Tests, CI, linting, build steps.
8) Risks and unknowns
   - Capture tech debt, missing docs, or ambiguous behavior.
   - Add open questions.

Evidence discipline:
- Every non-obvious claim must include `@source: path[:line]`.
- If a claim is inferred, mark it as `@inferred` and keep it brief.
- Unknowns are explicit and listed in "Open questions."

Stop conditions:
- You can answer: what it is, how it runs, main flow, config, data, risks.
- Further digging yields diminishing returns; leave a question instead.

Update rules:
- When the repo changes, refresh only the impacted sections.
- Keep a short "Last updated" line in the map.
- Do not expand the map beyond what is needed for fast orientation.

Quick scan commands (use rg when possible):
- `rg --files`
- `rg -n "main|entry|app|server|cli" src`
- `rg -n "TODO|FIXME|HACK" -g'*.py' -g'*.ts' -g'*.go'`
- `rg -n "docker|compose|k8s|systemd|service" -g'*.*'`
- `rg -n "config|yaml|toml|json|env" -g'*.*'`

