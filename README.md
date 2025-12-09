# strategickhaos-sovereign-protocol
The official sovereign mesh interface for Strategickhaos: AI reflex protocols, LightGate glyph verification, legal partitioning, and decentralized immunity systems.

## 🔥 DAMON Fleet - Automated Failure Mode Detection

This repository includes a **novel infrastructure-as-code watchdog system** that monitors your project for 100 different failure modes across 7 critical domains.

### Quick Start

```bash
# Install dependencies
pip install pyyaml

# Run all DAMONs
python damon/damon-agent.py --all damon/configs --project-root .

# Run a specific DAMON
python damon/damon-agent.py damon/configs/security.yml --project-root .
```

### The 7 DAMONs

| DAMON    | Watches For                              |
|----------|------------------------------------------|
| STRATEGY | Vision drift, no client offer, over-scope|
| EXECUTION| Burnout, context switching, stalled certs|
| SECURITY | Weak methodology, no repeatable harness  |
| CLOUD    | IAM mistakes, cost runaway, misconfig    |
| DATA     | Bad metrics, no logs, benchmark fraud    |
| STORY    | Portfolio chaos, buzzword overload       |
| ETHICS   | ToS violations, overclaims, scope creep  |

### Documentation

- [Full DAMON Documentation](damon/README.md)
- [Quick Start Guide](damon/QUICKSTART.md)
- [Configuration Files](damon/configs/)

### Docker Deployment

```bash
cd damon
docker-compose up --build
```

This starts 7 containerized watchdogs that continuously monitor your project health.
