from pydantic import BaseModel
from typing import List, Dict, Any
from src.platform.knowledge.query.plan import QueryPlan

class SearchResult(BaseModel):
    entity_id: str
    relevance_score: float
    source_index: str

class HybridSearchRouter:
    def __init__(self):
        self.indexes = ["vector", "graph", "spatial", "temporal"]
        
    def execute_plan(self, plan: QueryPlan) -> List[SearchResult]:
        """
        Routes the structured QueryPlan to the appropriate indexes.
        """
        results = []
        
        # Simulated routing logic
        if plan.spatial:
            results.append(SearchResult(entity_id=plan.entities[0].type + "_spatial_1", relevance_score=0.9, source_index="spatial"))
            
        if plan.temporal:
            results.append(SearchResult(entity_id=plan.entities[0].type + "_temporal_1", relevance_score=0.85, source_index="temporal"))
            
        # Fallback to vector/semantic
        results.append(SearchResult(entity_id=plan.entities[0].type + "_semantic_1", relevance_score=0.75, source_index="vector"))
        
        # Deduplicate and sort by relevance
        results.sort(key=lambda x: x.relevance_score, reverse=True)
        return results
