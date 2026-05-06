import streamlit as st
import sqlite3
import os

DB_PATH = os.path.join("data", "drone_platform.db")

def login():
    st.title("用户登录")
    username = st.text_input("用户名")
    password = st.text_input("密码", type="password")

    if st.button("登录", use_container_width=True):
        try:
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("SELECT id, role, level FROM users WHERE username=? AND password=?",
                      (username, password))
            row = c.fetchone()
            conn.close()

            if row:
                st.session_state.user_id = row[0]
                st.session_state.username = username
                st.session_state.role = row[1]
                st.session_state.level = row[2]
                st.experimental_rerun()
            else:
                st.error("用户名或密码错误")
        except Exception as e:
            st.error("数据库连接失败")
