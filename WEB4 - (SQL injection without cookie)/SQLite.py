import sqlite3
# 这里是创建一个新的table
# 建立连接，连接到一个 sqlite 数据库(如果没有连接，就创建)
conn = sqlite3.connect("database.db")

# 建立 cursor
cur = conn.cursor()

# Build one table to store the products name
#cur.execute("DROP TABLE IF EXISTS products")

with conn:
    cur.execute("""CREATE TABLE IF NOT EXISTS products (
    key INTEGER PRIMARY KEY,
    name TEXT 
    )""")

    # 插入
    cur.execute(f"""INSERT INTO products (name) VALUES(? )""", ("P1",))
    cur.execute(f"""INSERT INTO products (name)VALUES(? )""", ("P2",))
    cur.execute(f"""INSERT INTO products (name)VALUES(? )""", ("P3",))
    cur.execute(f"""INSERT INTO products (name)VALUES(? )""", ("P4",))
    cur.execute(f"""INSERT INTO products (name)VALUES(? )""", ("P5",))
    cur.execute(f"""INSERT INTO products (name)VALUES(? )""", ("P6",))
    cur.execute(f"""INSERT INTO products (name)VALUES(? )""", ("P7",))
    cur.execute(f"""INSERT INTO products (name)VALUES(? )""", ("P8",))
    cur.execute(f"""INSERT INTO products (name)VALUES(? )""", ("P9",))
    cur.execute(f"""INSERT INTO products (name)VALUES(? )""", ("P10",))


# build one table to store the search history
with conn:
    cur.execute("""CREATE TABLE IF NOT EXISTS searches (
    user_id INTEGER,
    product_name TEXT,
    searches INTEGER
    )""")


    #cur.execute("DROP TABLE IF EXISTS current_id")


with conn:


    cur.execute("""CREATE TABLE IF NOT EXISTS current_id (
    table_id INTEGER PRIMARY KEY,
    user_id INTEGER
    )""")

    #cur.execute(f"""INSERT INTO current_id (user_id) VALUES(? )""", (0,))




# 关闭数据库连接
conn.close()


