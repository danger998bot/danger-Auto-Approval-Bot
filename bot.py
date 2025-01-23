# Don't Remove Credit @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot @Tech_VJ
# Ask Doubt on telegram @KingVJ01

from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram import filters, Client, errors
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
    op = m.chat
    kk = m.from_user
    try:
        add_group(m.chat.id)
        await app.approve_chat_join_request(op.id, kk.id)

        # Inline buttons for multiple channels
        buttons = InlineKeyboardMarkup(
            [[
                InlineKeyboardButton("📢 private videos 18+", url="https://t.me/+XFWF3LihbuljNTY1"),
                InlineKeyboardButton("📢 onlyfan videos 18+", url="https://t.me/+BYavxhRxesc1YjY1"),
            ], [
                InlineKeyboardButton("Other viral videos", url="https://t.me/+ZfVKCqE6_wA0MjQ1")
            ]]
        )

        # Send photo with the welcome message and buttons
        await app.send_photo(
            kk.id,
            photo="https://ibb.co/q03Lgt2",  # Replace with your image URL
            caption=(
                f"**👋 Welcome, {kk.mention}!**\n\n"
                f"🌟 We're thrilled to have you in **{m.chat.title}**!\n\n"
                f"🔗 Check out our channels for the latest updates:\n"
                f"- [private videos 18+](https://t.me/+XFWF3LihbuljNTY1)\n"
                f"- [onlyfan videos 18+](https://t.me/+BYavxhRxesc1YjY1)\n"
                f"- [Other viral videos](https://t.me/+ZfVKCqE6_wA0MjQ1)\n\n"
                f"__Enjoy your stay and stay connected!__\n\n"
                f"Powered By: @mr_random_backup"
            ),
            reply_markup=buttons
        )
        add_user(kk.id)
    except errors.PeerIdInvalid:
        print("User hasn't started the bot yet.")
    except Exception as err:
        print(str(err))


#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Start ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.private & filters.command("start"))
async def op(_, m: Message):
    try:
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
        await m.reply_text(
            "**⚠️Access Denied!⚠️\n\nPlease Join My Update Channel To Use Me. If You Joined The Channel Then Click On Check Again Button To Confirm.**",
            reply_markup=key
        )
        return
    keyboard = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton("❤️Developer", url="@Mrdanger998"),
            InlineKeyboardButton("💬 Support", url="https://t.me/+Tq-EYP-n0xI4ZTk9")
        ]]
    )
    add_user(m.from_user.id)
    await m.reply_photo(
        "https://graph.org/file/d57d6f83abb6b8d0efb02.jpg",
        caption=(
            f"**🦊 Hello {m.from_user.mention}!\nI'm an auto approve [Admin Join Requests]"
            f"(https://t.me/telegram/153) Bot.\nI can approve users in Groups/Channels."
            f"Add me to your chat and promote me to admin with add members permission.\n\n"
            f"__Powered By : @VJ_Botz__**"
        ),
        reply_markup=keyboard
    )


#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ callback ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_callback_query(filters.regex("chk"))
async def chk(_, cb: CallbackQuery):
    try:
        await app.get_chat_member(cfg.CHID, cb.from_user.id)
    except:
        await cb.answer("🙅♂️ You are not joined my channel first join channel then check again. 🙅♂️", show_alert=True)
        return
    keyboard = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton("❤️Developer", url="@Mrdanger998"),
            InlineKeyboardButton("💬 Support", url="https://t.me/+Tq-EYP-n0xI4ZTk9")
        ]]
    )
    await cb.edit_text(
        text=(
            f"**🦊 Hello {cb.from_user.mention}!\nI'm an auto approve [Admin Join Requests]"
            f"(https://t.me/telegram/153) Bot.\nI can approve users in Groups/Channels."
            f"Add me to your chat and promote me to admin with add members permission.\n\n"
            f"__Powered By : @VJ_Botz__**"
        ),
        reply_markup=keyboard
    )


#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ info ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.command("users") & filters.user(cfg.SUDO))
async def dbtool(_, m: Message):
    xx = all_users()
    x = all_groups()
    tot = int(xx + x)
    await m.reply_text(text=f"""
🍀 Chats Stats 🍀
🙋♂️ Users : `{xx}`
👥 Groups : `{x}`
🚧 Total users & groups : `{tot}`""")


#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Broadcast ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

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
        except Exception:
            failed += 1

    await lel.edit(
        f"✅ Successfully sent to `{success}` users.\n"
        f"❌ Failed to `{failed}` users.\n"
        f"👾 Found `{blocked}` Blocked users.\n"
        f"👻 Found `{deactivated}` Deactivated users."
    )


#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Broadcast Forward ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.command("fcast") & filters.user(cfg.SUDO))
async def fcast(_, m: Message):
    allusers = users
    lel = await m.reply_text("`⚡️ Processing...`")
    success, failed, deactivated, blocked = 0, 0, 0, 0
    for usrs in allusers.find():
        try:
            userid = usrs["user_id"]
            if m.command[0] == "fcast":
                await m.reply_to_message.forward(int(userid))
            success += 1
        except FloodWait as ex:
            await asyncio.sleep(ex.value)
            if m.command[0] == "fcast":
                await m.reply_to_message.forward(int(userid))
        except errors.InputUserDeactivated:
            deactivated += 1
            remove_user(userid)
        except errors.UserIsBlocked:
            blocked += 1
        except Exception:
            failed += 1

    await lel.edit(
        f"✅ Successfully sent to `{success}` users.\n"
        f"❌ Failed to `{failed}` users.\n"
        f"👾 Found `{blocked}` Blocked users.\n"
        f"👻 Found `{deactivated}` Deactivated users."
    )


print("I'm Alive Now!")
app.run()
