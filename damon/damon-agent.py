#!/usr/bin/env python3
"""
DAMON Agent - Domain-Aware Monitoring Node

Reads YAML risk configurations and runs automated checks
to detect project failure modes across 7 domains:
- STRATEGY: Vision drift, no client offer, over-scope
- EXECUTION: Burnout, context switching, stalled certs
- SECURITY: Weak methodology, no repeatable harness
- CLOUD: IAM mistakes, cost runaway, misconfig
- DATA: Bad metrics, no logs, benchmark fraud
- STORY: Portfolio chaos, buzzword overload
- ETHICS: ToS violations, overclaims, scope creep
"""

import os
import sys
import yaml
import glob
import json
import logging
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum


class Severity(Enum):
    """Risk severity levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class Signal(Enum):
    """Traffic light signals for domain health"""
    GREEN = "green"
    YELLOW = "yellow"
    RED = "red"


@dataclass
class CheckResult:
    """Result of a single check execution"""
    check_type: str
    passed: bool
    message: str
    details: Optional[Dict[str, Any]] = None


@dataclass
class RiskAssessment:
    """Assessment result for a single risk"""
    risk_id: str
    risk_name: str
    severity: Severity
    checks_passed: int
    checks_failed: int
    check_results: List[CheckResult]
    signal: Signal


class DAMONAgent:
    """Main DAMON agent that reads configs and executes checks"""
    
    def __init__(self, config_path: str, project_root: str):
        """
        Initialize DAMON agent
        
        Args:
            config_path: Path to YAML configuration file
            project_root: Root directory of the project to monitor
        """
        self.config_path = Path(config_path)
        self.project_root = Path(project_root)
        self.config = self._load_config()
        self.logger = self._setup_logging()
        
    def _setup_logging(self) -> logging.Logger:
        """Configure logging for the agent"""
        logger = logging.getLogger(f"DAMON.{self.config['name']}")
        logger.setLevel(logging.INFO)
        
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.INFO)
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger
        
    def _load_config(self) -> Dict[str, Any]:
        """Load YAML configuration file"""
        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def run_checks(self) -> Dict[str, Any]:
        """
        Execute all checks defined in the configuration
        
        Returns:
            Dictionary containing assessment results
        """
        self.logger.info(f"🔍 Starting {self.config['name']} DAMON checks...")
        self.logger.info(f"   Domain: {self.config['domain']}")
        self.logger.info(f"   Priority: {self.config['priority']}")
        
        risk_assessments = []
        
        for risk in self.config.get('risks', []):
            assessment = self._assess_risk(risk)
            risk_assessments.append(assessment)
            
        overall_signal = self._calculate_overall_signal(risk_assessments)
        
        results = {
            'damon': self.config['name'],
            'domain': self.config['domain'],
            'timestamp': datetime.now().isoformat(),
            'overall_signal': overall_signal.value,
            'risk_assessments': [self._serialize_assessment(a) for a in risk_assessments]
        }
        
        self._print_summary(results)
        
        return results
    
    def _assess_risk(self, risk: Dict[str, Any]) -> RiskAssessment:
        """
        Assess a single risk by running all its checks
        
        Args:
            risk: Risk configuration dictionary
            
        Returns:
            RiskAssessment object
        """
        self.logger.info(f"\n📋 Checking risk: {risk['name']} ({risk['id']})")
        
        check_results = []
        
        for check in risk.get('checks', []):
            result = self._execute_check(check)
            check_results.append(result)
            
            status = "✅ PASS" if result.passed else "❌ FAIL"
            self.logger.info(f"   {status}: {result.message}")
        
        passed = sum(1 for r in check_results if r.passed)
        failed = sum(1 for r in check_results if not r.passed)
        
        # Determine signal based on check results
        if failed == 0:
            signal = Signal.GREEN
        elif failed <= len(check_results) // 2:
            signal = Signal.YELLOW
        else:
            signal = Signal.RED
            
        return RiskAssessment(
            risk_id=risk['id'],
            risk_name=risk['name'],
            severity=Severity(risk['severity']),
            checks_passed=passed,
            checks_failed=failed,
            check_results=check_results,
            signal=signal
        )
    
    def _execute_check(self, check: Dict[str, Any]) -> CheckResult:
        """
        Execute a single check based on its type
        
        Args:
            check: Check configuration dictionary
            
        Returns:
            CheckResult object
        """
        check_type = check['type']
        
        if check_type == 'file_exists':
            return self._check_file_exists(check)
        elif check_type == 'directory_exists':
            return self._check_directory_exists(check)
        elif check_type == 'keyword_check':
            return self._check_keywords(check)
        elif check_type == 'file_count':
            return self._check_file_count(check)
        elif check_type == 'file_age':
            return self._check_file_age(check)
        elif check_type == 'file_pattern_check':
            return self._check_file_patterns(check)
        elif check_type == 'commit_frequency':
            return self._check_commit_frequency(check)
        elif check_type == 'branch_count':
            return self._check_branch_count(check)
        elif check_type == 'directory_count':
            return self._check_directory_count(check)
        else:
            return CheckResult(
                check_type=check_type,
                passed=False,
                message=f"Unknown check type: {check_type}"
            )
    
    def _check_file_exists(self, check: Dict[str, Any]) -> CheckResult:
        """Check if a file exists"""
        path = self.project_root / check['path']
        exists = path.exists() and path.is_file()
        
        return CheckResult(
            check_type='file_exists',
            passed=exists,
            message=check['message'] if not exists else f"File exists: {check['path']}",
            details={'path': str(path), 'exists': exists}
        )
    
    def _check_directory_exists(self, check: Dict[str, Any]) -> CheckResult:
        """Check if a directory exists"""
        path = self.project_root / check['path']
        exists = path.exists() and path.is_dir()
        
        return CheckResult(
            check_type='directory_exists',
            passed=exists,
            message=check['message'] if not exists else f"Directory exists: {check['path']}",
            details={'path': str(path), 'exists': exists}
        )
    
    def _check_keywords(self, check: Dict[str, Any]) -> CheckResult:
        """Check for required or forbidden keywords in files"""
        files = check.get('files', [])
        required = check.get('required_keywords', [])
        forbidden = check.get('forbidden_keywords', [])
        min_matches = check.get('min_matches', len(required))
        max_matches = check.get('max_matches', 0)
        
        all_content = ""
        found_files = []
        
        for file_pattern in files:
            if '*' in file_pattern or '?' in file_pattern:
                # Handle glob patterns
                matches = list(self.project_root.glob(file_pattern))
                found_files.extend(matches)
            else:
                # Single file
                file_path = self.project_root / file_pattern
                if file_path.exists():
                    found_files.append(file_path)
        
        for file_path in found_files:
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    all_content += f.read() + "\n"
            except Exception:
                pass
        
        # Check required keywords
        if required:
            matches = sum(1 for kw in required if kw.lower() in all_content.lower())
            passed = matches >= min_matches
            
            return CheckResult(
                check_type='keyword_check',
                passed=passed,
                message=check['message'] if not passed else f"Found {matches}/{len(required)} required keywords",
                details={'required': required, 'matches': matches, 'files_checked': len(found_files)}
            )
        
        # Check forbidden keywords
        if forbidden:
            matches = sum(1 for kw in forbidden if kw.lower() in all_content.lower())
            passed = matches <= max_matches
            
            return CheckResult(
                check_type='keyword_check',
                passed=passed,
                message=check['message'] if not passed else f"Found {matches} forbidden keywords (max: {max_matches})",
                details={'forbidden': forbidden, 'matches': matches, 'files_checked': len(found_files)}
            )
        
        return CheckResult(
            check_type='keyword_check',
            passed=True,
            message="No keywords to check"
        )
    
    def _check_file_count(self, check: Dict[str, Any]) -> CheckResult:
        """Check number of files matching a pattern"""
        pattern = check['pattern']
        max_count = check.get('max_count', float('inf'))
        min_count = check.get('min_count', 0)
        
        matches = list(self.project_root.glob(f"**/{pattern}"))
        count = len(matches)
        
        passed = min_count <= count <= max_count
        
        return CheckResult(
            check_type='file_count',
            passed=passed,
            message=check['message'] if not passed else f"Found {count} files matching '{pattern}'",
            details={'pattern': pattern, 'count': count, 'min': min_count, 'max': max_count}
        )
    
    def _check_file_age(self, check: Dict[str, Any]) -> CheckResult:
        """Check if a file was modified recently"""
        path = self.project_root / check['path']
        max_days = check.get('max_days', 30)
        
        if not path.exists():
            return CheckResult(
                check_type='file_age',
                passed=False,
                message=f"File does not exist: {check['path']}"
            )
        
        mtime = datetime.fromtimestamp(path.stat().st_mtime)
        age_days = (datetime.now() - mtime).days
        
        passed = age_days <= max_days
        
        return CheckResult(
            check_type='file_age',
            passed=passed,
            message=check['message'] if not passed else f"File age: {age_days} days (max: {max_days})",
            details={'path': str(path), 'age_days': age_days, 'max_days': max_days}
        )
    
    def _check_file_patterns(self, check: Dict[str, Any]) -> CheckResult:
        """Check for forbidden patterns in files"""
        pattern = check['pattern']
        forbidden = check.get('forbidden_patterns', [])
        
        matches = list(self.project_root.glob(pattern))
        violations = []
        
        for file_path in matches:
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    for forbidden_pattern in forbidden:
                        if forbidden_pattern in content:
                            violations.append({
                                'file': str(file_path.relative_to(self.project_root)),
                                'pattern': forbidden_pattern
                            })
            except Exception:
                pass
        
        passed = len(violations) == 0
        
        return CheckResult(
            check_type='file_pattern_check',
            passed=passed,
            message=check['message'] if not passed else f"No forbidden patterns found",
            details={'violations': violations, 'files_checked': len(matches)}
        )
    
    def _check_commit_frequency(self, check: Dict[str, Any]) -> CheckResult:
        """Check git commit frequency (requires git)"""
        max_per_day = check.get('max_per_day', 50)
        
        try:
            import subprocess
            result = subprocess.run(
                ['git', '-C', str(self.project_root), 'log', '--since=1.day.ago', '--oneline'],
                capture_output=True,
                text=True
            )
            
            commit_count = len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
            passed = commit_count <= max_per_day
            
            return CheckResult(
                check_type='commit_frequency',
                passed=passed,
                message=check['message'] if not passed else f"Commits today: {commit_count} (max: {max_per_day})",
                details={'commits_today': commit_count, 'max_per_day': max_per_day}
            )
        except Exception as e:
            return CheckResult(
                check_type='commit_frequency',
                passed=True,
                message=f"Could not check git commits: {str(e)}"
            )
    
    def _check_branch_count(self, check: Dict[str, Any]) -> CheckResult:
        """Check number of git branches"""
        max_branches = check.get('max_branches', 10)
        
        try:
            import subprocess
            result = subprocess.run(
                ['git', '-C', str(self.project_root), 'branch', '-a'],
                capture_output=True,
                text=True
            )
            
            branch_count = len([l for l in result.stdout.strip().split('\n') if l.strip()])
            passed = branch_count <= max_branches
            
            return CheckResult(
                check_type='branch_count',
                passed=passed,
                message=check['message'] if not passed else f"Branches: {branch_count} (max: {max_branches})",
                details={'branch_count': branch_count, 'max_branches': max_branches}
            )
        except Exception as e:
            return CheckResult(
                check_type='branch_count',
                passed=True,
                message=f"Could not check git branches: {str(e)}"
            )
    
    def _check_directory_count(self, check: Dict[str, Any]) -> CheckResult:
        """Check number of directories matching a pattern"""
        pattern = check['pattern']
        max_count = check.get('max_count', float('inf'))
        
        matches = [p for p in self.project_root.glob(pattern) if p.is_dir()]
        count = len(matches)
        
        passed = count <= max_count
        
        return CheckResult(
            check_type='directory_count',
            passed=passed,
            message=check['message'] if not passed else f"Found {count} directories (max: {max_count})",
            details={'pattern': pattern, 'count': count, 'max': max_count}
        )
    
    def _calculate_overall_signal(self, assessments: List[RiskAssessment]) -> Signal:
        """Calculate overall signal from risk assessments"""
        if not assessments:
            return Signal.GREEN
        
        # Count signals
        red_count = sum(1 for a in assessments if a.signal == Signal.RED)
        yellow_count = sum(1 for a in assessments if a.signal == Signal.YELLOW)
        
        # Any critical risk showing RED = overall RED
        critical_red = any(
            a.signal == Signal.RED and a.severity == Severity.CRITICAL 
            for a in assessments
        )
        
        if critical_red or red_count > len(assessments) // 2:
            return Signal.RED
        elif yellow_count > 0 or red_count > 0:
            return Signal.YELLOW
        else:
            return Signal.GREEN
    
    def _serialize_assessment(self, assessment: RiskAssessment) -> Dict[str, Any]:
        """Convert RiskAssessment to dictionary for JSON serialization"""
        return {
            'risk_id': assessment.risk_id,
            'risk_name': assessment.risk_name,
            'severity': assessment.severity.value,
            'signal': assessment.signal.value,
            'checks_passed': assessment.checks_passed,
            'checks_failed': assessment.checks_failed,
            'check_results': [
                {
                    'type': r.check_type,
                    'passed': r.passed,
                    'message': r.message,
                    'details': r.details
                }
                for r in assessment.check_results
            ]
        }
    
    def _print_summary(self, results: Dict[str, Any]) -> None:
        """Print a formatted summary of the results"""
        signal = results['overall_signal']
        signal_emoji = {
            'green': '🟢',
            'yellow': '🟡',
            'red': '🔴'
        }
        
        print("\n" + "="*60)
        print(f"DAMON: {results['damon']}")
        print(f"Domain: {results['domain']}")
        print(f"Overall Signal: {signal_emoji[signal]} {signal.upper()}")
        print("="*60)
        
        for assessment in results['risk_assessments']:
            sig_emoji = signal_emoji[assessment['signal']]
            print(f"\n{sig_emoji} {assessment['risk_name']} ({assessment['risk_id']})")
            print(f"   Severity: {assessment['severity']}")
            print(f"   Checks: {assessment['checks_passed']} passed, {assessment['checks_failed']} failed")
        
        # Print signal interpretation
        print(f"\n{signal_emoji[signal]} Signal Interpretation:")
        signals = self.config.get('signals', {})
        for msg in signals.get(signal, []):
            print(f"   • {msg}")
        
        print("\n" + "="*60 + "\n")


def main():
    """Main entry point for DAMON agent"""
    import argparse
    
    parser = argparse.ArgumentParser(description='DAMON - Domain-Aware Monitoring Node')
    parser.add_argument('config', help='Path to YAML configuration file')
    parser.add_argument('--project-root', default='.', help='Root directory of project to monitor')
    parser.add_argument('--output', help='Output JSON results to file')
    parser.add_argument('--all', action='store_true', help='Run all DAMONs in configs directory')
    
    args = parser.parse_args()
    
    if args.all:
        # Run all DAMONs in the configs directory
        config_dir = Path(args.config)
        if not config_dir.is_dir():
            print(f"Error: {args.config} is not a directory")
            sys.exit(1)
        
        all_results = []
        for config_file in sorted(config_dir.glob('*.yml')):
            agent = DAMONAgent(config_file, args.project_root)
            results = agent.run_checks()
            all_results.append(results)
        
        # Print combined summary
        print("\n" + "="*60)
        print("DAMON FLEET SUMMARY")
        print("="*60)
        
        signal_counts = {'green': 0, 'yellow': 0, 'red': 0}
        for result in all_results:
            signal = result['overall_signal']
            signal_counts[signal] += 1
            emoji = {'green': '🟢', 'yellow': '🟡', 'red': '🔴'}[signal]
            print(f"{emoji} {result['damon']}: {signal.upper()}")
        
        print(f"\nOverall: {signal_counts['green']} green, {signal_counts['yellow']} yellow, {signal_counts['red']} red")
        print("="*60 + "\n")
        
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(all_results, f, indent=2)
            print(f"Results written to {args.output}")
    else:
        # Run single DAMON
        agent = DAMONAgent(args.config, args.project_root)
        results = agent.run_checks()
        
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"Results written to {args.output}")


if __name__ == '__main__':
    main()
