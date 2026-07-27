# zilan-agent demo tape for vhs (https://github.com/charmbracelet/vhs)
#
# Usage:
#   cd zilan-agent/
#   vhs scripts/demo.tape
#   # produces demo.gif
#
# Requirements: vhs, Python 3.10+, PyYAML, pytest

Output demo.gif

Set FontSize 18
Set Width 900
Set Height 600
Set Padding 10
Set Theme "Catppuccin Mocha"
Set Framerate 30
Set PlaybackSpeed 1.2

Hide

Type "cd zilan-agent"
Enter
Sleep 300ms

Show

# ── Title ──
Type "# zilan-agent · Output Contract Demo"
Enter
Sleep 500ms
Type "# github.com/RyanYao527/zilan-agent"
Enter
Sleep 800ms

# ── Step 1: Validate ──
Type "# Step 1: Repository validation"
Enter
Sleep 500ms
Type "python scripts/validate_zilan_repo.py --check-generated --strict-yaml"
Enter
Sleep 2s

# ── Step 2: Tests ──
Type "# Step 2: 172 tests, all passing"
Enter
Sleep 300ms
Type "python -m pytest -q"
Enter
Sleep 3s

# ── Step 3: Contract PASS ──
Type "# Step 3: Contract review — PASS sample"
Enter
Sleep 500ms
Type "python scripts/reasoning_contract_runner.py --query-id SRQ-04 --sample-id srq04-agama-citation-boundary-pass --json | python -c \"import sys,json; d=json.load(sys.stdin); print(f'overall_status: {d[chr(39)+chr(39)]}') # ...\""
Enter
Sleep 2s

# ── Step 4: Contract FAIL ──
Type "# Step 4: Same query, FAIL sample — catches the drift"
Enter
Sleep 500ms
Type "python scripts/reasoning_contract_runner.py --query-id SRQ-04 --sample-id srq04-agama-citation-boundary-fail --json | python -c \"import sys,json; d=json.load(sys.stdin); print(f'overall_status: {d[chr(39)+chr(39)]}') # ...\""
Enter
Sleep 2s

# ── Step 5: Search ──
Type "# Step 5: Agama search with stable citations"
Enter
Sleep 300ms
Type "python scripts/search_agama.py --terms '無我|非我' --limit 3"
Enter
Sleep 2s

# ── End ──
Type "# 172 tests · 86% coverage · mypy/ruff clean · MIT"
Enter
Sleep 1s

Hide
