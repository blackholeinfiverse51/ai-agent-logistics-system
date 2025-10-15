"""
Employee Management API - Advanced Features
Performance reviews, training modules, gamification, and wellness tracking
"""

from fastapi import APIRouter, HTTPException, Depends, Request
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import json
import asyncio
from dataclasses import dataclass, asdict
from enum import Enum

from ..modules.bhiv_core_integration import bhiv_core_integration
from ..unified_logging.logger import UnifiedLogger
from ..event_broker.event_broker import EventBroker

router = APIRouter()
unified_logger = UnifiedLogger()
event_broker = EventBroker()

class ReviewType(Enum):
    ANNUAL = "annual"
    MID_YEAR = "mid_year"
    PROJECT = "project"
    PROBATION = "probation"

class BadgeType(Enum):
    PRODUCTIVITY = "productivity"
    QUALITY = "quality"
    TEAMWORK = "teamwork"
    INNOVATION = "innovation"
    LEADERSHIP = "leadership"

@dataclass
class PerformanceReview:
    id: str
    employee_id: str
    reviewer_id: str
    review_type: ReviewType
    period_start: datetime
    period_end: datetime
    metrics: Dict[str, Any]
    ai_report: str
    manager_feedback: str
    employee_feedback: str
    overall_rating: float
    status: str
    created_at: datetime
    updated_at: datetime

@dataclass
class TrainingModule:
    id: str
    title: str
    description: str
    category: str
    difficulty: str
    estimated_duration: int  # minutes
    prerequisites: List[str]
    learning_objectives: List[str]
    gurukul_pipeline: str
    content_url: str
    created_at: datetime

@dataclass
class LearningPath:
    id: str
    employee_id: str
    title: str
    description: str
    modules: List[str]
    progress: Dict[str, float]  # module_id -> completion percentage
    status: str
    created_at: datetime
    completed_at: Optional[datetime]

@dataclass
class Badge:
    id: str
    employee_id: str
    badge_type: BadgeType
    title: str
    description: str
    icon_url: str
    earned_at: datetime
    criteria: Dict[str, Any]

@dataclass
class LeaderboardEntry:
    employee_id: str
    employee_name: str
    score: float
    rank: int
    badges_count: int
    metrics: Dict[str, Any]

@dataclass
class WellnessRecord:
    id: str
    employee_id: str
    date: datetime
    work_hours: float
    break_count: int
    stress_level: int  # 1-10
    energy_level: int  # 1-10
    sleep_hours: float
    exercise_minutes: int
    last_break_reminder: Optional[datetime]

# In-memory storage for demo (would be database in production)
performance_reviews = {}
training_modules = {}
learning_paths = {}
badges = {}
wellness_records = {}

@router.post("/performance-reviews")
async def create_performance_review(request: Request):
    """Create a performance review with AI-generated report"""
    try:
        data = await request.json()
        employee_id = data.get("employee_id")
        reviewer_id = data.get("reviewer_id")
        review_type = data.get("review_type", "annual")

        if not employee_id or not reviewer_id:
            raise HTTPException(status_code=400, detail="Employee ID and reviewer ID required")

        # Generate AI report using UniGuru
        ai_report = await generate_ai_performance_report(employee_id, review_type)

        review = PerformanceReview(
            id=f"review_{len(performance_reviews) + 1}",
            employee_id=employee_id,
            reviewer_id=reviewer_id,
            review_type=ReviewType(review_type),
            period_start=datetime.now() - timedelta(days=365),
            period_end=datetime.now(),
            metrics=data.get("metrics", {}),
            ai_report=ai_report,
            manager_feedback="",
            employee_feedback="",
            overall_rating=0.0,
            status="draft",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

        performance_reviews[review.id] = review

        # Log event
        await event_broker.publish_event({
            "event_type": "performance_review_created",
            "source_system": "employee_management",
            "payload": {
                "review_id": review.id,
                "employee_id": employee_id,
                "reviewer_id": reviewer_id,
                "ai_report_generated": True
            }
        })

        return {"status": "created", "review_id": review.id, "ai_report": ai_report}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create performance review: {str(e)}")

@router.get("/performance-reviews/{employee_id}")
async def get_employee_reviews(employee_id: str):
    """Get performance reviews for an employee"""
    reviews = [asdict(review) for review in performance_reviews.values()
               if review.employee_id == employee_id]
    return {"reviews": reviews}

@router.put("/performance-reviews/{review_id}")
async def update_performance_review(review_id: str, request: Request):
    """Update performance review with feedback"""
    try:
        if review_id not in performance_reviews:
            raise HTTPException(status_code=404, detail="Review not found")

        data = await request.json()
        review = performance_reviews[review_id]

        if "manager_feedback" in data:
            review.manager_feedback = data["manager_feedback"]
        if "employee_feedback" in data:
            review.employee_feedback = data["employee_feedback"]
        if "overall_rating" in data:
            review.overall_rating = data["overall_rating"]
        if "status" in data:
            review.status = data["status"]

        review.updated_at = datetime.now()

        return {"status": "updated", "review": asdict(review)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update review: {str(e)}")

@router.post("/training-modules")
async def create_training_module(request: Request):
    """Create a training module with Gurukul integration"""
    try:
        data = await request.json()

        module = TrainingModule(
            id=f"module_{len(training_modules) + 1}",
            title=data["title"],
            description=data["description"],
            category=data["category"],
            difficulty=data.get("difficulty", "intermediate"),
            estimated_duration=data.get("estimated_duration", 60),
            prerequisites=data.get("prerequisites", []),
            learning_objectives=data.get("learning_objectives", []),
            gurukul_pipeline=data.get("gurukul_pipeline", "default"),
            content_url=data.get("content_url", ""),
            created_at=datetime.now()
        )

        training_modules[module.id] = module

        # Log event
        await event_broker.publish_event({
            "event_type": "training_module_created",
            "source_system": "employee_management",
            "payload": {
                "module_id": module.id,
                "title": module.title,
                "category": module.category
            }
        })

        return {"status": "created", "module": asdict(module)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create training module: {str(e)}")

@router.get("/training-modules")
async def get_training_modules(category: Optional[str] = None):
    """Get all training modules, optionally filtered by category"""
    modules = list(training_modules.values())
    if category:
        modules = [m for m in modules if m.category == category]

    return {"modules": [asdict(m) for m in modules]}

@router.post("/learning-paths")
async def create_learning_path(request: Request):
    """Create personalized learning path for employee"""
    try:
        data = await request.json()
        employee_id = data["employee_id"]
        modules = data["modules"]

        # Generate personalized path using Gurukul
        personalized_modules = await generate_personalized_learning_path(employee_id, modules)

        path = LearningPath(
            id=f"path_{len(learning_paths) + 1}",
            employee_id=employee_id,
            title=data.get("title", "Personalized Learning Path"),
            description=data.get("description", ""),
            modules=personalized_modules,
            progress={module_id: 0.0 for module_id in personalized_modules},
            status="active",
            created_at=datetime.now(),
            completed_at=None
        )

        learning_paths[path.id] = path

        return {"status": "created", "path": asdict(path)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create learning path: {str(e)}")

@router.get("/learning-paths/{employee_id}")
async def get_employee_learning_paths(employee_id: str):
    """Get learning paths for an employee"""
    paths = [asdict(path) for path in learning_paths.values()
             if path.employee_id == employee_id]
    return {"paths": paths}

@router.put("/learning-paths/{path_id}/progress")
async def update_learning_progress(path_id: str, request: Request):
    """Update progress on a learning path"""
    try:
        if path_id not in learning_paths:
            raise HTTPException(status_code=404, detail="Learning path not found")

        data = await request.json()
        module_id = data["module_id"]
        progress = data["progress"]

        path = learning_paths[path_id]
        path.progress[module_id] = progress

        # Check if path is completed
        if all(p >= 100.0 for p in path.progress.values()):
            path.status = "completed"
            path.completed_at = datetime.now()

        return {"status": "updated", "path": asdict(path)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update progress: {str(e)}")

@router.post("/badges/earn")
async def earn_badge(request: Request):
    """Award a badge to an employee"""
    try:
        data = await request.json()
        employee_id = data["employee_id"]
        badge_type = BadgeType(data["badge_type"])

        # Check if employee qualifies for badge
        qualifies = await check_badge_eligibility(employee_id, badge_type)

        if not qualifies:
            raise HTTPException(status_code=400, detail="Employee does not qualify for this badge")

        badge = Badge(
            id=f"badge_{len(badges) + 1}",
            employee_id=employee_id,
            badge_type=badge_type,
            title=data.get("title", f"{badge_type.value.title()} Badge"),
            description=data.get("description", ""),
            icon_url=data.get("icon_url", ""),
            earned_at=datetime.now(),
            criteria=data.get("criteria", {})
        )

        badges[badge.id] = badge

        # Log event
        await event_broker.publish_event({
            "event_type": "badge_earned",
            "source_system": "employee_management",
            "payload": {
                "badge_id": badge.id,
                "employee_id": employee_id,
                "badge_type": badge_type.value
            }
        })

        return {"status": "earned", "badge": asdict(badge)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to earn badge: {str(e)}")

@router.get("/badges/{employee_id}")
async def get_employee_badges(employee_id: str):
    """Get badges earned by an employee"""
    employee_badges = [asdict(badge) for badge in badges.values()
                      if badge.employee_id == employee_id]
    return {"badges": employee_badges}

@router.get("/leaderboard")
async def get_leaderboard(limit: int = 10):
    """Get employee leaderboard"""
    # Calculate scores based on badges, performance, etc.
    leaderboard = await calculate_leaderboard_scores()

    return {"leaderboard": leaderboard[:limit]}

@router.post("/wellness/record")
async def record_wellness_data(request: Request):
    """Record employee wellness data"""
    try:
        data = await request.json()
        employee_id = data["employee_id"]

        record = WellnessRecord(
            id=f"wellness_{len(wellness_records) + 1}",
            employee_id=employee_id,
            date=datetime.now(),
            work_hours=data.get("work_hours", 0.0),
            break_count=data.get("break_count", 0),
            stress_level=data.get("stress_level", 5),
            energy_level=data.get("energy_level", 5),
            sleep_hours=data.get("sleep_hours", 8.0),
            exercise_minutes=data.get("exercise_minutes", 0),
            last_break_reminder=None
        )

        wellness_records[record.id] = record

        # Check if break reminder needed
        if record.work_hours > 4 and record.break_count == 0:
            await send_break_reminder(employee_id)

        return {"status": "recorded", "record": asdict(record)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to record wellness data: {str(e)}")

@router.get("/wellness/{employee_id}")
async def get_employee_wellness(employee_id: str, days: int = 7):
    """Get wellness data for an employee"""
    cutoff_date = datetime.now() - timedelta(days=days)
    records = [asdict(record) for record in wellness_records.values()
               if record.employee_id == employee_id and record.date >= cutoff_date]

    return {"records": records}

@router.post("/wellness/break-reminder/{employee_id}")
async def send_break_reminder(employee_id: str):
    """Send break reminder to employee"""
    try:
        # Update last reminder time
        for record in wellness_records.values():
            if record.employee_id == employee_id:
                record.last_break_reminder = datetime.now()
                break

        # Send reminder via event broker
        await event_broker.publish_event({
            "event_type": "break_reminder",
            "source_system": "employee_management",
            "target_systems": ["notification"],
            "payload": {
                "employee_id": employee_id,
                "message": "You've been working for 4+ hours. Consider taking a short break to recharge!",
                "timestamp": datetime.now().isoformat()
            },
            "priority": "normal"
        })

        return {"status": "reminder_sent"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send break reminder: {str(e)}")

# Helper functions

async def generate_ai_performance_report(employee_id: str, review_type: str) -> str:
    """Generate AI performance report using UniGuru"""
    try:
        # Query UniGuru for performance analysis
        query = f"Analyze performance data for employee {employee_id} for {review_type} review"
        context = {
            "employee_id": employee_id,
            "review_type": review_type,
            "analysis_type": "performance_review"
        }

        result = await bhiv_core_integration.query_uniguru(query, context)

        if result.get("success"):
            return result.get("response", "AI report generation failed")
        else:
            return "Unable to generate AI performance report at this time."

    except Exception as e:
        return f"Error generating AI report: {str(e)}"

async def generate_personalized_learning_path(employee_id: str, base_modules: List[str]) -> List[str]:
    """Generate personalized learning path using Gurukul"""
    try:
        query = f"Personalize learning path for employee {employee_id} based on their performance and skill gaps"
        context = {
            "employee_id": employee_id,
            "base_modules": base_modules,
            "personalization_type": "learning_path"
        }

        result = await bhiv_core_integration.query_gurukul(query, "learning_pipeline")

        if result.get("success"):
            # Return personalized module order
            return result.get("modules", base_modules)
        else:
            return base_modules

    except Exception as e:
        return base_modules

async def check_badge_eligibility(employee_id: str, badge_type: BadgeType) -> bool:
    """Check if employee qualifies for a badge"""
    # Simple eligibility check - in production would analyze performance data
    employee_badges = [b for b in badges.values() if b.employee_id == employee_id]
    return len(employee_badges) < 5  # Limit to 5 badges per employee for demo

async def calculate_leaderboard_scores() -> List[Dict[str, Any]]:
    """Calculate leaderboard scores"""
    scores = {}
    for badge in badges.values():
        if badge.employee_id not in scores:
            scores[badge.employee_id] = {
                "employee_id": badge.employee_id,
                "employee_name": f"Employee {badge.employee_id}",
                "score": 0.0,
                "badges_count": 0,
                "metrics": {}
            }
        scores[badge.employee_id]["score"] += 10.0  # 10 points per badge
        scores[badge.employee_id]["badges_count"] += 1

    # Sort by score
    leaderboard = sorted(scores.values(), key=lambda x: x["score"], reverse=True)

    # Add ranks
    for i, entry in enumerate(leaderboard, 1):
        entry["rank"] = i

    return leaderboard