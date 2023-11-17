import sqlite3 as sq
# from create_bot import dp
from keyboards.client_kb import order_kb


def sql_start():
    global base, cur
    base = sq.connect("Notifications.db")
    cur = base.cursor()
    if base:
        print("Db connected")
    base.execute('CREATE TABLE IF NOT EXISTS {}(user_tg TEXT PRIMARY KEY, user_sm TEXT,'
                 'subs INTEGER, Anilib INTEGER, Anivost INTEGER)'.format('notif'))
    base.commit()


async def sql_add_command(state):
    async with state.proxy() as data:
        # print(data['user_tg'])
        # exists = cur.execute("SELECT 1 FROM notif WHERE user_tg = ?", [data['user_tg']]).fetchone()
        # # print(exists)
        # if exists:
        #     cur.execute('UPDATE notif SET user_sm == ? WHERE user_tg = ?', (data['user_sm'], data['user_tg']))
        #     base.commit()
        #     cur.execute('UPDATE notif SET subs == ? WHERE user_tg = ?', (data['subs'], data['user_tg']))
        #     base.commit()
        #     cur.execute('UPDATE notif SET Anilib == ? WHERE user_tg = ?', (data['Anilib'], data['user_tg']))
        #     base.commit()
        #     cur.execute('UPDATE notif SET Anivost == ? WHERE user_tg = ?', (data['Anivost'], data['user_tg']))
        #     base.commit()
        # else:
        cur.execute('INSERT INTO notif VALUES (?, ?, ?, ?, ?)', tuple(data.values()))
        base.commit()


async def sql_check_user(state):
    async with state.proxy() as data:
        exists = cur.execute("SELECT 1 FROM notif WHERE user_tg = ?", [data['user_tg']]).fetchone()
        return 1 if exists else 0


async def sql_check_sub(id):
    exists = cur.execute("SELECT subs FROM notif WHERE user_tg = ?", [id]).fetchone()
    return 1 if exists else 0


async def sql_check_al(id):
    exists = cur.execute("SELECT Anilib FROM notif WHERE user_tg = ?", [id]).fetchone()
    return exists


async def sql_check_av(id):
    print(id)
    exists = cur.execute("SELECT Anivost FROM notif WHERE user_tg = ?", [id]).fetchone()
    print(exists)
    return exists


async def sql_update_command(state):
    async with state.proxy() as data:
        cur.execute('UPDATE notif SET user_sm == ? WHERE user_tg = ?', (data['user_sm'], data['user_tg']))
        base.commit()
        cur.execute('UPDATE notif SET subs == ? WHERE user_tg = ?', (data['subs'], data['user_tg']))
        base.commit()
        cur.execute('UPDATE notif SET Anilib == ? WHERE user_tg = ?', (data['Anilib'], data['user_tg']))
        base.commit()
        cur.execute('UPDATE notif SET Anivost == ? WHERE user_tg = ?', (data['Anivost'], data['user_tg']))
        base.commit()


async def sql_update_subs(id):
    cur.execute('UPDATE notif SET subs == ? WHERE user_tg == ?', ((int(await sql_check_sub(id)) + 1) % 2, id))
    base.commit()


async def sql_update_al(id):
    cur.execute('UPDATE notif SET Anilib == ? WHERE user_tg == ?', ((int(await sql_check_al(id)) + 1) % 2, id))
    base.commit()


async def sql_update_av(id):
    cur.execute('UPDATE notif SET Anivost == ? WHERE user_tg == ?', ((int(await sql_check_av(id)) + 1) % 2, id))
    base.commit()

# async def sql_read(message):
#     for ret in cur.execute("SELECT * FROM menu").fetchall():
#         await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\nОписание {ret[2]}\nЦена {ret[-1]}',
#                              reply_markup=order_kb)
