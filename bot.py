# Don't Remove Credit @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot @Tech_VJ
# Ask Doubt on Telegram @KingVJ01

from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram import filters, Client, errors, enums
from pyrogram.errors import UserNotParticipant
from pyrogram.errors.exceptions.flood_420 import FloodWait
from database import add_user, add_group, all_users, all_groups, users, remove_user
from configs import cfg
import random, asyncio

# Initialize the bot
app = Client(
    "approver",
    api_id=cfg.API_ID,
    api_hash=cfg.API_HASH,
    bot_token=cfg.BOT_TOKEN
)

# ━━━━━━━━━━━━━━━━━━━━ Main Process ━━━━━━━━━━━━━━━━━━━━

@app.on_chat_join_request(filters.group | filters.channel)
async def approve(_, m: Message):
    op = m.chat  # Chat details
    kk = m.from_user  # User who sent the join request
    try:
        # Approve the join request
        await app.approve_chat_join_request(op.id, kk.id)

        # Add the user and group to the database
        add_group(m.chat.id)
        add_user(kk.id)

        # Send a private message to the user
        try:
            await app.send_message(
                kk.id,
                f"**Hello {kk.mention}!
Welcome to {m.chat.title}.

__Powered By: @mr_random_backup__**"
            )
        except errors.PeerIdInvalid:
            print(f"Cannot send private message to {kk.id}. The user hasn't started the bot.")
        except Exception as private_msg_error:
            print(f"Error while sending private message: {str(private_msg_error)}")

    except Exception as err:
        print(f"Error approving join request: {str(err)}")

# ━━━━━━━━━━━━━━━━━━━━ Start Command ━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.private & filters.command("start"))
async def start(_, m: Message):
    try:
        # Check if the user is part of the required channel
        await app.get_chat_member(cfg.CHID, m.from_user.id)
    except:
        try:
            invite_link = await app.create_chat_invite_link(int(cfg.CHID))
        except:
            await m.reply("**Make Sure I Am Admin In Your Channel**")
            return 

        key = InlineKeyboardMarkup(
            [[
                InlineKeyboardButton("🍿 Join Update Channel 🍿", url=invite_link.invite_link),
                InlineKeyboardButton("🍀 Check Again 🍀", callback_data="chk")
            ]]
        ) 
        await m.reply_text("**⚠️Access Denied!⚠️\n\nPlease Join My Update Channel To Use Me. If You Joined The Channel Then Click On Check Again Button To Confirm.**", reply_markup=key)
        return 

    keyboard = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton("❤️Developer", url="@Mrdanger998"),
            InlineKeyboardButton("💬 Support", url="https://t.me/+Tq-EYP-n0xI4ZTk9")
        ]]
    )
    add_user(m.from_user.id)
    await m.reply_photo(
        "https://ibb.co/q03Lgt2", 
        caption=f"**🦊 Hello {m.from_user.mention}!
I'm an auto-approve [Admin Join Requests](https://t.me/telegram/153) Bot.
I can approve users in Groups/Channels. Add me to your chat and promote me to admin with add members permission.

__Powered By: @mr_random_backup__**", 
        reply_markup=keyboard
    )

# ━━━━━━━━━━━━━━━━━━━━ Callback Query ━━━━━━━━━━━━━━━━━━━━

@app.on_callback_query(filters.regex("chk"))
async def chk(_, cb: CallbackQuery):
    try:
        await app.get_chat_member(cfg.CHID, cb.from_user.id)
    except:
        await cb.answer("🙅‍♂️ You are not joined my channel. First join the channel then check again. 🙅‍♂️", show_alert=True)
        return 

    keyboard = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton("🔍 Channel", url="https://t.me/+Tq-EYP-n0xI4ZTk9"),
            InlineKeyboardButton("💬 Support", url="https://t.me/+Tq-EYP-n0xI4ZTk9")
        ]]
    )
    add_user(cb.from_user.id)
    await cb.edit_text(
        text=f"**🦊 Hello {cb.from_user.mention}!
I'm an auto-approve [Admin Join Requests](https://t.me/telegram/153) Bot.
I can approve users in Groups/Channels. Add me to your chat and promote me to admin with add members permission.

__Powered By: @mr_random_backup__**", 
        reply_markup=keyboard
    )

# ━━━━━━━━━━━━━━━━━━━━ Run the Bot ━━━━━━━━━━━━━━━━━━━━

print("I'm Alive Now!")
app.run()
