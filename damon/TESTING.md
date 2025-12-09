# DAMON Fleet Testing Guide

## Quick Verification

### Test 1: Single DAMON Execution
```bash
python damon/damon-agent.py damon/configs/strategy.yml --project-root .
```

**Expected Output:**
- Should show STRATEGY DAMON header
- Should list 3 risks (Vision Drift, No Client Offer, Over-Scope)
- Should show 🟢🟡🔴 signals for each risk
- Should show overall signal
- Should display signal interpretation

### Test 2: Fleet Mode Execution
```bash
python damon/damon-agent.py --all damon/configs --project-root .
```

**Expected Output:**
- Should run all 7 DAMONs sequentially
- Should show individual summaries for each DAMON
- Should show fleet summary with signal counts
- Should complete without errors

### Test 3: JSON Output Generation
```bash
python damon/damon-agent.py --all damon/configs --project-root . --output /tmp/damon-test.json
cat /tmp/damon-test.json | python -m json.tool | head -50
```

**Expected Output:**
- Should create `/tmp/damon-test.json`
- JSON should be valid and parseable
- Should contain array of 7 DAMON results
- Each result should have: damon, domain, timestamp, overall_signal, risk_assessments

## Detailed Test Cases

### Test Case 1: File Exists Check
**Setup:**
```bash
# Remove file if exists
rm -f VISION.md
```

**Execute:**
```bash
python damon/damon-agent.py damon/configs/strategy.yml --project-root .
```

**Verify:**
- Should show ❌ FAIL for "Missing VISION.md"

**Cleanup:**
```bash
# Create the file
touch VISION.md
```

**Re-execute:**
```bash
python damon/damon-agent.py damon/configs/strategy.yml --project-root .
```

**Verify:**
- Should show ✅ PASS for VISION.md existence

---

### Test Case 2: Keyword Check
**Setup:**
```bash
cat > VISION.md << EOF
This is a test vision document.
EOF
```

**Execute:**
```bash
python damon/damon-agent.py damon/configs/strategy.yml --project-root .
```

**Verify:**
- Should show ❌ FAIL for "Strategic documents missing key alignment terms"

**Fix:**
```bash
cat > VISION.md << EOF
This is our strategic vision document.

Mission: Build secure multi-language implementations
Goal: Master GCP certifications
Objective: Create novel security benchmarking methodology
EOF
```

**Re-execute:**
```bash
python damon/damon-agent.py damon/configs/strategy.yml --project-root .
```

**Verify:**
- Should show ✅ PASS for keyword check

---

### Test Case 3: Directory Exists Check
**Setup:**
```bash
# Ensure directory doesn't exist
rm -rf security/red-team
```

**Execute:**
```bash
python damon/damon-agent.py damon/configs/security.yml --project-root .
```

**Verify:**
- Should show ❌ FAIL for "Missing red-team testing directory"

**Fix:**
```bash
mkdir -p security/red-team
```

**Re-execute:**
```bash
python damon/damon-agent.py damon/configs/security.yml --project-root .
```

**Verify:**
- Should show ✅ PASS for red-team directory

---

### Test Case 4: Commit Frequency Check
**Execute:**
```bash
python damon/damon-agent.py damon/configs/execution.yml --project-root .
```

**Verify:**
- Should show commit count for last 24 hours
- Should pass if commits < 50

**Simulate burnout:**
```bash
# This is informational only - you can't easily simulate without making 50+ commits
# The check should handle this gracefully
```

---

### Test Case 5: File Count Check
**Execute:**
```bash
python damon/damon-agent.py damon/configs/strategy.yml --project-root .
```

**Verify:**
- Should count markdown files at root level
- Should pass if count ≤ 20
- Current count should be displayed

---

### Test Case 6: Signal Logic
**Test RED Signal:**
- All checks fail → Should show 🔴 RED

**Test YELLOW Signal:**
- Some checks pass, some fail → Should show 🟡 YELLOW

**Test GREEN Signal:**
- All checks pass → Should show 🟢 GREEN

---

### Test Case 7: Multiple File Patterns
**Setup:**
```bash
mkdir -p implementations/python
mkdir -p implementations/rust
mkdir -p implementations/cpp
mkdir -p implementations/flamelang
```

**Execute:**
```bash
python damon/damon-agent.py damon/configs/security.yml --project-root .
```

**Verify:**
- Should show ✅ PASS for each implementation directory

---

### Test Case 8: Docker Build
**Execute:**
```bash
cd damon
docker-compose build damon-strategy
```

**Verify:**
- Build should complete without errors
- Image should be created: `docker images | grep damon`

---

### Test Case 9: Docker Run
**Execute:**
```bash
cd damon
docker-compose up damon-strategy
```

**Verify:**
- Container should start
- Should show STRATEGY DAMON output
- Should exit cleanly

---

### Test Case 10: Fleet Dashboard
**Execute:**
```bash
cd damon
mkdir -p results
docker-compose up damon-fleet
```

**Verify:**
- Should run all 7 DAMONs
- Should create `results/fleet-status.json`
- JSON should contain all 7 DAMON results

## Automated Test Script

```bash
#!/bin/bash
# automated-test.sh

set -e

echo "🧪 Running DAMON Fleet Tests"
echo "============================="

# Test 1: Single DAMON
echo ""
echo "Test 1: Single DAMON execution"
python damon/damon-agent.py damon/configs/strategy.yml --project-root . > /dev/null
echo "✅ PASS: Single DAMON execution"

# Test 2: Fleet Mode
echo ""
echo "Test 2: Fleet mode execution"
python damon/damon-agent.py --all damon/configs --project-root . > /dev/null
echo "✅ PASS: Fleet mode execution"

# Test 3: JSON Output
echo ""
echo "Test 3: JSON output generation"
python damon/damon-agent.py --all damon/configs --project-root . --output /tmp/test-results.json > /dev/null
if [ -f /tmp/test-results.json ]; then
    echo "✅ PASS: JSON file created"
    python -m json.tool /tmp/test-results.json > /dev/null
    echo "✅ PASS: JSON is valid"
else
    echo "❌ FAIL: JSON file not created"
    exit 1
fi

# Test 4: All DAMONs individually
echo ""
echo "Test 4: Individual DAMON execution"
for config in damon/configs/*.yml; do
    damon_name=$(basename $config .yml)
    python damon/damon-agent.py $config --project-root . > /dev/null
    echo "✅ PASS: $damon_name DAMON"
done

# Test 5: Check executability
echo ""
echo "Test 5: Script executability"
if [ -x damon/damon-agent.py ]; then
    echo "✅ PASS: damon-agent.py is executable"
else
    echo "❌ FAIL: damon-agent.py is not executable"
    exit 1
fi

echo ""
echo "============================="
echo "🎉 All tests passed!"
echo "============================="
```

Save as `damon/test.sh` and run:
```bash
chmod +x damon/test.sh
./damon/test.sh
```

## Performance Benchmarks

Typical execution times on standard hardware:

- Single DAMON: 0.1-0.5 seconds
- Fleet mode (7 DAMONs): 0.5-2 seconds
- JSON output: +0.1 seconds overhead
- Docker build: 30-60 seconds (first time)
- Docker run: 1-3 seconds per DAMON

## Troubleshooting Tests

### "No module named 'yaml'"
```bash
pip install pyyaml
```

### "Permission denied" on scripts
```bash
chmod +x damon/damon-agent.py
chmod +x damon/examples.sh
chmod +x damon/test.sh
```

### Docker build fails
```bash
# Check Docker is running
docker --version
docker info

# Check Dockerfile syntax
cd damon
docker build -f Dockerfile ..
```

### Git checks fail
```bash
# Ensure you're in a git repository
git status

# If not, initialize:
git init
```

## Expected Initial State

On first run without any project setup:

```
🔴 STRATEGY: RED  - Missing all strategic documents
🔴 EXECUTION: RED - Missing workload/cert tracking
🔴 SECURITY: RED  - Missing security methodology
🔴 CLOUD: RED     - Missing GCP configuration
🔴 DATA: RED      - Missing metrics/logging
🔴 STORY: RED     - Missing portfolio
🔴 ETHICS: RED    - Missing compliance docs
```

This is **expected and correct**! The DAMONs are telling you what needs to be built.

## Progress Tracking

As you build out the project, watch the signals improve:

1. **Phase 1**: All 🔴 RED (starting point)
2. **Phase 2**: Some 🟡 YELLOW (documentation started)
3. **Phase 3**: Some 🟢 GREEN (core infrastructure complete)
4. **Phase 4**: Mostly 🟢 GREEN (mature project)

## CI/CD Testing

To test the GitHub Actions workflow locally:

```bash
# Install act (GitHub Actions local runner)
# https://github.com/nektos/act

act push -W .github/workflows/damon-fleet.yml
```

Or just push to GitHub and check the Actions tab.

## Integration Tests

Test with real project evolution:

1. Start: All RED
2. Add VISION.md: STRATEGY improves
3. Add security/: SECURITY improves
4. Add gcp/: CLOUD improves
5. Continue building: Watch signals turn GREEN

This is the DAMON Fleet in action! 🔥
