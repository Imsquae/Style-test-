from app.models import UserActivity
from datetime import datetime, timedelta


def get_recent_activities(days=7):
    """Get user activities from the last X days"""
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    
    return UserActivity.query.filter(
        UserActivity.timestamp >= cutoff_date
    ).order_by(
        UserActivity.timestamp.desc()
    ).limit(20).all() 