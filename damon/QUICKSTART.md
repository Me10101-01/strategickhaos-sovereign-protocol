# DAMON Fleet Quick Start Guide

## Installation

### Prerequisites
- Python 3.8+
- Docker and Docker Compose (optional, for containerized deployment)
- Git (for commit-based checks)

### Python Dependencies

```bash
pip install pyyaml
```

## Running Your First DAMON Check

### 1. Test a Single DAMON

```bash
# From the project root
python damon/damon-agent.py damon/configs/strategy.yml --project-root .
```

You'll see output like:

```
🔍 Starting STRATEGY DAMON checks...
   Domain: strategic_alignment
   Priority: critical

📋 Checking risk: Vision Drift (STRAT-001)
   ❌ FAIL: Missing VISION.md - no documented strategic vision
   ❌ FAIL: Strategic documents missing key alignment terms
   
============================================================
DAMON: STRATEGY
Domain: strategic_alignment
Overall Signal: 🔴 RED
============================================================

🔴 Vision Drift (STRAT-001)
   Severity: high
   Checks: 0 passed, 2 failed

🔴 Signal Interpretation:
   • No strategic vision documented
   
============================================================
```

### 2. Run All DAMONs

```bash
python damon/damon-agent.py --all damon/configs --project-root .
```

This runs all 7 DAMONs and shows a fleet summary:

```
============================================================
DAMON FLEET SUMMARY
============================================================
🔴 STRATEGY: RED
🔴 EXECUTION: RED
🔴 SECURITY: RED
🔴 CLOUD: RED
🔴 DATA: RED
🔴 STORY: RED
🔴 ETHICS: RED

Overall: 0 green, 0 yellow, 7 red
============================================================
```

### 3. Save Results to JSON

```bash
python damon/damon-agent.py --all damon/configs --project-root . --output damon-results.json
```

## Understanding the Output

### Traffic Light Signals

- **🟢 GREEN**: Everything is good, keep going
- **🟡 YELLOW**: Some issues need attention soon
- **🔴 RED**: Critical problems, stop and fix now

### Risk IDs

Each check has a unique ID:
- `STRAT-001`: Strategy domain, risk #1
- `SEC-002`: Security domain, risk #2
- etc.

### Check Results

Each check shows:
- **Pass/Fail status**
- **Descriptive message**
- **Additional details** (when available)

## Fixing RED Signals

The DAMON agent tells you exactly what's missing. For example:

```
❌ FAIL: Missing VISION.md - no documented strategic vision
```

To fix:
1. Create the missing file: `touch VISION.md`
2. Add required content
3. Re-run the DAMON to verify: `python damon/damon-agent.py damon/configs/strategy.yml --project-root .`

## Docker Deployment

### Build the Images

```bash
cd damon
docker-compose build
```

### Run the Fleet

```bash
docker-compose up
```

### Run in Background

```bash
docker-compose up -d
```

### View Results

```bash
# View logs
docker-compose logs -f damon-fleet

# Results are saved to damon/results/fleet-status.json
cat damon/results/fleet-status.json | python -m json.tool
```

## Common Workflows

### Daily Health Check

```bash
# Morning routine: check all domains
python damon/damon-agent.py --all damon/configs --project-root .
```

### Pre-commit Check

```bash
# Before committing code, check security
python damon/damon-agent.py damon/configs/security.yml --project-root .
```

### Weekly Certification Review

```bash
# Check execution domain for certification progress
python damon/damon-agent.py damon/configs/execution.yml --project-root .
```

### Portfolio Preparation

```bash
# Check story domain before updating LinkedIn
python damon/damon-agent.py damon/configs/story.yml --project-root .
```

## Integrating with Your Workflow

### GitHub Actions

Create `.github/workflows/damon.yml`:

```yaml
name: DAMON Fleet Check

on: [push, pull_request]

jobs:
  damon-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install pyyaml
      - run: python damon/damon-agent.py --all damon/configs --project-root . --output damon-results.json
      - uses: actions/upload-artifact@v3
        with:
          name: damon-results
          path: damon-results.json
```

### Pre-commit Hook

Create `.git/hooks/pre-commit`:

```bash
#!/bin/bash
echo "Running DAMON security checks..."
python damon/damon-agent.py damon/configs/security.yml --project-root . || exit 1
```

Make it executable:

```bash
chmod +x .git/hooks/pre-commit
```

## Troubleshooting

### "ModuleNotFoundError: No module named 'yaml'"

Install PyYAML:
```bash
pip install pyyaml
```

### "Could not check git commits"

Git checks require a git repository. If you see this message but aren't using git, the check will pass automatically.

### Permission Denied on Docker

Run with sudo or add your user to the docker group:
```bash
sudo usermod -aG docker $USER
```

### Config File Not Found

Make sure you're running from the project root or provide the full path:
```bash
python /full/path/to/damon/damon-agent.py /full/path/to/damon/configs/strategy.yml --project-root /full/path/to/project
```

## Next Steps

1. **Create the missing files** identified by RED signals
2. **Customize the configs** to match your project's needs
3. **Set up automated checks** in CI/CD
4. **Monitor regularly** to catch problems early

## Getting Help

- Check the main [DAMON README](README.md) for detailed documentation
- Review the YAML configs in `damon/configs/` to understand what's being checked
- Look at the source code in `damon-agent.py` to understand how checks work

---

**Remember**: The DAMONs are watching your back. When they show 🔴, they're preventing future pain. Fix the issues early! 🔥
