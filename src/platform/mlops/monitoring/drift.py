from typing import List, Dict, Any

class DriftDetector:
    """
    Simulates detection of data or concept drift.
    """
    @staticmethod
    def detect_drift(baseline_distribution: List[float], current_distribution: List[float]) -> str:
        """
        Returns HEALTHY, WARNING, or DEGRADED based on simulated distribution shift.
        """
        if not baseline_distribution or not current_distribution:
            return "UNKNOWN"
            
        # Simplified drift check: compare means
        baseline_mean = sum(baseline_distribution) / len(baseline_distribution)
        current_mean = sum(current_distribution) / len(current_distribution)
        
        diff = abs(baseline_mean - current_mean)
        
        if diff > 10.0:
            return "DEGRADED"
        elif diff > 5.0:
            return "WARNING"
        return "HEALTHY"
