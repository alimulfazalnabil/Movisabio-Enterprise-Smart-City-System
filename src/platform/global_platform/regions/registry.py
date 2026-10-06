from pydantic import BaseModel
from typing import Dict, List

class Region(BaseModel):
    region_id: str
    region_code: str
    jurisdiction_id: str
    provider: str
    status: str = "HEALTHY" # HEALTHY, DEGRADED, OFFLINE
    is_primary: bool = False

class RegionRegistry:
    def __init__(self):
        self.regions: Dict[str, Region] = {}
        
    def register(self, region: Region) -> None:
        self.regions[region.region_id] = region
        
    def get_region(self, region_id: str) -> Region:
        return self.regions.get(region_id)
        
    def update_health(self, region_id: str, status: str) -> bool:
        if region_id in self.regions:
            self.regions[region_id].status = status
            return True
        return False
