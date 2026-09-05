import streamlit as st
import sqlite3
import os

DB_PATH = os.path.join("data", "drone_platform.db")

def login():
    st.title("用户登录")
    
    # 登录/注册 切换
    tab1, tab2 = st.tabs(["登录", "注册"])
    
    with tab1:
        _login_form()
    
    with tab2:
        _register_form()

def _login_form():
    username = st.text_input("用户名", key="login_user")
    password = st.text_input("密码", type="password", key="login_pwd")

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
            st.error(f"登录失败：{e}")

def _register_form():
    st.subheader("新用户注册")
    
    with st.form("register_form"):
        username = st.text_input("用户名 *", placeholder="用于登录的唯一标识")
        real_name = st.text_input("姓名", placeholder="真实姓名（选填）")
        phone = st.text_input("电话", placeholder="手机号（选填）")
        password = st.text_input("密码 *", type="password")
        confirm_password = st.text_input("确认密码 *", type="password")
        
        submit = st.form_submit_button("注册", use_container_width=True)
    
    if submit:
        # 校验
        if not username or not password:
            st.error("用户名和密码不能为空")
            return
        
        if password != confirm_password:
            st.error("两次密码不一致")
            return
        
        if len(password) < 6:
            st.error("密码长度至少6位")
            return
        
        try:
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            
            # 检查用户名是否已存在
            c.execute("SELECT id FROM users WHERE username=?", (username,))
            if c.fetchone():
                st.error("该用户名已被注册")
                conn.close()
                return
            
            # 插入新用户，默认角色=学员，等级=初级
            c.execute(
                "INSERT INTO users (username, password, real_name, phone, role, level, status) VALUES (?,?,?,?,?,?,?)",
                (username, password, real_name, phone, "学员", "初级", "正常")
            )
            conn.commit()
            conn.close()
            
            st.success("✅ 注册成功！请切换到登录页登录")
            
        except Exception as e:
            st.error(f"注册失败：{e}")
