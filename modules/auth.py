"""
认证模块
处理用户注册、登录、会话管理
使用简化的 Session-based 认证，适合 MVP
"""

import streamlit as st
import bcrypt
import yaml
from datetime import datetime
from pathlib import Path

# ======================
# 配置
# ======================
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
USERS_FILE = DATA_DIR / "users.yaml"

# 确保目录存在
DATA_DIR.mkdir(exist_ok=True)

# ======================
# 用户数据管理
# ======================

def load_users() -> dict:
    """加载用户数据"""
    if not USERS_FILE.exists():
        return {}
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except:
        return {}


def save_users(users: dict):
    """保存用户数据"""
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        yaml.dump(users, f, allow_unicode=True, default_flow_style=False)


def hash_password(password: str) -> str:
    """密码哈希"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password: str, hashed: str) -> bool:
    """验证密码"""
    try:
        return bcrypt.checkpw(password.encode(), hashed.encode())
    except:
        return False


def create_user(username: str, name: str, password: str, phone: str = "", role: str = "user") -> bool:
    """创建新用户"""
    users = load_users()
    if username in users:
        return False
    users[username] = {
        "name": name,
        "password": hash_password(password),
        "role": role,
        "phone": phone or "",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    save_users(users)
    return True


def verify_user(username: str, password: str) -> dict:
    """验证用户登录"""
    users = load_users()
    if username not in users:
        return None
    if verify_password(password, users[username]["password"]):
        return {
            "username": username,
            "name": users[username]["name"],
            "role": users[username].get("role", "user")
        }
    return None


def init_auth():
    """初始化认证系统 - 确保默认管理员存在"""
    users = load_users()
    if "admin" not in users:
        users["admin"] = {
            "name": "管理员",
            "password": hash_password("admin123"),
            "role": "admin",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        save_users(users)
    return True


# ======================
# 渲染登录/注册界面
# ======================

def render_login_register():
    """渲染登录注册界面"""

    # 初始化认证
    init_auth()

    # 创建 Tab
    tab1, tab2 = st.tabs(["🔐 登录", "📝 注册"])

    with tab1:
        st.markdown("### 登录账户")

        with st.form("login_form", clear_on_submit=True):
            username = st.text_input("用户名", placeholder="请输入用户名", autocomplete="username")
            password = st.text_input("密码", type="password", placeholder="请输入密码", autocomplete="current-password")
            submitted = st.form_submit_button("登录", use_container_width=True)

            if submitted:
                if not username or not password:
                    st.error("请输入用户名和密码")
                else:
                    user = verify_user(username, password)
                    if user:
                        st.session_state.authenticated = True
                        st.session_state.user = username
                        st.session_state.user_info = user
                        st.success(f"欢迎回来，{user['name']}！")
                        st.rerun()
                    else:
                        st.error("用户名或密码错误")

    with tab2:
        st.markdown("### 注册新账户")

        with st.form("register_form", clear_on_submit=True):
            new_username = st.text_input("用户名", placeholder="设置用户名", autocomplete="new-username")
            new_name = st.text_input("姓名/公司名", placeholder="请输入姓名或公司名")
            new_phone = st.text_input("手机号", placeholder="用于平台联系（选填）")
            new_password = st.text_input("密码", type="password", placeholder="设置密码（至少6位）")
            confirm_password = st.text_input("确认密码", type="password", placeholder="再次输入密码")
            submitted = st.form_submit_button("注册", use_container_width=True)

            if submitted:
                if not new_username or not new_name or not new_password:
                    st.error("请填写所有字段")
                elif new_password != confirm_password:
                    st.error("两次密码输入不一致")
                elif len(new_password) < 6:
                    st.error("密码长度至少6位")
                else:
                    if create_user(new_username, new_name, new_password, new_phone):
                        st.success("注册成功！请登录")
                    else:
                        st.error("用户名已存在")


def logout():
    """退出登录"""
    st.session_state.authenticated = False
    st.session_state.user = None
    st.session_state.user_info = None
    st.rerun()
