from pyrogram.errors import InputUserDeactivated, UserNotParticipant, FloodWait, UserIsBlocked, PeerIdInvalid
import asyncio
import time

async def broadcast_messages(user_id, message):
    try:
        await message.copy(chat_id=user_id)
        return True, "Success"
    except (FloodWait, UserIsBlocked, InputUserDeactivated, UserNotParticipant, PeerIdInvalid) as e:
        # Just return the error, no database
        return False, str(e)
    except Exception as e:
        return False, str(e)
