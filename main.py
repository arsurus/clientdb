import psycopg2

# Создание таблиц
def create_db(conn):
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            client_id SERIAL PRIMARY KEY, 
            first_name VARCHAR(60) NOT NULL, 
            last_name VARCHAR(60) NOT NULL, 
            email VARCHAR(60) UNIQUE NOT NULL
            CHECK (email like '%@%.%')
        );
        """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS clients_phones (
            client_id INTEGER NOT NULL REFERENCES clients(client_id), 
            phone VARCHAR(20) UNIQUE
        );
        """)
    conn.commit()
    cur.close()

# Добавление клиента
def add_client(conn, first_name, last_name, email, phone=None):
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO clients (first_name, last_name, email)
        VALUES (%s, %s, %s); """, (first_name, last_name, email))
    conn.commit()
    cur.execute("""
        SELECT client_id FROM clients WHERE email=%s;
        """, (email,))
    cl_id = cur.fetchone()[0]
    if phone != None:
        cur.execute("""
            INSERT INTO clients_phones (client_id, phone)
            VALUES (%s, %s); """, (cl_id, phone))
        conn.commit()
    else:
        cur.close()

# Добавление тел.номера
def add_phone(conn, client_id, phone):
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO clients_phones (client_id, phone)
        VALUES (%s, %s); """, (client_id, phone))
    conn.commit()
    cur.close()

# Изменение данных о клиенте
def change_client(conn, client_id, first_name=None, last_name=None, email=None):
    cur = conn.cursor()
    if first_name != None:
        cur.execute("""
            UPDATE clients SET first_name=%s WHERE client_id=%s;
            """, (first_name, client_id))
        conn.commit()
    if last_name != None:
        cur.execute("""
            UPDATE clients SET last_name=%s WHERE client_id=%s;
            """, (last_name, client_id))
        conn.commit()
    if email != None:
        cur.execute("""
            UPDATE clients SET email=%s WHERE client_id=%s;
            """, (email, client_id))
        conn.commit()
    else:
        cur.close()

# Функция удаления  телефона для существующего клиента
def delete_phone(conn, client_id, phone):
    cur = conn.cursor()
    cur.execute("""
        DELETE FROM clients_phones WHERE client_id=%s AND phone=%s;
        """, (client_id, phone))
    conn.commit()
    cur.close()

# Функция удаления существующего клиента
def delete_client(conn, client_id):
    cur = conn.cursor()
    cur.execute("""
        DELETE FROM clients_phones WHERE client_id=%s;
        """, (client_id,))
    cur.execute("""
        DELETE FROM clients WHERE client_id=%s;
        """, (client_id,))
    conn.commit()
    cur.close()

# Функция поиска клиента по его данным
def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    cur = conn.cursor()
    cur.execute("""
        SELECT * FROM clients as c
        LEFT JOIN clients_phones as cp on c.client_id = cp.client_id 
        WHERE first_name=%s OR last_name=%s OR email=%s OR phone=%s
        """, (first_name, last_name, email, phone))
    print(cur.fetchall())
    cur.close()


# Вызов функций
with psycopg2.connect(database="clientdb", user="postgres", password="postgres") as conn:

    # create_db(conn)
    # add_client(conn, 'Nika', 'Ivanova', 'nivanova@mail.com', '12345678')
    # add_client(conn, 'Vasya', 'Petrov', 'vasya@mail.com', '11223344')
    # add_client(conn, 'Lev', 'Tolstoy', 'leva@mail.com')
    # add_client(conn, 'Petr', 'Velikiy', 'piter@mail.com')
    # add_phone(conn, 1, '87654321')
    # add_phone(conn, 3, '00000000')
    change_client(conn, 4, None, None,'petr@mail.ru')
    #delete_phone(conn, 2, '11223344')
    #delete_client (conn, 3)
    #find_client(conn, None, None, 'nivanova@mail.com' )


