from typing import Dict, Any, List

class DataQualityPipeline:
    """
    Quality status: VALID, SUSPECT, STALE, INVALID, MISSING, UNKNOWN
    """
    
    @staticmethod
    def validate_record(record: Dict[str, Any], schema: Dict[str, Any]) -> str:
        """
        Validates a record against a simple schema.
        Returns the quality status.
        Never treat missing data as zero.
        """
        if not record:
            return "MISSING"
            
        required_fields = schema.get("required", [])
        for field in required_fields:
            if field not in record or record[field] is None:
                return "INVALID" # Missing required field
                
        # Basic constraints check
        constraints = schema.get("constraints", {})
        for field, constraint in constraints.items():
            val = record.get(field)
            if val is not None:
                if constraint == ">= 0" and isinstance(val, (int, float)) and val < 0:
                    return "INVALID"
                    
        return "VALID"
