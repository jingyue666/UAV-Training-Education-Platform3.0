import streamlit as st
import os
from modules import auth, profile, admin_panel, training

st.set_page_config(page_title="无人机培训平台", layout="wide")

# 全局样式：智慧树风格
st.markdown("""
<style>
/* 全局重置 */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}
body {
    font-family: "Microsoft YaHei", sans-serif;
    background-color: #f5f7fa;
}
/* 顶部导航栏 */
.top-nav {
    background-color: #ffffff;
    border-bottom: 1px solid #e8e8e8;
    padding: 10px 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.logo {
    font-size: 20px;
    font-weight: bold;
    color: #1890ff;
}
.nav-links a {
    margin: 0 15px;
    color: #333;
    text-decoration: none;
    font-size: 15px;
}
.nav-links a:hover {
    color: #1890ff;
}
/* 横幅轮播 */
.banner {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 60px 20px;
    text-align: center;
    border-radius: 0;
}
.banner h1 {
    font-size: 36px;
    margin-bottom: 10px;
}
.banner p {
    font-size: 18px;
    opacity: 0.9;
}
/* 分类标签 */
.category-tag {
    display: inline-block;
    padding: 6px 16px;
    margin: 0 8px 10px 0;
    border-radius: 20px;
    background-color: #e6f7ff;
    color: #1890ff;
    border: 1px solid #91d5ff;
    cursor: pointer;
}
.category-tag.active {
    background-color: #1890ff;
    color: white;
}
/* 课程卡片 */
.course-card {
    background-color: white;
    border-radius: 12px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.08);
    overflow: hidden;
    margin-bottom: 20px;
}
.course-card img {
    width: 100%;
    height: 150px;
    object-fit: cover;
}
.course-info {
    padding: 15px;
}
.course-title {
    font-size: 16px;
    font-weight: bold;
    margin-bottom: 8px;
}
.course-meta {
    font-size: 13px;
    color: #666;
    margin-bottom: 10px;
}
.course-btn {
    width: 100%;
    background-color: #1890ff;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 8px 0;
    cursor: pointer;
}
/* 侧边栏隐藏 */
.css-18ni7ap.ezrtsby2 {
    display: none;
}
</style>
""", unsafe_allow_html=True)

def init_session():
    defaults = {
        "user_id": None,
        "username": None,
        "role": None,
        "level": None,
        "video_url": None,
        "curr_module": None
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

def show_top_nav():
    st.markdown("""
    <div class="top-nav">
        <div class="logo">无人机培训平台</div>
        <div class="nav-links">
            <a href="#">首页</a>
            <a href="#">课程中心</a>
            <a href="#">个人中心</a>
            <a href="#">帮助中心</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_banner():
    st.markdown("""
    <div class="banner">
        <h1>无人机职业技能培训平台</h1>
        <p>理论+实操+行业应用，一站式无人机技能提升</p>
    </div>
    """, unsafe_allow_html=True)

def main():
    init_session()
    if not st.session_state.username:
        auth.login()
        return

    show_top_nav()
    show_banner()

    # 顶部功能标签栏
    st.markdown("<div style='padding: 20px 20px 0;'>", unsafe_allow_html=True)
    tabs = st.columns(4)
    with tabs[0]:
        if st.button("学习中心", key="tab1"):
            st.session_state.curr_tab = "学习中心"
    with tabs[1]:
        if st.button("模拟考试", key="tab2"):
            st.session_state.curr_tab = "模拟考试"
    with tabs[2]:
        if st.button("个人中心", key="tab3"):
            st.session_state.curr_tab = "个人中心"
    with tabs[3]:
        if st.button("管理者模式", key="tab4"):
            st.session_state.curr_tab = "管理者模式"
    st.markdown("</div>", unsafe_allow_html=True)

    # 默认进入学习中心
    if "curr_tab" not in st.session_state:
        st.session_state.curr_tab = "学习中心"

    if st.session_state.curr_tab == "学习中心":
        training.show()
    elif st.session_state.curr_tab == "模拟考试":
        st.info("模拟考试功能开发中")
    elif st.session_state.curr_tab == "个人中心":
        profile.personal_center()
    elif st.session_state.curr_tab == "管理者模式":
        admin_panel.admin_panel()

if __name__ == "__main__":
    main()