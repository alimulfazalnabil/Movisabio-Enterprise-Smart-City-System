from src.services.education.models.schemas import SkillGap, InternshipMatch

class SkillsEngine:
    def evaluate_skill_gap(self, skill_name: str, demand: int, capacity: int) -> SkillGap:
        """
        Evaluates the gap between regional industry demand and training capacity.
        """
        status = "BALANCED"
        if demand > capacity * 1.2:
            status = "SHORTAGE"
        elif capacity > demand * 1.5:
            status = "SURPLUS"
            
        return SkillGap(
            skill_name=skill_name,
            industry_demand=demand,
            training_capacity=capacity,
            gap_status=status
        )

    def recommend_internship(self, student_id: str, company_id: str, skills_overlap: int, required_skills: int, distance: float) -> InternshipMatch:
        """
        Calculates an internship match score based on skills and geographic proximity.
        """
        match_score = (skills_overlap / max(required_skills, 1)) * 100.0
        
        # Penalize for distance > 20km
        if distance > 20:
            match_score -= (distance - 20) * 0.5
            
        return InternshipMatch(
            student_id=student_id,
            company_id=company_id,
            skill_match_score=max(0.0, min(100.0, match_score)),
            distance_km=distance
        )
