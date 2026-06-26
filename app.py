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
# 自定义商务冷色 CSS
# ======================
st.markdown("""
<style>
    /* 整体背景 */
    .stApp { background-color: #f8fafc; }

    /* 主色调 */
    :root {
        --primary: #1e3a5f;
        --primary-light: #2d5a87;
        --secondary: #0d7377;
        --accent: #14919b;
        --bg-dark: #0f2439;
        --text-dark: #1e293b;
        --text-gray: #64748b;
        --border: #cbd5e1;
        --card-bg: #ffffff;
    }

    /* Hero 区域 */
    .hero {
        background: linear-gradient(135deg, #0f2439 0%, #1e3a5f 50%, #2d5a87 100%);
        padding: 60px 40px;
        border-radius: 12px;
        margin-bottom: 40px;
        text-align: center;
        box-shadow: 0 10px 40px rgba(15, 36, 57, 0.15);
    }
    .hero h1 {
        color: #ffffff;
        font-size: 2.2rem;
        font-weight: 600;
        margin-bottom: 16px;
        letter-spacing: -0.5px;
    }
    .hero p {
        color: #94a3b8;
        font-size: 1.1rem;
        letter-spacing: 0.5px;
    }

    /* 卡片样式 */
    .metric-card {
        background: #ffffff;
        padding: 24px;
        border-radius: 10px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 2px 8px rgba(15, 36, 57, 0.06);
    }

    /* 侧边栏 */
    .stSidebar {
        background-color: #ffffff !important;
    }
    .stSidebar > div {
        background-color: #ffffff;
    }

    /* 按钮 */
    .stButton > button {
        background-color: #1e3a5f;
        color: white;
        border: none;
        border-radius: 6px;
    }
    .stButton > button:hover {
        background-color: #2d5a87;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #f1f5f9;
        border-radius: 6px 6px 0 0;
        padding: 8px 16px;
    }
    .stTabs .stTabs[aria-selected="true"] {
        background-color: #1e3a5f !important;
        color: white !important;
    }

    /* 成功/信息提示 */
    .stSuccess { background-color: #ecfdf5; border-left: 4px solid #0d7377; }
    .stInfo { background-color: #f0f9ff; border-left: 4px solid #14919b; }
    .stWarning { background-color: #fef3c7; border-left: 4px solid #d97706; }
    .stError { background-color: #fef2f2; border-left: 4px solid #dc2626; }

    /* 滚动条 */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #f1f5f9; }
    ::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

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
    <div class="hero">
        <h1>🏢 M&A 并购重组项目信息交流平台</h1>
        <p>汇聚优质并购项目 / 连接资本与机会 / 专注卖方顾问服务</p>
    </div>
    """, unsafe_allow_html=True)

    # 平台优势
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #1e3a5f; margin-bottom: 8px;">🔒 安全合规</h3>
            <p style="color: #64748b; font-size: 14px;">端到端加密 / 严格访问控制 / NDA/NCA 协议保护</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #1e3a5f; margin-bottom: 8px;">📊 精选项目</h3>
            <p style="color: #64748b; font-size: 14px;">严格筛选 / 真实尽职调查 / 完善信息披露</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #1e3a5f; margin-bottom: 8px;">🤝 专业对接</h3>
            <p style="color: #64748b; font-size: 14px;">一对一服务 / 精准匹配 / 全流程跟踪</p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # 项目统计
    projects = load_projects()
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("在售项目", len(projects))
    with col2:
        st.metric("行业覆盖", "智能制造/新能源")
    with col3:
        st.metric("成功案例", "10+")
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
    if st.sidebar.button("🚪 退出登录", use_container_width=True):
        logout()

    st.sidebar.divider()
    st.sidebar.markdown("### 📌 快速导航")

    # 页面选择
    pages = {
        "📋 项目列表": "projects_list",
        "🔍 搜索中心": "search",
        "👤 用户中心": "user_center",
    }

    # 管理员额外入口
    if st.session_state.user_info.get("role") == "admin":
        st.sidebar.divider()
        st.sidebar.markdown("### 🔧 管理后台")
        if st.sidebar.button("📝 发布项目", use_container_width=True):
            st.switch_page("pages/admin_center.py")

    selection = st.sidebar.radio("跳转页面", list(pages.keys()))

    # 渲染对应页面
    if selection == "📋 项目列表":
        from pages.projects_list import render
        render()
    elif selection == "🔍 搜索中心":
        from pages.search import render
        render()
    elif selection == "👤 用户中心":
        from pages.user_center import render
        render()


if __name__ == "__main__":
    main()
