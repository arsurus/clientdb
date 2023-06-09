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
        cur.execute(""" 
            SELECT client_id from clients WHERE client_id=%s;
            """, (client_id,))
        fnd = cur.fetchone()
        if fnd:
            if first_name != None:
                cur.execute("""
                    UPDATE clients SET first_name=%s WHERE client_id=%s;
                    """, (first_name, client_id))
                conn.commit()
                return "Изменения приняты"
            if last_name != None:
                cur.execute("""
                    UPDATE clients SET last_name=%s WHERE client_id=%s;
                    """, (last_name, client_id))
                conn.commit()
                return "Изменения приняты"
            if email != None:
                cur.execute("""
                    UPDATE clients SET email=%s WHERE client_id=%s;
                    """, (email, client_id))
                conn.commit()
                return "Изменения приняты"
        return "Клиент ID не найден"

# Функция удаления  телефона для существующего клиента
def delete_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute(""" 
             SELECT client_id from clients WHERE client_id=%s;
             """, (client_id,))
        fnd = cur.fetchone()
        print(fnd)
        if fnd:
            cur.execute(""" 
                SELECT client_id from clients_phones WHERE phone=%s;
                """, (phone,))
            fnd2 = cur.fetchone()
            print(fnd2)
            if (fnd2 == fnd) and (find_client(conn, None, None, None, phone=phone) == 'Клиент найден'):
                cur.execute(""" 
                    DELETE FROM clients_phones WHERE client_id=%s AND phone=%s;
                    """, (client_id, phone))
                conn.commit()
                return "Тел номер удален"
            return "Телефонный номер не найден или имеется несоответствие"
        return "Клиент ID не найден"

# Функция удаления существующего клиента
def delete_client(conn, client_id):
    with conn.cursor() as cur:
        cur.execute(""" 
              SELECT client_id from clients WHERE client_id=%s;
              """, (client_id,))
        fnd = cur.fetchone()
        print(fnd)
        if fnd:
            cur.execute("""
                DELETE FROM clients WHERE client_id=%s;
                """, (client_id,))
            conn.commit()
            return "Клиент удален"
        return "Кдиент ID не найден"

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

   #create_db(conn)
   # print(add_client(conn, '32eASD', None, 'asbce@abc.ru', '9s000e2276w6354'))

    #print (add_client(conn, '12822Vasya', '1222Petrov', '122vasy2a@mail.com', ))
     #add_client(conn, 'Lev', 'Tolstoy', 'leva@mail.com')
    # add_client(conn, 'Petr', 'Velikiy', 'piter@mail.com')
    #print(add_phone(conn, 32, '87665343321'))
    #print (add_phone(conn, 2, '000124340000'))
    #print (change_client(conn, 2, None, None,'p8e1tr@mail.ru'))
    #print(delete_phone(conn, 500, '90002276w6354'))
    print(delete_client (conn, 99))
    #print (find_client(conn, 'Lev', None,))


