#!/bin/bash
# Automated test suite for DAMON Fleet

set -e

echo "🧪 Running DAMON Fleet Tests"
echo "============================="

# Test 1: Single DAMON
echo ""
echo "Test 1: Single DAMON execution"
python damon/damon-agent.py damon/configs/strategy.yml --project-root . > /dev/null 2>&1
echo "✅ PASS: Single DAMON execution"

# Test 2: Fleet Mode
echo ""
echo "Test 2: Fleet mode execution"
python damon/damon-agent.py --all damon/configs --project-root . > /dev/null 2>&1
echo "✅ PASS: Fleet mode execution"

# Test 3: JSON Output
echo ""
echo "Test 3: JSON output generation"
python damon/damon-agent.py --all damon/configs --project-root . --output /tmp/test-results.json > /dev/null 2>&1
if [ -f /tmp/test-results.json ]; then
    echo "✅ PASS: JSON file created"
    python -m json.tool /tmp/test-results.json > /dev/null 2>&1
    echo "✅ PASS: JSON is valid"
    
    # Check structure
    DAMON_COUNT=$(python -c "import json; print(len(json.load(open('/tmp/test-results.json'))))")
    if [ "$DAMON_COUNT" -eq 7 ]; then
        echo "✅ PASS: All 7 DAMONs in results"
    else
        echo "❌ FAIL: Expected 7 DAMONs, got $DAMON_COUNT"
        exit 1
    fi
else
    echo "❌ FAIL: JSON file not created"
    exit 1
fi

# Test 4: All DAMONs individually
echo ""
echo "Test 4: Individual DAMON execution"
for config in damon/configs/*.yml; do
    damon_name=$(basename "$config" .yml)
    python damon/damon-agent.py "$config" --project-root . > /dev/null 2>&1
    echo "✅ PASS: $damon_name DAMON"
done

# Test 5: Check executability
echo ""
echo "Test 5: Script executability"
if [ -x damon/damon-agent.py ]; then
    echo "✅ PASS: damon-agent.py is executable"
else
    echo "⚠️  WARN: damon-agent.py is not executable (non-critical)"
fi

# Test 6: Check all required files exist
echo ""
echo "Test 6: Required files exist"
required_files=(
    "damon/damon-agent.py"
    "damon/README.md"
    "damon/QUICKSTART.md"
    "damon/Dockerfile"
    "damon/docker-compose.yml"
    "damon/configs/strategy.yml"
    "damon/configs/execution.yml"
    "damon/configs/security.yml"
    "damon/configs/cloud.yml"
    "damon/configs/data.yml"
    "damon/configs/story.yml"
    "damon/configs/ethics.yml"
)

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ PASS: $file exists"
    else
        echo "❌ FAIL: $file missing"
        exit 1
    fi
done

# Test 7: Verify YAML syntax
echo ""
echo "Test 7: YAML syntax validation"
for config in damon/configs/*.yml; do
    if python -c "import yaml; yaml.safe_load(open('$config'))" 2>&1; then
        echo "✅ PASS: $(basename "$config") is valid YAML"
    else
        echo "❌ FAIL: $(basename "$config") has invalid YAML"
        exit 1
    fi
done

# Test 8: Verify Python syntax
echo ""
echo "Test 8: Python syntax validation"
if python -m py_compile damon/damon-agent.py 2>&1; then
    echo "✅ PASS: damon-agent.py has valid Python syntax"
else
    echo "❌ FAIL: damon-agent.py has syntax errors"
    exit 1
fi

# Test 9: Check help output
echo ""
echo "Test 9: Help output"
python damon/damon-agent.py --help > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ PASS: Help command works"
else
    echo "❌ FAIL: Help command failed"
    exit 1
fi

# Test 10: Verify each DAMON has all required fields
echo ""
echo "Test 10: DAMON config structure validation"
for config in damon/configs/*.yml; do
    damon_name=$(basename $config .yml)
    
    # Check required top-level fields
    python -c "
import yaml
with open('$config') as f:
    data = yaml.safe_load(f)
    required = ['name', 'description', 'domain', 'priority', 'risks', 'signals']
    missing = [f for f in required if f not in data]
    if missing:
        print(f'Missing fields: {missing}')
        exit(1)
" 2>&1
    
    if [ $? -eq 0 ]; then
        echo "✅ PASS: $damon_name config structure valid"
    else
        echo "❌ FAIL: $damon_name config missing required fields"
        exit 1
    fi
done

echo ""
echo "============================="
echo "🎉 All tests passed!"
echo ""
echo "Summary:"
echo "  ✅ 10 test categories"
echo "  ✅ 30+ individual checks"
echo "  ✅ DAMON Fleet is ready to use"
echo "============================="
echo ""
echo "Next steps:"
echo "  1. Run: python damon/damon-agent.py --all damon/configs --project-root ."
echo "  2. Review the output and fix any 🔴 RED signals"
echo "  3. Set up CI/CD with .github/workflows/damon-fleet.yml"
echo "  4. Deploy with Docker: cd damon && docker-compose up"
echo ""
