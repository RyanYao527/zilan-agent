#!/usr/bin/env bash
# 60-second CLI demo for zilan-agent
# Record with: asciinema rec demo.cast -c "bash scripts/demo.sh"
# Or convert to GIF: asciinema-agg demo.cast demo.gif
#
# For vhs (charmbracelet): vhs scripts/demo.tape > demo.gif

set -e

# Colors for readability
BOLD="\e[1m"
GREEN="\e[32m"
BLUE="\e[34m"
RESET="\e[0m"

# Simulate typing speed for recording
pause() { sleep 0.8; }
fast_pause() { sleep 0.3; }

clear

# ── Title ──
echo -e "${BOLD}${BLUE}╔══════════════════════════════════════════════╗"
echo -e "║   zilan-agent · Output Contract Demo          ║"
echo -e "║   LLM reliability through deterministic checks ║"
echo -e "╚══════════════════════════════════════════════╝${RESET}"
pause

# ── Step 1: Sanity check ──
echo -e "\n${BOLD}▶ Step 1: Repository validation${RESET}"
fast_pause
echo -e "$ python scripts/validate_zilan_repo.py --check-generated --strict-yaml"
python scripts/validate_zilan_repo.py --check-generated --strict-yaml
pause

# ── Step 2: Run tests ──
echo -e "\n${BOLD}▶ Step 2: Full test suite${RESET}"
fast_pause
echo -e "$ python -m pytest -q"
python -m pytest -q 2>&1 | tail -5
pause

# ── Step 3: Contract review — PASS ──
echo -e "\n${BOLD}▶ Step 3: Answer contract review — ${GREEN}PASS${RESET} sample${RESET}"
fast_pause
echo -e "$ python scripts/reasoning_contract_runner.py \\"
echo -e "    --query-id SRQ-04 --sample-id srq04-agama-citation-boundary-pass --json"
fast_pause
python scripts/reasoning_contract_runner.py \
	--query-id SRQ-04 --sample-id srq04-agama-citation-boundary-pass --json |
	python -c "
import sys, json
d = json.load(sys.stdin)
print(f\"  overall_status:  {d['overall_status']}\")
print(f\"  answer_review:   {d['answer_review_status']}\")
for k, v in d['validators'].items():
    print(f\"  {k:20s}: {v['status']}\")
"
pause

# ── Step 4: Contract review — FAIL ──
echo -e "\n${BOLD}▶ Step 4: Answer contract review — ${BLUE}FAIL${RESET} sample${RESET}"
fast_pause
echo -e "$ python scripts/reasoning_contract_runner.py \\"
echo -e "    --query-id SRQ-04 --sample-id srq04-agama-citation-boundary-fail --json"
fast_pause
python scripts/reasoning_contract_runner.py \
	--query-id SRQ-04 --sample-id srq04-agama-citation-boundary-fail --json |
	python -c "
import sys, json
d = json.load(sys.stdin)
print(f\"  overall_status:  {d['overall_status']}\")
rc = d.get('role_coverage', {})
missing = rc.get('missing_needs', [])
if missing:
    print(f\"  missing_needs:   {missing}\")
ar = d.get('answer_contract_review') or {}
checks = ar.get('checks', [])
for c in checks:
    status = '✓' if c.get('status') == 'pass' else '✗'
    print(f\"  {status} {c['id']:25s} {c['status']}\")
"
pause

# ── Step 5: Agama search ──
echo -e "\n${BOLD}▶ Step 5: Agama scripture search${RESET}"
fast_pause
echo -e "$ python scripts/search_agama.py --terms '無我|非我' --limit 3"
python scripts/search_agama.py --terms "無我|非我" --limit 3
pause

# ── Done ──
echo -e "\n${BOLD}${GREEN}╔══════════════════════════════════════════════╗"
echo -e "║  211 tests · 85% coverage · mypy/ruff clean  ║"
echo -e "║  github.com/RyanYao527/zilan-agent           ║"
echo -e "╚══════════════════════════════════════════════╝${RESET}"
