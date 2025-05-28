from app import db
from app.models.stats import BoutiqueStats, UserActivity
from datetime import datetime, timedelta
from sqlalchemy import func


class StatsService:
    @staticmethod
    def record_boutique_view(boutique_id):
        today = datetime.utcnow().date()
        stats = BoutiqueStats.query.filter_by(
            boutique_id=boutique_id,
            date=today
        ).first()
        
        if stats:
            stats.views += 1
        else:
            stats = BoutiqueStats(boutique_id=boutique_id, views=1)
            db.session.add(stats)
        
        db.session.commit()
    
    @staticmethod
    def get_boutique_stats(boutique_id, days=30):
        start_date = datetime.utcnow().date() - timedelta(days=days)
        
        stats = BoutiqueStats.query.filter(
            BoutiqueStats.boutique_id == boutique_id,
            BoutiqueStats.date >= start_date
        ).all()
        
        return {
            'total_views': sum(s.views for s in stats),
            'total_searches': sum(s.searches for s in stats),
            'daily_stats': [{
                'date': s.date.strftime('%Y-%m-%d'),
                'views': s.views,
                'searches': s.searches
            } for s in stats]
        }
    
    @staticmethod
    def record_user_activity(user_id, action, details=None):
        activity = UserActivity(
            user_id=user_id,
            action=action,
            details=details or {}
        )
        db.session.add(activity)
        db.session.commit() 