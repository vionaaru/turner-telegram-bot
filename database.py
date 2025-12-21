# Author: Sergey Akulov
# GitHub: https://github.com/serg-akulov

import pymysql
import config

def get_connection():
    return pymysql.connect(
        host=config.DB_HOST, user=config.DB_USER, password=config.DB_PASS,
        database=config.DB_NAME, cursorclass=pymysql.cursors.DictCursor, autocommit=True
    )

def get_bot_config():
    conn = get_connection()
    cfg = {}
    with conn.cursor() as cursor:
        cursor.execute("SELECT key_name, value_text FROM settings")
        for row in cursor.fetchall(): cfg[row['key_name']] = row['value_text']
        cursor.execute("SELECT cfg_key, cfg_value FROM bot_config")
        for row in cursor.fetchall(): cfg[row['cfg_key']] = row['cfg_value']
    conn.close()
    return cfg

def update_setting(key, val):
    conn = get_connection()
    with conn.cursor() as cur: cur.execute("UPDATE settings SET value_text=%s WHERE key_name=%s", (val, key))
    conn.close()

def create_order(user_id, username, full_name):
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("INSERT INTO orders (user_id, username, full_name, status) VALUES (%s, %s, %s, 'filling')", (user_id, username, full_name))
        oid = cur.lastrowid
    conn.close()
    return oid

def update_order_field(oid, field, val):
    conn = get_connection()
    with conn.cursor() as cur: cur.execute(f"UPDATE orders SET {field}=%s WHERE id=%s", (val, oid))
    conn.close()

def finish_order_creation(oid):
    conn = get_connection()
    with conn.cursor() as cur: cur.execute("UPDATE orders SET status='new' WHERE id=%s", (oid,))
    conn.close()

def get_order(oid):
    conn = get_connection()
    with conn.cursor() as cur: 
        cur.execute("SELECT * FROM orders WHERE id=%s", (oid,))
        res = cur.fetchone()
    conn.close()
    return res

def get_active_order_id(user_id):
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT id FROM orders WHERE user_id=%s AND status='filling' ORDER BY id DESC LIMIT 1", (user_id,))
        res = cur.fetchone()
    conn.close()
    return res['id'] if res else None

def get_user_last_active_order(user_id):
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT id FROM orders WHERE user_id=%s AND status IN ('new','discussion','approved','work') ORDER BY id DESC LIMIT 1", (user_id,))
        res = cur.fetchone()
    conn.close()
    return res['id'] if res else None

# --- ИСПРАВЛЕННАЯ ФУНКЦИЯ ---
def cancel_old_filling_orders(user_id):
    """Помечает все старые черновики как rejected (отменен/отказ)"""
    conn = get_connection()
    with conn.cursor() as cur:
        # БЫЛО: status='canceled' (Ошибка!)
        # СТАЛО: status='rejected' (Правильно!)
        cur.execute("UPDATE orders SET status='rejected' WHERE user_id=%s AND status='filling'", (user_id,))
    conn.close()