import streamlit as st
import sqlite3
import os

DB_PATH = os.path.join("data", "drone_platform.db")

MODULES = [
    {"name": "基础理论模块"},
    {"name": "实操技能模块"},
    {"name": "行业应用模块"},
    {"name": "商业运营模块"},
]

def show():
    # 模块按钮
    cols = st.columns(4)
    for i, m in enumerate(MODULES):
        with cols[i]:
            if st.button(m["name"], key=f"m{i}", use_container_width=True):
                st.session_state.mod = m["name"]

    # 默认模块
    if "mod" not in st.session_state:
        st.session_state.mod = "基础理论模块"

    current = st.session_state.mod
    st.subheader(current)
    st.divider()

    # 加载视频
    try:
        con = sqlite3.connect(DB_PATH)
        videos = con.execute("SELECT title, cover, url, level FROM videos WHERE category=?", (current,)).fetchall()
        con.close()

        if not videos:
            st.info("暂无视频")
            return

        # 3列卡片 + 封面图
        cols = st.columns(3)
        for i, (title, cover, url, level) in enumerate(videos):
            with cols[i % 3]:
                # 显示封面（没有就显示默认图）
                if cover and cover.strip() != "":
                    st.image(cover, use_column_width=True)
                else:
                    st.image("https://picsum.photos/seed/"+str(i)+"/400/225", use_column_width=True)
                
                st.markdown(f"**{title}**")
                st.caption(f"难度：{level}")
                if st.button("播放", key=f"p{i}", use_container_width=True):
                    st.session_state.vurl = url

        # 播放区
        if "vurl" in st.session_state and st.session_state.vurl:
            st.divider()
            st.video(st.session_state.vurl)

    except Exception as e:
        st.error(f"加载失败：{e}")