import uuid
from datetime import datetime, timezone
from src.services.climate.models.schemas import EmissionFactor, CarbonRecord, DataQuality, ConfidenceLevel

class CarbonCalculationEngine:
    """
    Calculates carbon emissions from activity data using versioned emission factors.
    Maintains provenance in a ledger format.
    """
    
    def calculate_emissions(self, 
                            tenant_id: str, 
                            source_id: str,
                            source_category: str,
                            activity_type: str,
                            activity_quantity: float, 
                            activity_unit: str,
                            factor: EmissionFactor,
                            quality: DataQuality = DataQuality.CALCULATED,
                            confidence: ConfidenceLevel = ConfidenceLevel.MEDIUM_CONFIDENCE) -> CarbonRecord:
        
        if factor.unit_activity != activity_unit:
            raise ValueError(f"Activity unit {activity_unit} does not match factor unit {factor.unit_activity}")
            
        emissions = activity_quantity * factor.factor_value
        
        return CarbonRecord(
            carbon_record_id=str(uuid.uuid4()),
            tenant_id=tenant_id,
            territory_id="DEFAULT_TERRITORY",
            source_category=source_category,
            source_id=source_id,
            activity_type=activity_type,
            activity_quantity=activity_quantity,
            activity_unit=activity_unit,
            emission_factor_id=factor.factor_id,
            emission_factor_value=factor.factor_value,
            emission_quantity=emissions,
            emission_unit=factor.unit_emission,
            calculation_method=factor.methodology,
            model_version="carbon-calc-v1",
            data_quality=quality,
            confidence=confidence,
            timestamp=datetime.now(timezone.utc)
        )
