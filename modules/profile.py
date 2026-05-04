import streamlit as st
import sqlite3
import os

DB_PATH = os.path.join("data", "drone_platform.db")

def personal_center():
    st.title("个人中心")
    tab1, tab2 = st.tabs(["基本信息", "修改密码"])

    with tab1:
        try:
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("SELECT username, real_name, phone, role, level FROM users WHERE id=?", (st.session_state.user_id,))
            info = c.fetchone()
            conn.close()

            if info:
                st.write(f"**用户名**: {info[0]}")
                st.write(f"**姓名**: {info[1]}")
                st.write(f"**电话**: {info[2]}")
                st.write(f"**身份**: {info[3]}")
                st.write(f"**等级**: {info[4]}")
        except:
            st.error("获取信息失败")

    with tab2:
        old_pwd = st.text_input("原密码", type="password")
        new_pwd = st.text_input("新密码", type="password")
        confirm_pwd = st.text_input("确认新密码", type="password")
        if st.button("确认修改"):
            if new_pwd != confirm_pwd:
                st.error("两次密码不一致")
                return
            try:
                conn = sqlite3.connect(DB_PATH)
                c = conn.cursor()
                c.execute("SELECT password FROM users WHERE id=?", (st.session_state.user_id,))
                row = c.fetchone()
                if row[0] != old_pwd:
                    st.error("原密码错误")
                else:
                    c.execute("UPDATE users SET password=? WHERE id=?", (new_pwd, st.session_state.user_id))
                    conn.commit()
                    st.success("修改成功！")
                conn.close()
            except:
                st.error("修改失败")