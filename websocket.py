from flask_socketio import SocketIO, emit, join_room
from flask_login import current_user
from app.services.notification_service import NotificationService

socketio = SocketIO()


@socketio.on('connect')
def handle_connect():
    if current_user.is_authenticated:
        join_room(f'user_{current_user.id}')
        emit('connection_status', {'status': 'connected'})


@socketio.on('disconnect')
def handle_disconnect():
    pass


@socketio.on('read_notification')
def handle_read_notification(data):
    notification_id = data.get('notification_id')
    if notification_id:
        NotificationService.mark_as_read(notification_id)
        emit('notification_updated', {'id': notification_id, 'read': True}) 