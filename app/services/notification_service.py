from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.notification import Notification

async def create_notification(db: AsyncSession, user_id: int, type: str, title: str, message: str, metadata=None):
    notif = Notification(user_id=user_id, type=type, title=title, message=message, metadata_info=metadata)
    db.add(notif)
    await db.commit()
    await db.refresh(notif)
    return notif

async def get_user_notifications(db: AsyncSession, user_id: int, unread_only=False):
    q = select(Notification).filter(Notification.user_id == user_id)
    if unread_only:
        q = q.filter(Notification.read == False)
    result = await db.execute(q)
    return result.scalars().all()

async def mark_read(db: AsyncSession, notification_id: int, user_id: int):
    notif = (await db.execute(select(Notification).filter(Notification.id == notification_id, Notification.user_id == user_id))).scalars().first()
    if notif:
        notif.read = True
        await db.commit()
        return True
    return False

def send_sms(phone: str, message: str) -> bool:
    print(f"Twilio Stub: Sent SMS to {phone} - {message}")
    return True

def send_whatsapp(phone: str, message: str) -> bool:
    print(f"WhatsApp Stub: Sent to {phone} - {message}")
    return True
