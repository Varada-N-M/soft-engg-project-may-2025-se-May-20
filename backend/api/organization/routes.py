from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from models import *
from sqlalchemy import func
from datetime import datetime, timedelta

class OrganizationStats(Resource):
    @jwt_required()
    def get(self):
        """
        Get statistics for the organization.
        """
        try:
            current_user_id = get_jwt_identity()

            # Optional: Check if current user is an organization admin/principal
            user = Users.query.filter(
                Users.user_id == current_user_id,
                Users.is_active == True,
                Users.role_type.in_([UserRole.ADMIN, UserRole.PRINCIPAL, UserRole.ORGANIZATION])
            ).first()
            if not user:
                return {"error": "Unauthorized"}, 403

            # ---------- Stats ----------
            total_children = db.session.query(func.count(Child.child_id)).scalar()
            avg_engagement = 78  # Placeholder, can be calculated from activity logs
            skills_completed = db.session.query(func.count(SkillCompleted.id)).filter(SkillCompleted.is_learned == True).scalar()
            wellbeing_score = 8.4  # Placeholder – can be an aggregate from some scoring table

            # ---------- Development Data ----------
            # Example: group skills by category from CommonSkill if categories exist
            development_data = [
                {"skill": "Time Management", "progress": 85, "target": 90},
                {"skill": "Emotional Regulation", "progress": 72, "target": 80},
                {"skill": "Communication", "progress": 88, "target": 85},
                {"skill": "Financial Literacy", "progress": 65, "target": 75},
                {"skill": "Health & Hygiene", "progress": 92, "target": 90},
                {"skill": "Problem Solving", "progress": 78, "target": 85},
            ]

            # ---------- Engagement Data ----------
            today = datetime.utcnow().date()
            engagement_data = []
            for i in range(7):
                date = today - timedelta(days=i)
                engagement_data.append({
                    "date": date.isoformat(),
                    "engagement": 65 + i,  # dummy trend
                    "completions": 45 + i
                })
            engagement_data.reverse()

            # ---------- Safety Data ----------
            safety_data = {
                "emergencyKnowledge": 78,
                "firstAidBasics": 65,
                "contactInformation": 92,
                "safetyProtocols": 71
            }

            # ---------- Age Distribution ----------
            age_distribution = []
            now = datetime.utcnow().date()
            children = Child.query.all()
            age_groups = {"8-9": 0, "10-11": 0, "12-13": 0, "14": 0}

            for c in children:
                if c.dob:
                    age = (now - c.dob).days // 365
                    if 8 <= age <= 9:
                        age_groups["8-9"] += 1
                    elif 10 <= age <= 11:
                        age_groups["10-11"] += 1
                    elif 12 <= age <= 13:
                        age_groups["12-13"] += 1
                    elif age == 14:
                        age_groups["14"] += 1

            total_count = sum(age_groups.values()) or 1
            age_distribution = [
                {"age": k, "count": v, "percentage": round((v / total_count) * 100, 1)}
                for k, v in age_groups.items()
            ]

            # ---------- Risk Data ----------
            risk_data = {
                "lowRisk": 892,
                "mediumRisk": 287,
                "highRisk": 68,
                "criticalRisk": 12
            }

            # ---------- Child Reports ----------
            child_reports = []
            for c in Child.query.limit(10).all():
                child_reports.append({
                    "id": f"C{c.child_id:03d}",
                    "name": f"{c.user.first_name} {c.user.last_name}" if c.user else "Unknown",
                    "age": (now - c.dob).days // 365 if c.dob else None,
                    "engagement": 80,  # placeholder
                    "skillsCompleted": len(c.skills),
                    "wellbeingScore": 8.0,  # placeholder
                    "lastActive": (now - timedelta(days=1)).isoformat(),
                    "riskLevel": "Low"
                })

            return {
                "stats": {
                    "totalChildren": total_children,
                    "avgEngagement": avg_engagement,
                    "skillsCompleted": skills_completed,
                    "wellbeingScore": wellbeing_score
                },
                "developmentData": development_data,
                "engagementData": engagement_data,
                "safetyData": safety_data,
                "ageData": age_distribution,
                "riskData": risk_data,
                "childReports": child_reports
            }, 200

        except Exception as e:
            return {"error": str(e)}, 500
