import psycopg2

# Создание таблиц
def create_db(conn):
    with conn.cursor() as cur:
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
                client_id INTEGER NOT NULL REFERENCES clients(client_id) ON DELETE CASCADE, 
                phone VARCHAR(20) UNIQUE
            );
            """)
        conn.commit()


# Добавление клиента
def add_client(conn, first_name, last_name, email, phone=None):
    with conn.cursor() as cur:
        if find_client(conn, email=email) == 'Клиент найден':
            result = "Клиент с указанным email уже существует"
            return result
        cur.execute("""
            INSERT INTO clients (first_name, last_name, email)
            VALUES (%s, %s, %s) RETURNING client_id; """, (first_name, last_name, email))
        if phone != None:
            cl_id = cur.fetchone()
            res = add_phone(conn, cl_id, phone)
            if res != 'Телефон добавлен':
                conn.rollback()
                result = 'Добавить данного клиента невозможно'
                return result
            conn.commit()
            result = 'Клиент добавлен'
            return result



# Добавление тел.номера
def add_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        if find_client(conn, None, None, None, phone=phone) == "Клиент найден":
            return "Номер существует"
        cur.execute("""
            SELECT last_name FROM clients
            WHERE client_id=%s ;
            """, (client_id,)
        )
        if not cur.fetchone():
            result = "Такого клиента не существует"
            return result
        cur.execute ("""
            INSERT INTO clients_phones (client_id, phone)
            VALUES (%s, %s); """, (client_id, phone))
        conn.commit()
        result = 'Телефон добавлен'
    return result

# Изменение данных о клиенте
def change_client(conn, client_id, first_name=None, last_name=None, email=None):
    with conn.cursor() as cur:
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



# Функция удаления  телефона для существующего клиента
def delete_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute("""
            DELETE FROM clients_phones WHERE client_id=%s AND phone=%s;
            """, (client_id, phone))
        conn.commit()


# Функция удаления существующего клиента
def delete_client(conn, client_id):
    with conn.cursor() as cur:
        cur.execute("""
            DELETE FROM clients WHERE client_id=%s;
            """, (client_id,))
        conn.commit()

# Функция поиска клиента по его данным
def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT * FROM clients as c
            LEFT JOIN clients_phones as cp on c.client_id = cp.client_id 
            WHERE first_name=%s OR last_name=%s OR email=%s OR phone=%s
            """, (first_name, last_name, email, phone))
        a = cur.fetchall()
        print(a)
        if a == []:
            result = "Клиент не найден"
            return result
        else:
            result = "Клиент найден"
            return result

# Вызов функций
with psycopg2.connect(database="clientdb", user="postgres", password="postgres") as conn:

    # create_db(conn)
    #add_client(conn, '3eASD', '23wSD', '2AS3Dq@mail.com', '900076w6354')
    print (add_client(conn, '12822Vasya', '1222Petrov', '122vasy2a@mail.com', ))
    # add_client(conn, 'Lev', 'Tolstoy', 'leva@mail.com')
    # add_client(conn, 'Petr', 'Velikiy', 'piter@mail.com')
    #add_phone(conn, 2, '8766543321')
    #print (add_phone(conn, 7, '000124340000'))
    #change_client(conn, 4, None, None,'petr@mail.ru')
    #delete_phone(conn, 2, '11223344')
    #delete_client (conn, 1)
    #find_client(conn, None , None, 'leva@mail.com')


