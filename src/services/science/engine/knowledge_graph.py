from src.services.science.models.schemas import Publication
from typing import List

class KnowledgeGraphEngine:
    def __init__(self, publications: List[Publication]):
        self.publications = {pub.publication_id: pub for pub in publications}
        
    def filter_evidence(self, target_evidence_levels: List[str]) -> List[Publication]:
        """
        Retrieves publications that match verified levels of evidence, intentionally ignoring non-peer-reviewed/AI hypotheses.
        """
        return [
            pub for pub in self.publications.values() 
            if pub.evidence_level in target_evidence_levels
        ]
        
    def find_citations(self, publication_id: str) -> List[Publication]:
        """
        Resolves the citations of a given publication to actual Publication objects.
        """
        if publication_id not in self.publications:
            return []
            
        pub = self.publications[publication_id]
        cited_pubs = []
        for cited_id in pub.citations:
            if cited_id in self.publications:
                cited_pubs.append(self.publications[cited_id])
                
        return cited_pubs
