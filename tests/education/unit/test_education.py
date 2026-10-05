from src.services.education.models.schemas import CampusOccupancy
from src.services.education.engine.campus import CampusEngine
from src.services.education.engine.skills import SkillsEngine

def test_campus_overcapacity():
    occupancy = CampusOccupancy(campus_id="CAMPUS-01", current_occupancy=9600, peak_capacity=10000)
    engine = CampusEngine()
    status = engine.evaluate_occupancy(occupancy)
    assert status == "OVERCAPACITY_CANDIDATE"

def test_campus_underutilized():
    occupancy = CampusOccupancy(campus_id="CAMPUS-01", current_occupancy=2000, peak_capacity=10000)
    engine = CampusEngine()
    status = engine.evaluate_occupancy(occupancy)
    assert status == "UNDERUTILIZED"

def test_skill_gap_shortage():
    engine = SkillsEngine()
    gap = engine.evaluate_skill_gap("Robotics", demand=500, capacity=200)
    assert gap.gap_status == "SHORTAGE"

def test_internship_match():
    engine = SkillsEngine()
    match = engine.recommend_internship("STU-100", "COMP-200", skills_overlap=4, required_skills=5, distance=10.0)
    assert match.skill_match_score == 80.0
    
    # Test distance penalty
    match2 = engine.recommend_internship("STU-100", "COMP-300", skills_overlap=5, required_skills=5, distance=40.0)
    # Base score 100, distance penalty (40-20)*0.5 = 10, final = 90
    assert match2.skill_match_score == 90.0
