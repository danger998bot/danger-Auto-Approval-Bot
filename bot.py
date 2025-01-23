# Don't Remove Credit @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot @Tech_VJ
# Ask Doubt on telegram @KingVJ01

from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram import filters, Client, errors, enums
from pyrogram.errors import UserNotParticipant
from pyrogram.errors.exceptions.flood_420 import FloodWait
from database import add_user, add_group, all_users, all_groups, users, remove_user
from configs import cfg
import random, asyncio

app = Client(
    "approver",
    api_id=cfg.API_ID,
    api_hash=cfg.API_HASH,
    bot_token=cfg.BOT_TOKEN
)

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Main process ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_chat_join_request(filters.group | filters.channel)
async def approve(_, m: Message):
    op = m.chat
    kk = m.from_user
    try:
        add_group(m.chat.id)
        await app.approve_chat_join_request(op.id, kk.id)
        await app.send_message(
            kk.id,
            f"**Hello {m.from_user.mention}!\nWelcome to {m.chat.title}.\n\n__Powered By: @mr_random_backup__**"
        )
        add_user(kk.id)
    except errors.PeerIdInvalid:
        print("User hasn't started the bot (Group only).")
    except Exception as err:
        print(f"Error: {str(err)}")


#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Start ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.private & filters.command("start"))
async def start(_, m: Message):
    try:
        # Check if user is already a member of the channel
        await app.get_chat_member(cfg.CHID, m.from_user.id)
    except UserNotParticipant:
        try:
            invite_link = await app.create_chat_invite_link(int(cfg.CHID))
        except errors.ChatAdminRequired:
            await m.reply("❌ I need admin rights in the channel to create an invite link.")
            return
        except Exception as err:
            await m.reply(f"❌ An unexpected error occurred: {err}")
            return

        # Prompt user to join the channel
        key = InlineKeyboardMarkup(
            [[
                InlineKeyboardButton("🍿 Join Update Channel 🍿", url=invite_link.invite_link),
                InlineKeyboardButton("🍀 Check Again 🍀", callback_data="chk")
            ]]
        )
        await m.reply_text(
            "**⚠️ Access Denied! ⚠️\n\n"
            "Please join my update channel to use me. Once joined, click 'Check Again' to confirm.**",
            reply_markup=key
        )
        return

    # Send welcome message
    keyboard = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton("❤️ Developer", url="https://t.me/Mrdanger998"),
            InlineKeyboardButton("💬 Support", url="https://t.me/+Tq-EYP-n0xI4ZTk9")
        ]]
    )
    user_mention = m.from_user.mention or m.from_user.first_name
    await m.reply_photo(
        "https://via.placeholder.com/500",
        caption=(
            f"**🦊 Hello {user_mention}!\n"
            "I'm an auto-approve bot for Admin Join Requests.\n"
            "Add me to your group/channel as admin to get started!**"
        ),
        reply_markup=keyboard
    )


#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Callback ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_callback_query(filters.regex("chk"))
async def chk(_, cb: CallbackQuery):
    try:
        await app.get_chat_member(cfg.CHID, cb.from_user.id)
    except UserNotParticipant:
        await cb.answer("🙅‍♂️ You haven't joined the channel. Join it and try again.", show_alert=True)
        return

    keyboard = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton("🗯 Channel", url="https://t.me/+Tq-EYP-n0xI4ZTk9"),
            InlineKeyboardButton("💬 Support", url="https://t.me/+Tq-EYP-n0xI4ZTk9")
        ]]
    )
    await cb.edit_message_text(
        text=(
            f"**🦊 Hello {cb.from_user.mention}!\n"
            "I'm an auto-approve bot for Admin Join Requests.\n"
            "Add me to your group/channel as admin to get started!**"
        ),
        reply_markup=keyboard
    )


#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Info ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.command("users") & filters.user(cfg.SUDO))
async def dbtool(_, m: Message):
    xx = all_users()
    x = all_groups()
    tot = int(xx + x)
    await m.reply_text(
        f"""
🍀 Chats Stats 🍀
🙋‍♂️ Users : `{xx}`
👥 Groups : `{x}`
🚧 Total users & groups : `{tot}` """
    )


#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Broadcast ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.command("bcast") & filters.user(cfg.SUDO))
async def bcast(_, m: Message):
    allusers = users
    lel = await m.reply_text("`⚡️ Processing...`")
    success = 0
    failed = 0
    deactivated = 0
    blocked = 0
    for usrs in allusers.find():
        try:
            userid = usrs["user_id"]
            await m.reply_to_message.copy(int(userid))
            success += 1
        except FloodWait as ex:
            await asyncio.sleep(ex.value)
            await m.reply_to_message.copy(int(userid))
        except errors.InputUserDeactivated:
            deactivated += 1
            remove_user(userid)
        except errors.UserIsBlocked:
            blocked += 1
        except Exception as e:
            print(e)
            failed += 1

    await lel.edit(
        f"✅ Success to `{success}` users.\n"
        f"❌ Failed to `{failed}` users.\n"
        f"👾 Blocked: `{blocked}` users.\n"
        f"👻 Deactivated: `{deactivated}` users."
    )

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Broadcast Forward ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.command("fcast") & filters.user(cfg.SUDO))
async def fcast(_, m: Message):
    allusers = users
    lel = await m.reply_text("`⚡️ Processing...`")
    success = 0
    failed = 0
    deactivated = 0
    blocked = 0
    for usrs in allusers.find():
        try:
            userid = usrs["user_id"]
            await m.reply_to_message.forward(int(userid))
            success += 1
        except FloodWait as ex:
            await asyncio.sleep(ex.value)
            await m.reply_to_message.forward(int(userid))
        except errors.InputUserDeactivated:
            deactivated += 1
            remove_user(userid)
        except errors.UserIsBlocked:
            blocked += 1
        except Exception as e:
            print(e)
            failed += 1

    await lel.edit(
        f"✅ Success to `{success}` users.\n"
        f"❌ Failed to `{failed}` users.\n"
        f"👾 Blocked: `{blocked}` users.\n"
        f"👻 Deactivated: `{deactivated}` users."
    )

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Bot Initialization ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

print("I'm Alive Now!")
app.run()
