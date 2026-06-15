# 2026-06-15 Mock Claude Install Smoke Evidence

| Field | Value |
|---|---|
| Date | 2026-06-15 |
| Scenario | Mock Claude Code skill/agent install smoke |
| Route / provider | Claude Code install layout; no model provider runtime |
| Repository commit | `a9121d21ae376533a837a450fb487012bcaa3401` |
| Source location | Repository checkout at `C:\Users\rori9\zilan-agent-review` |
| Redaction note | No secrets were present. Temporary directory suffix is not semantically relevant. |
| Runtime log entry | `docs/runtime-validation-log.md#2026-06-15-mock-claude-install-smoke` |

## Command

```powershell
python scripts\mock_install_smoke.py
```

## Output Excerpts

```text
mode: mock-claude-install
mock_home: %TEMP%\zilan-mock-install-...\home
skill_dir: %TEMP%\zilan-mock-install-...\home\.claude\skills\zilan-agent
agent_file: %TEMP%\zilan-mock-install-...\home\.claude\agents\zilan.md
checks:
  - skill:SKILL.md: pass
  - skill:agents/zilan-claude-code.md: pass
  - skill:scripts/search_agama.py: pass
  - skill:scripts/build_agama_context.py: pass
  - skill:context/因明推理引擎.md: pass
  - skill:context/摄类学工具箱.md: pass
  - skill:context/agama/agama-index.md: pass
  - skill:context/agama/T0099-za-agama.md: pass
  - agent:file: pass
  - agent:matches-source: pass
  - agent-fragment:name: zilan: pass
  - agent-fragment:tools:: pass
  - agent-fragment:search_agama.py: pass
  - agent-fragment:context/: pass
search_exit_code: 0
```

Installed skill Agama search excerpt:

```text
Found 1 matches for /緣起/
《中阿含經》(T01n0026) 卷 7, context/agama/T0026-zhong-agama.md:2227
  | 「諸賢！世尊亦如是說：『若見緣起便見法，若見法便見緣起。』...
```

## Result

| Check | Result | Notes |
|---|---|---|
| Mock skill copy | `pass` | Copied repository into temporary `.claude/skills/zilan-agent`. |
| Mock agent install | `pass` | Installed `agents/zilan-claude-code.md` as temporary `.claude/agents/zilan.md`. |
| Required skill files | `pass` | Checked skill definition, agent definition, scripts, and key context files. |
| Agent definition fragments | `pass` | Checked name, tools, search script, and context references. |
| Installed Agama search | `pass` | Ran copied `scripts/search_agama.py` from the temporary skill directory. |

## Limitations

- This validates filesystem layout and local helper availability only.
- It does not start Claude Code or verify model answer quality.
- It intentionally avoids touching the real user `~/.claude` directory.
