"""
M&A 并购重组项目信息交流平台
MNA Platform - Streamlit MVP

入口文件
"""
import streamlit as st
from modules.auth import render_login_register, logout
from modules.data_manager import load_projects

# ======================
# 页面配置
# ======================
st.set_page_config(
    page_title="M&A 并购重组平台",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ======================
# 初始化
# ======================
def init_session():
    """初始化会话状态"""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "user" not in st.session_state:
        st.session_state.user = None
    if "user_info" not in st.session_state:
        st.session_state.user_info = None

init_session()

# ======================
# 首页渲染
# ======================
def render_home():
    """渲染首页"""

    # Hero Section
    st.markdown("""
    <style>
        .hero {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            padding: 60px 40px;
            border-radius: 16px;
            margin-bottom: 40px;
            text-align: center;
        }
        .hero h1 {
            color: #ffffff;
            font-size: 2.5rem;
            margin-bottom: 16px;
        }
        .hero p {
            color: #a0a0a0;
            font-size: 1.1rem;
        }
    </style>
    <div class="hero">
        <h1>M&A 并购重组项目信息交流平台</h1>
        <p>汇聚优质并购项目 / 连接资本与机会 / 专注卖方顾问服务</p>
    </div>
    """, unsafe_allow_html=True)

    # 平台优势
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### 🔒 安全合规")
        st.caption("端到端加密 / 严格访问控制 / NDA/NCA 协议保护")
    with col2:
        st.markdown("### 📊 精选项目")
        st.caption("严格筛选 / 真实尽职调查 / 完善信息披露")
    with col3:
        st.markdown("### 🤝 专业对接")
        st.caption("一对一服务 / 精准匹配 / 全流程跟踪")

    st.divider()

    # 项目统计
    projects = load_projects()
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("在售项目", len(projects))
    with col2:
        st.metric("行业覆盖", "电子器件/新能源/制造")
    with col3:
        st.metric("成功案例", "20+")
    with col4:
        st.metric("注册用户", "200+")


def main():
    """主函数"""

    # 未登录：显示登录/注册
    if not st.session_state.authenticated:
        render_login_register()
        st.divider()
        render_home()
        return

    # 已登录：渲染页面导航
    st.sidebar.success(f"✅ 已登录：{st.session_state.user_info.get('name', st.session_state.user)}")

    # 登出按钮
    if st.sidebar.button("退出登录", use_container_width=True):
        logout()

    st.sidebar.divider()
    st.sidebar.markdown("### 快速导航")

    # 页面选择
    pages = {
        "I. 项目列表": "projects_list",
        "II. 搜索中心": "search",
        "III. 用户中心": "user_center",
    }

    # 管理员额外入口
    if st.session_state.user_info.get("role") == "admin":
        st.sidebar.divider()
        st.sidebar.markdown("### 管理后台")
        if st.sidebar.button("发布项目", use_container_width=True):
            st.switch_page("pages/admin_center.py")

    selection = st.sidebar.radio("跳转页面", list(pages.keys()))

    # 渲染对应页面
    if selection == "I. 项目列表":
        from pages.projects_list import render
        render()
    elif selection == "II. 搜索中心":
        from pages.search import render
        render()
    elif selection == "III. 用户中心":
        from pages.user_center import render
        render()


if __name__ == "__main__":
    main()
