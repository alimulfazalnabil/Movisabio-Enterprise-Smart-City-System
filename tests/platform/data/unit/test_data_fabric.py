from src.platform.data_catalog.catalog import DataCatalog, DataProduct
from src.platform.schema_registry.registry import SchemaRegistry
from src.platform.data_quality.validator import DataQualityPipeline

def test_data_catalog():
    catalog = DataCatalog()
    
    prod = DataProduct(
        product_id="traffic.intersection_state",
        name="Traffic Intersection State",
        owner="traffic-domain",
        classification="RESTRICTED",
        version="1.0",
        schema_id="schema_traffic_1",
        description="Real-time intersection traffic state",
        retention_policy="SHORT_TERM"
    )
    
    catalog.register_product(prod)
    
    found = catalog.search_products("traffic")
    assert len(found) == 1
    assert found[0].product_id == "traffic.intersection_state"

def test_schema_registry():
    registry = SchemaRegistry()
    schema_def = {
        "required": ["timestamp", "vehicle_count", "average_speed"],
        "constraints": {
            "vehicle_count": ">= 0",
            "average_speed": ">= 0"
        }
    }
    
    registry.register_schema("traffic_state", "1.0", schema_def)
    
    retrieved = registry.get_schema("traffic_state", "1.0")
    assert retrieved is not None
    assert "vehicle_count" in retrieved["required"]

def test_data_quality_validator():
    schema = {
        "required": ["timestamp", "vehicle_count", "average_speed"],
        "constraints": {
            "vehicle_count": ">= 0",
            "average_speed": ">= 0"
        }
    }
    
    # Valid record
    record1 = {
        "timestamp": "2026-10-02T12:00:00Z",
        "vehicle_count": 15,
        "average_speed": 45.2
    }
    assert DataQualityPipeline.validate_record(record1, schema) == "VALID"
    
    # Missing required field
    record2 = {
        "timestamp": "2026-10-02T12:00:00Z",
        "vehicle_count": 15
    }
    assert DataQualityPipeline.validate_record(record2, schema) == "INVALID"
    
    # Violates constraint
    record3 = {
        "timestamp": "2026-10-02T12:00:00Z",
        "vehicle_count": -5,
        "average_speed": 45.2
    }
    assert DataQualityPipeline.validate_record(record3, schema) == "INVALID"
    
    # Missing data
    assert DataQualityPipeline.validate_record({}, schema) == "MISSING"
