from flask_login import current_user
from flask_socketio import join_room, emit, leave_room
from model import Message, User
from ext import db


def handle_connect():
    if current_user.is_authenticated:
        join_room(current_user.id)
        print(f"Пользователь с id:{current_user.id} подключился к комнате.")
        emit('after_connect', {'data': 'Соединение установлено.'})
    else:
        print("Ошибка: неавторизованный пользователь попытался подключиться.")
        emit('after_connect', {'data': 'Ошибка подключения: пользователь не авторизован.'})


def handle_send_private_message_event(data):
    if not current_user.is_authenticated:
        print("Ошибка: неавторизованный пользователь пытается отправить сообщение.")
        return emit('error', {'data': 'Вы должны быть авторизованы для отправки сообщений.'})

    if 'recipient_id' not in data or 'message' not in data:
        print("Ошибка: недостающие данные в запросе.")
        return emit('error', {'data': 'Некорректные данные: recipient_id или сообщение отсутствуют.'})

    recipient = User.query.get(data['recipient_id'])
    if not recipient:
        print(f"Ошибка: пользователь с ID {data['recipient_id']} не найден.")
        return emit('error', {'data': f"Пользователь с ID {data['recipient_id']} не найден."})

    message_text = data['message'].strip()
    if not message_text:
        print("Ошибка: отправлено пустое сообщение.")
        return emit('error', {'data': 'Сообщение не может быть пустым.'})


    print(f"Получен запрос на отправку сообщения от пользователя с id:{current_user.id} пользователю с id:{data['recipient_id']}")

    try:
        message = Message(sender_id=current_user.id, recipient_id=data['recipient_id'], content=message_text)
        db.session.add(message)
        db.session.commit()
        print(f"Сообщение от пользователя с id:{current_user.id} для пользователя с id:{data['recipient_id']} сохранено в базе данных.")
        emit('receive_private_message', {
            'sender_id': current_user.id,
            'log': 'Сообщение получено и отправлено',
            'message': data['message']
        }, data['recipient_id'])
        print(f"Сообщение отправлено в комнату с id:{data['recipient_id']}")
    except Exception as e:
        db.session.rollback()
        print(f"Ошибка при сохранении сообщения в базе данных: {e}")
        emit('error', {'data': 'Произошла ошибка при сохранении сообщения.'})

