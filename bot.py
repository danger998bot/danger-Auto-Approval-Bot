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

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Main process ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_chat_join_request(filters.group | filters.channel)
async def approve(_, m: Message):
    chat = m.chat
    user = m.from_user
    try:
        add_group(chat.id)
        await app.approve_chat_join_request(chat.id, user.id)
        await app.send_message(
            user.id, 
            "**Hello {}!**\nWelcome to **{}** 🎉\n\n__Powered By : @mr_random_backup__".format(
                user.mention, chat.title
            )
        )
        add_user(user.id)
    except errors.PeerIdInvalid:
        print("User hasn't started the bot (group join).")
    except Exception as err:
        print(f"Error: {err}")

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Start ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.private & filters.command("start"))
async def start(_, m: Message):
    try:
        await app.get_chat_member(cfg.CHID, m.from_user.id)
    except:
        try:
            invite_link = await app.create_chat_invite_link(int(cfg.CHID))
        except:
            await m.reply("**Make sure I am an admin in your channel.**")
            return 
        key = InlineKeyboardMarkup(
            [[
                InlineKeyboardButton("🍿 Join Update Channel 🍿", url=invite_link.invite_link),
                InlineKeyboardButton("🍀 Check Again 🍀", callback_data="chk")
            ]]
        ) 
        await m.reply_text(
            "**⚠️ Access Denied! ⚠️\n\nPlease join my update channel to use me. If you have joined, click the 'Check Again' button to confirm.**", 
            reply_markup=key
        )
        return 
    keyboard = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton("❤️ Developer", url="@Mrdanger998"),
            InlineKeyboardButton("💬 Support", url="https://t.me/+Tq-EYP-n0xI4ZTk9")
        ]]
    )
    add_user(m.from_user.id)
    await m.reply_photo(
        "https://img.freepik.com/free-photo/flat-lay-welcome-note-with-copy-space_23-2148719638.jpg",  # Replace with your chosen welcome image URL
        caption="**🦊 Hello {}!**\nI'm an auto approve [Admin Join Requests]({}) bot.\n\nI can approve users in Groups/Channels. Add me to your chat and promote me to admin with 'Add Members' permission.\n\n__Powered By : @mr_random_backup__".format(
            m.from_user.mention, "https://t.me/telegram/153"
        ),
        reply_markup=keyboard
    )

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Callback ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_callback_query(filters.regex("chk"))
async def chk(_, cb: CallbackQuery):
    try:
        await app.get_chat_member(cfg.CHID, cb.from_user.id)
    except:
        await cb.answer("🙅‍♂️ You have not joined the channel. Please join and then check again.", show_alert=True)
        return 
    keyboard = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton("🗯 Channel", url="https://t.me/+Tq-EYP-n0xI4ZTk9"),
            InlineKeyboardButton("💬 Support", url="https://t.me/+Tq-EYP-n0xI4ZTk9")
        ]]
    )
    add_user(cb.from_user.id)
    await cb.edit_text(
        text="**🦊 Hello {}!**\nI'm an auto approve [Admin Join Requests]({}) bot.\n\nI can approve users in Groups/Channels. Add me to your chat and promote me to admin with 'Add Members' permission.\n\n__Powered By : @mr_random_backup__".format(
            cb.from_user.mention, "https://t.me/telegram/153"
        ), 
        reply_markup=keyboard
    )

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Broadcast & Tools ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.command("users") & filters.user(cfg.SUDO))
async def dbtool(_, m: Message):
    xx = all_users()
    x = all_groups()
    tot = int(xx + x)
    await m.reply_text(
        f"""
🍀 Chats Stats 🍀
🙋‍♂️ Users: `{xx}`
👥 Groups: `{x}`
🚧 Total Users & Groups: `{tot}`"""
    )

@app.on_message(filters.command("bcast") & filters.user(cfg.SUDO))
async def bcast(_, m: Message):
    allusers = users
    lel = await m.reply_text("`⚡️ Processing...`")
    success, failed, deactivated, blocked = 0, 0, 0, 0
    for usrs in allusers.find():
        try:
            userid = usrs["user_id"]
            if m.command[0] == "bcast":
                await m.reply_to_message.copy(int(userid))
            success += 1
        except FloodWait as ex:
            await asyncio.sleep(ex.value)
            if m.command[0] == "bcast":
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
        f"✅ Successful to `{success}` users.\n❌ Failed to `{failed}` users.\n👾 Found `{blocked}` blocked users.\n👻 Found `{deactivated}` deactivated users."
    )

print("I'm Alive Now!")
app.run()
