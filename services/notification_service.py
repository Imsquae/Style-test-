from app import db
from app.models.notification import Notification
from flask_socketio import SocketIO

socketio = SocketIO()


class NotificationService:
    @staticmethod
    def create_notification(user_id, title, message, type='info'):
        notification = Notification(
            user_id=user_id,
            title=title,
            message=message,
            type=type
        )
        db.session.add(notification)
        db.session.commit()
        
        # Envoyer la notification en temps réel
        socketio.emit('new_notification', {
            'title': title,
            'message': message,
            'type': type
        }, room=f'user_{user_id}')
        
        return notification
    
    @staticmethod
    def mark_as_read(notification_id):
        notification = Notification.query.get(notification_id)
        if notification:
            notification.read = True
            db.session.commit()
    
    @staticmethod
    def get_unread_notifications(user_id):
        return Notification.query.filter_by(
            user_id=user_id,
            read=False
        ).order_by(Notification.created_at.desc()).all() 