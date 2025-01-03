import aiosqlite



#Записываем данные
async def add_database(number, photo):
    async with aiosqlite.connect('tg_base.db') as db:
        await db.execute('CREATE TABLE IF NOT EXISTS users (number TEXT, photo TEXT) ')
        await db.execute('INSERT INTO users (number, photo) VALUES(?, ?)', (number,photo))
        await db.commit()

#поиск данных по столбцу number через FSM
async def get_photo_bynumber(number):
    async with aiosqlite.connect('tg_base.db') as db:
        async with db.execute(f'SELECT photo FROM users WHERE number = "{number}" ') as cursor:
            rows = await cursor.fetchall()
            list_id = []
            
            for i in rows:
                list_id.append(i)
            return list_id


