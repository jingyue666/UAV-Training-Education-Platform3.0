import streamlit as st
import sqlite3
import os
from modules.profile import add_watch_history

DB_PATH = os.path.join("data", "drone_platform.db")

DEFAULT_COVERS = {
    "基础理论模块": "https://images.unsplash.com/photo-1473968512647-3e447244af8f?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
    "实操技能模块": "https://images.unsplash.com/photo-1527977966376-1c8408f9f108?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
    "行业应用模块": "https://images.unsplash.com/photo-1531259683007-009259d1812d?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
    "商业运营模块": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"
}

MODULES = list(DEFAULT_COVERS.keys())

def show():
    cols = st.columns(4)
    for i, name in enumerate(MODULES):
        with cols[i]:
            if st.button(name, key=f"mod_btn_{i}", use_container_width=True):
                st.session_state.mod = name

    if "mod" not in st.session_state:
        st.session_state.mod = MODULES[0]

    current = st.session_state.mod
    st.subheader(current)
    st.divider()

    try:
        con = sqlite3.connect(DB_PATH)
        videos = con.execute("SELECT title, cover, url, level FROM videos WHERE category=?", (current,)).fetchall()
        con.close()

        if not videos:
            st.info("暂无视频")
            return

        cols = st.columns(3)
        for i, (title, cover, url, level) in enumerate(videos):
            with cols[i % 3]:
                if cover and cover.strip() != "":
                    st.image(cover, use_column_width=True)
                else:
                    st.image(DEFAULT_COVERS[current], use_column_width=True)

                st.markdown(f"**{title}**")
                st.caption(f"难度：{level}")
                if st.button("播放", key=f"p{i}", use_container_width=True):
                    st.session_state.vurl = url
                    add_watch_history(title, current)

        if "vurl" in st.session_state and st.session_state.vurl:
            st.divider()
            st.video(st.session_state.vurl)

    except Exception as e:
        st.error(f"加载失败：{e}")
