# DAMON Fleet Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                      DAMON FLEET SYSTEM                          │
│                   (100 Failure Mode Monitors)                    │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
        ┌───────────────────────────────────────────┐
        │         7 Domain-Aware Monitoring         │
        │              Nodes (DAMONs)               │
        └───────────────────────────────────────────┘
                                │
                ┌───────────────┼───────────────┐
                │               │               │
        ┌───────▼──────┐ ┌─────▼──────┐ ┌─────▼──────┐
        │   STRATEGY   │ │ EXECUTION  │ │  SECURITY  │
        │              │ │            │ │            │
        │ • Vision     │ │ • Burnout  │ │ • Method   │
        │ • Client     │ │ • Context  │ │ • Harness  │
        │ • Scope      │ │ • Certs    │ │ • Multi-   │
        │              │ │            │ │   Lang     │
        └──────────────┘ └────────────┘ └────────────┘
                │
        ┌───────▼──────┐ ┌─────▼──────┐ ┌─────▼──────┐
        │    CLOUD     │ │    DATA    │ │   STORY    │
        │              │ │            │ │            │
        │ • IAM        │ │ • Metrics  │ │ • Portfolio│
        │ • Costs      │ │ • Logs     │ │ • Buzzwords│
        │ • Config     │ │ • Bench    │ │ • LinkedIn │
        │              │ │            │ │            │
        └──────────────┘ └────────────┘ └────────────┘
                │
        ┌───────▼──────┐
        │   ETHICS     │
        │              │
        │ • ToS        │
        │ • Claims     │
        │ • Scope      │
        │              │
        └──────────────┘
```

## Data Flow

```
Project Files
     │
     ▼
┌─────────────────┐
│ YAML Configs    │ ◄── Define risks & checks
│ (configs/*.yml) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  damon-agent.py │ ◄── Executes checks
│                 │
│ Check Types:    │
│ • file_exists   │
│ • keyword_check │
│ • file_count    │
│ • file_age      │
│ • commit_freq   │
│ • branch_count  │
│ • etc.          │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Risk Assessment │
│                 │
│ Per Risk:       │
│ • Pass count    │
│ • Fail count    │
│ • Signal (🟢🟡🔴) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Overall Signal  │
│                 │
│ 🟢 GREEN        │
│ 🟡 YELLOW       │
│ 🔴 RED          │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Output          │
│ • Console       │
│ • JSON file     │
│ • CI/CD         │
│ • Docker logs   │
└─────────────────┘
```

## Check Type Details

### File System Checks
- `file_exists`: Verify required documentation exists
- `directory_exists`: Verify expected structure
- `file_count`: Ensure not too many/few files
- `directory_count`: Monitor work-in-progress

### Content Checks
- `keyword_check`: Search for required/forbidden terms
- `file_pattern_check`: Find problematic code patterns

### Git Checks
- `commit_frequency`: Detect burnout patterns
- `branch_count`: Monitor context switching

### Time-based Checks
- `file_age`: Ensure regular updates

## Signal Logic

```
For each Risk:
    Run all checks
    Count passes & fails
    
    If all pass:
        Signal = 🟢 GREEN
    Else if ≤50% fail:
        Signal = 🟡 YELLOW
    Else:
        Signal = 🔴 RED

For overall DAMON:
    If any CRITICAL risk is 🔴:
        Overall = 🔴 RED
    Else if >50% risks are 🟡/🔴:
        Overall = 🟡 YELLOW / 🔴 RED
    Else:
        Overall = 🟢 GREEN
```

## Docker Deployment

```
┌─────────────────────────────────────────────────┐
│         docker-compose.yml                      │
├─────────────────────────────────────────────────┤
│                                                 │
│  ┌──────────────┐  ┌──────────────┐            │
│  │ damon-       │  │ damon-       │            │
│  │ strategy     │  │ execution    │            │
│  └──────────────┘  └──────────────┘            │
│                                                 │
│  ┌──────────────┐  ┌──────────────┐            │
│  │ damon-       │  │ damon-       │            │
│  │ security     │  │ cloud        │            │
│  └──────────────┘  └──────────────┘            │
│                                                 │
│  ┌──────────────┐  ┌──────────────┐            │
│  │ damon-       │  │ damon-       │            │
│  │ data         │  │ story        │            │
│  └──────────────┘  └──────────────┘            │
│                                                 │
│  ┌──────────────┐  ┌──────────────┐            │
│  │ damon-       │  │ damon-       │            │
│  │ ethics       │  │ fleet        │◄─ Aggregator
│  └──────────────┘  └──────────────┘            │
│                                                 │
└─────────────────────────────────────────────────┘
         │
         ▼ Volume Mount
   Project Directory (Read-Only)
```

## Usage Patterns

### Development Workflow
```
1. Make code changes
2. Run: python damon/damon-agent.py --all damon/configs
3. Fix any 🔴 RED signals
4. Commit changes
```

### CI/CD Integration
```
GitHub Actions Workflow:
1. Checkout code
2. Install Python + dependencies
3. Run DAMON Fleet
4. Upload results as artifacts
5. Fail build if critical domains are 🔴 (optional)
```

### Continuous Monitoring
```
Docker Compose:
1. Build images: docker-compose build
2. Start fleet: docker-compose up -d
3. View logs: docker-compose logs -f
4. Check results: cat damon/results/fleet-status.json
```

## Customization Points

### Add New Check Type
Edit `damon-agent.py`:
```python
def _check_custom(self, check: Dict[str, Any]) -> CheckResult:
    # Your custom logic here
    return CheckResult(...)
```

### Add New Risk
Edit config YAML:
```yaml
risks:
  - id: DOMAIN-004
    name: New Risk
    severity: high
    checks:
      - type: file_exists
        path: REQUIRED_FILE.md
```

### Add New DAMON
1. Create `damon/configs/custom.yml`
2. Add service to `docker-compose.yml`
3. Run: `python damon/damon-agent.py damon/configs/custom.yml`

## Integration Examples

### Pre-commit Hook
```bash
#!/bin/bash
python damon/damon-agent.py damon/configs/security.yml || exit 1
```

### Slack Notification
```python
import requests
results = run_damon_fleet()
if results['overall_signal'] == 'red':
    requests.post(SLACK_WEBHOOK, json={'text': '🔴 DAMON Alert!'})
```

### Prometheus Metrics
```python
from prometheus_client import Gauge
damon_signal = Gauge('damon_signal', 'DAMON signal level', ['domain'])
for result in results:
    signal_value = {'green': 0, 'yellow': 1, 'red': 2}[result['signal']]
    damon_signal.labels(domain=result['domain']).set(signal_value)
```

## Why This Is Novel

1. **Multi-domain Coverage**: Most tools monitor one aspect (security OR quality). DAMONs monitor ALL failure modes.

2. **Declarative Configuration**: Risks and checks are YAML, not code. Easy to customize without programming.

3. **Traffic Light Simplicity**: Complex checks → Simple 🟢🟡🔴 signals anyone can understand.

4. **Containerized & Composable**: Each DAMON runs independently. Scale horizontally.

5. **Multi-Language Support**: Built-in checks for Python/Rust/C++/FlameLang security benchmarking.

6. **Actionable Feedback**: Not just "something's wrong" — tells you exactly what file is missing or what keyword to add.
