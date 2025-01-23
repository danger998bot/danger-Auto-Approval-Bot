# Updated Auto-Approval Bot Code with Adjustments

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import PeerIdInvalid, FloodWait, UserNotParticipant
from database import add_user, add_group, all_users, all_groups, users, remove_user
from configs import cfg
import asyncio

# Initialize bot
app = Client(
    "approver",
    api_id=cfg.API_ID,
    api_hash=cfg.API_HASH,
    bot_token=cfg.BOT_TOKEN
)

# Welcome photo URL (Replace with your custom welcome image)
WELCOME_PHOTO_URL = "https://via.placeholder.com/600x400.png?text=Welcome+to+the+Group"

# Auto-approve join requests and send private welcome message
@app.on_chat_join_request(filters.group | filters.channel)
async def approve(_, m: Message):
    try:
        add_group(m.chat.id)
        await app.approve_chat_join_request(m.chat.id, m.from_user.id)

        # Send private message to the user
        await app.send_message(
            m.from_user.id,
            f"**Hello {m.from_user.mention}!\nWelcome to {m.chat.title}!\n\nPowered by: @YourChannel**"
        )

        add_user(m.from_user.id)
    except PeerIdInvalid:
        print("User has not started the bot.")
    except Exception as e:
        print(f"Error: {e}")

# Start command handler
@app.on_message(filters.private & filters.command("start"))
async def start(_, m: Message):
    try:
        # Check if the user is in the required channel
        await app.get_chat_member(cfg.CHID, m.from_user.id)
    except UserNotParticipant:
        # Generate invite link if the user is not in the required channel
        try:
            invite_link = await app.create_chat_invite_link(int(cfg.CHID))
        except Exception:
            await m.reply("**Make sure I am an admin in your channel.**")
            return

        key = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("Join Update Channel", url=invite_link.invite_link),
                InlineKeyboardButton("Check Again", callback_data="chk")
            ]
        ])

        await m.reply_text(
            "**Access Denied!**\n\nPlease join my update channel to use me. "
            "If you joined the channel, click on the 'Check Again' button to confirm.",
            reply_markup=key
        )
        return

    # If the user is already in the channel, send the welcome message
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Developer", url="https://t.me/YourChannel"),
            InlineKeyboardButton("Support", url="https://t.me/YourSupportGroup")
        ]
    ])

    add_user(m.from_user.id)
    await m.reply_photo(
        WELCOME_PHOTO_URL,
        caption=(
            f"**Hello {m.from_user.mention}!\n\n"
            "I'm an auto-approval bot for admin join requests."
            "Add me to your group/channel as an admin to get started!\n\n"
            "Powered by: @YourChannel**"
        ),
        reply_markup=keyboard
    )

# Callback query handler for checking channel join status
@app.on_callback_query(filters.regex("chk"))
async def chk(_, cb: CallbackQuery):
    try:
        # Check if the user is in the required channel
        await app.get_chat_member(cfg.CHID, cb.from_user.id)
    except UserNotParticipant:
        await cb.answer("You are not in the required channel. Please join and try again.", show_alert=True)
        return

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Channel", url="https://t.me/YourChannel"),
            InlineKeyboardButton("Support", url="https://t.me/YourSupportGroup")
        ]
    ])

    add_user(cb.from_user.id)
    await cb.edit_message_text(
        text=(
            f"**Hello {cb.from_user.mention}!\n\n"
            "I'm an auto-approval bot for admin join requests."
            "Add me to your group/channel as an admin to get started!\n\n"
            "Powered by: @YourChannel**"
        ),
        reply_markup=keyboard
    )

# Admin-only command to display user and group statistics
@app.on_message(filters.command("users") & filters.user(cfg.SUDO))
async def dbtool(_, m: Message):
    total_users = all_users()
    total_groups = all_groups()
    total = total_users + total_groups

    await m.reply_text(
        f"""
Chats Stats:
- Users: `{total_users}`
- Groups: `{total_groups}`
- Total: `{total}`
        """
    )

# Broadcast messages to all users
@app.on_message(filters.command("bcast") & filters.user(cfg.SUDO))
async def broadcast(_, m: Message):
    all_users_list = users
    processing_msg = await m.reply_text("Processing...")

    success, failed, deactivated, blocked = 0, 0, 0, 0

    for user in all_users_list.find():
        try:
            userid = user["user_id"]
            if m.reply_to_message:
                await m.reply_to_message.copy(int(userid))
            success += 1
        except FloodWait as ex:
            await asyncio.sleep(ex.value)
            continue
        except PeerIdInvalid:
            deactivated += 1
            remove_user(userid)
        except Exception:
            failed += 1

    await processing_msg.edit(
        f"Broadcast Complete:\n- Success: `{success}`\n- Failed: `{failed}`\n"
        f"- Blocked: `{blocked}`\n- Deactivated: `{deactivated}`"
    )

# Run the bot
print("Bot is running...")
app.run()
