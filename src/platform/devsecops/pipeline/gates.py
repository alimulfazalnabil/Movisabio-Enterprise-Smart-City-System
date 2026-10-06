from pydantic import BaseModel
from typing import List, Dict, Optional

class SBOM(BaseModel):
    artifact_id: str
    version: str
    commit_sha: str
    dependencies: List[Dict[str, str]]
    vulnerabilities: List[Dict[str, str]] = []
    signature: Optional[str] = None

class QualityGate:
    @staticmethod
    def evaluate(test_results: Dict[str, bool], security_results: Dict[str, bool]) -> bool:
        """
        All tests and security scans must pass.
        """
        for check, passed in test_results.items():
            if not passed:
                return False
                
        for check, passed in security_results.items():
            if not passed:
                return False
                
        return True

class SecurityGate:
    @staticmethod
    def scan_secrets(commits: List[str]) -> bool:
        """
        Mock implementation of secret scanning.
        """
        suspicious = ["api_key=", "password=", "secret=", "token="]
        for commit in commits:
            for s in suspicious:
                if s in commit.lower():
                    return False
        return True
