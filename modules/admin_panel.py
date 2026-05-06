import streamlit as st
import sqlite3
import os

DB_PATH = os.path.join("data", "drone_platform.db")

def admin_panel():
    st.header("管理者后台")
    tabs = st.tabs(["课程管理", "视频管理", "学员管理"])
    with tabs[0]:
        course_manage()
    with tabs[1]:
        video_manage()
    with tabs[2]:
        student_manage()

def course_manage():
    st.subheader("课程管理")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    with st.form("add_course"):
        title = st.text_input("课程名称")
        level = st.selectbox("难度", ["初级", "中级", "高级"])
        price = st.number_input("价格", 0.0)
        if st.form_submit_button("新增"):
            c.execute("INSERT INTO courses (title, level, price) VALUES (?,?,?)",
                      (title, level, price))
            conn.commit()
            st.success("添加成功")
    st.dataframe(conn.execute("SELECT * FROM courses").fetchall(), use_container_width=True)
    conn.close()

def video_manage():
    st.subheader("视频管理")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    with st.expander("新增视频"):
        with st.form("add_video"):
            title = st.text_input("视频标题")
            category = st.selectbox("所属模块", [
                "基础理论模块",
                "实操技能模块",
                "行业应用模块",
                "商业运营模块"
            ])
            level = st.selectbox("难度", ["初级","中级","高级"])
            url = st.text_input("视频链接")
            cover = st.text_input("封面链接")
            if st.form_submit_button("发布"):
                c.execute("INSERT INTO videos (title, category, level, url, cover) VALUES (?,?,?,?,?)",
                          (title, category, level, url, cover))
                conn.commit()
                st.success("发布成功")
    videos = c.execute("SELECT id, title, category, level FROM videos ORDER BY created_at DESC").fetchall()
    for vid, title, cat, lv in videos:
        col1, col2, col3 = st.columns([3,1,1])
        with col1: st.write(f"【{cat}】{title}")
        with col2: st.write(lv)
        with col3:
            if st.button("删除", key=f"del_{vid}"):
                c.execute("DELETE FROM videos WHERE id=?", (vid,))
                conn.commit()
                st.experimental_rerun()
    conn.close()

def student_manage():
    st.subheader("学员管理")
    conn = sqlite3.connect(DB_PATH)
    st.dataframe(conn.execute("SELECT id, real_name, phone, level FROM users WHERE role='学员'").fetchall(), use_container_width=True)
    conn.close()
