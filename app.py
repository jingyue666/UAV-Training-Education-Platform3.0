import streamlit as st
from modules import auth, profile, admin_panel, training

st.set_page_config(page_title="无人机培训平台", layout="wide")

st.markdown("""
<style>
body {
    font-family: "Microsoft YaHei", sans-serif;
    background-color: #f5f7fa;
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
        "curr_module": None,
        "mod": "基础理论模块",
        "watch_history": []
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

def show_banner():
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 60px 20px; text-align: center; margin: 10px 0; border-radius:12px;">
        <h1 style="margin:0;">无人机职业技能培训平台</h1>
        <p style="font-size:16px; opacity:0.9;">理论+实操+行业应用，一站式无人机技能提升</p>
    </div>
    """, unsafe_allow_html=True)

def main():
    init_session()
    if not st.session_state.username:
        auth.login()
        return

    show_banner()

    menu = ["学习中心", "模拟考试"]
    if st.session_state.role == "学员":
        menu.append("个人中心")
    if st.session_state.role == "管理员":
        menu.append("管理者模式")

    selected = st.selectbox("功能导航", menu)

    if selected == "学习中心":
        training.show()
    elif selected == "模拟考试":
        st.info("模拟考试功能开发中")
    elif selected == "个人中心":
        # 权限拦截：未登录不让进
        if st.session_state.user_id:
            profile.personal_center()
        else:
            st.warning("请先登录")
    elif selected == "管理者模式":
        admin_panel.admin_panel()

if __name__ == "__main__":
    main()
