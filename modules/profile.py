import streamlit as st
import sqlite3
import os

DB_PATH = os.path.join("data", "drone_platform.db")

def personal_center():
    st.markdown("""
    <div style="background-color:#ffffff; padding:20px; border-radius:12px; box-shadow:0 2px 10px rgba(0,0,0,0.08); margin-bottom:20px;">
        <h2 style="margin:0; color:#2c3e50;">👤 个人中心</h2>
        <p style="color:#7f8c8d;">查看个人信息、修改密码、浏览历史</p>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📋 基本信息", "🔐 修改密码", "📺 浏览历史"])

    with tab1:
        show_basic_info()
    with tab2:
        change_password()
    with tab3:
        show_history()

def show_basic_info():
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT username, real_name, phone, role, level FROM users WHERE id=?", (st.session_state.user_id,))
        row = c.fetchone()
        conn.close()

        if row:
            st.markdown(f"""
            <div style="display:grid; gap:10px;">
                <div style="background:#f8f9fa; padding:12px; border-radius:8px;">
                    <b>用户名</b><br>{row[0]}
                </div>
                <div style="background:#f8f9fa; padding:12px; border-radius:8px;">
                    <b>姓名</b><br>{row[1] if row[1] else '未填写'}
                </div>
                <div style="background:#f8f9fa; padding:12px; border-radius:8px;">
                    <b>电话</b><br>{row[2] if row[2] else '未填写'}
                </div>
                <div style="background:#f8f9fa; padding:12px; border-radius:8px;">
                    <b>身份</b><br>{row[3]}
                </div>
                <div style="background:#f8f9fa; padding:12px; border-radius:8px;">
                    <b>等级</b><br>{row[4]}
                </div>
            </div>
            """, unsafe_allow_html=True)
    except:
        st.error("获取信息失败")

def change_password():
    st.subheader("修改密码")
    with st.form("pwd_form"):
        old = st.text_input("原密码", type="password")
        new = st.text_input("新密码", type="password")
        confirm = st.text_input("确认新密码", type="password")
        submit = st.form_submit_button("确认修改", use_container_width=True)

    if submit:
        if new != confirm:
            st.error("两次密码不一致")
            return
        try:
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("SELECT password FROM users WHERE id=?", (st.session_state.user_id,))
            row = c.fetchone()
            if not row or row[0] != old:
                st.error("原密码错误")
            else:
                c.execute("UPDATE users SET password=? WHERE id=?", (new, st.session_state.user_id))
                conn.commit()
                st.success("✅ 密码修改成功")
            conn.close()
        except:
            st.error("修改失败")

def show_history():
    st.subheader("最近观看的课程")
    if "watch_history" not in st.session_state or len(st.session_state.watch_history) == 0:
        st.info("暂无浏览历史")
        return

    for item in reversed(st.session_state.watch_history):
        st.markdown(f"""
        <div style="background:#fff; padding:14px; border-radius:10px; box-shadow:0 1px 5px rgba(0,0,0,0.05); margin-bottom:10px;">
            <b>{item['title']}</b><br>
            <small style="color:#777;">模块：{item['module']}</small>
        </div>
        """, unsafe_allow_html=True)

# 记录观看历史（去重+限制10条）
def add_watch_history(title, module_name):
    if "watch_history" not in st.session_state:
        st.session_state.watch_history = []

    # 去重：已有就不重复加
    for item in st.session_state.watch_history:
        if item["title"] == title:
            return

    st.session_state.watch_history.append({
        "title": title,
        "module": module_name
    })

    # 只保留最近10条
    if len(st.session_state.watch_history) > 10:
        st.session_state.watch_history.pop(0)
