#!/bin/bash
# DAMON Fleet Usage Examples
# This script demonstrates various ways to use the DAMON Fleet

set -e

echo "🔥 DAMON Fleet - Usage Examples"
echo "================================"
echo ""

# Example 1: Run all DAMONs
echo "Example 1: Run all DAMONs"
echo "-------------------------"
echo "Command: python damon/damon-agent.py --all damon/configs --project-root ."
echo ""
read -p "Press Enter to run..."
python damon/damon-agent.py --all damon/configs --project-root .
echo ""

# Example 2: Run a single DAMON
echo "Example 2: Run STRATEGY DAMON only"
echo "-----------------------------------"
echo "Command: python damon/damon-agent.py damon/configs/strategy.yml --project-root ."
echo ""
read -p "Press Enter to run..."
python damon/damon-agent.py damon/configs/strategy.yml --project-root .
echo ""

# Example 3: Save results to JSON
echo "Example 3: Save results to JSON file"
echo "-------------------------------------"
echo "Command: python damon/damon-agent.py --all damon/configs --project-root . --output /tmp/damon-results.json"
echo ""
read -p "Press Enter to run..."
python damon/damon-agent.py --all damon/configs --project-root . --output /tmp/damon-results.json
echo "Results saved to /tmp/damon-results.json"
echo ""
echo "Preview:"
cat /tmp/damon-results.json | python -m json.tool | head -40
echo ""

# Example 4: Run critical DAMONs only
echo "Example 4: Run critical DAMONs only (SECURITY + ETHICS)"
echo "--------------------------------------------------------"
echo ""
read -p "Press Enter to run..."
echo "Running SECURITY DAMON..."
python damon/damon-agent.py damon/configs/security.yml --project-root .
echo ""
echo "Running ETHICS DAMON..."
python damon/damon-agent.py damon/configs/ethics.yml --project-root .
echo ""

# Example 5: Docker usage
echo "Example 5: Docker deployment (not executed, just shown)"
echo "--------------------------------------------------------"
echo ""
echo "To build and run with Docker:"
echo "  cd damon"
echo "  docker-compose build"
echo "  docker-compose up"
echo ""
echo "To run specific DAMONs:"
echo "  docker-compose up damon-security damon-ethics"
echo ""
echo "To run in background:"
echo "  docker-compose up -d"
echo ""

echo "✅ Examples complete!"
echo ""
echo "Next steps:"
echo "1. Review the DAMON output above"
echo "2. Fix any 🔴 RED signals by creating missing files/directories"
echo "3. Re-run DAMONs to verify fixes"
echo "4. Set up automated checks in CI/CD (see .github/workflows/damon-fleet.yml)"
echo ""
