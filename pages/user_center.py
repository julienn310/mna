"""
用户中心页面
用户信息管理、收藏、项目申请记录
"""

import streamlit as st
import pandas as pd
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.data_manager import load_projects

def render():
    """渲染用户中心页"""

    st.markdown("""
    <style>
        .user-card {
            background: linear-gradient(135deg, #1e3a5f 0%, #2d5a87 100%);
            padding: 24px;
            border-radius: 12px;
            color: white;
            text-align: center;
        }
    </style>
    """, unsafe_allow_html=True)

    st.title("👤 用户中心")
    st.markdown("---")

    # 用户信息卡片
    if st.session_state.user_info:
        user = st.session_state.user_info
    else:
        user = {"name": "未知用户", "username": st.session_state.get("user", "guest")}

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div class="user-card">
            <div style="font-size: 48px; margin-bottom: 8px;">👤</div>
            <div style="font-size: 20px; font-weight: bold;">{user.get("name", "用户")}</div>
            <div style="font-size: 14px; opacity: 0.8;">@{user.get("username", "")}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.metric("收藏项目", "0")
    with col3:
        st.metric("申请记录", "0")

    st.markdown("---")

    # 功能标签页
    tab1, tab2, tab3, tab4 = st.tabs(["📋 收藏项目", "📝 申请记录", "⚙️ 账户设置", "🔐 安全设置"])

    with tab1:
        st.markdown("### ⭐ 我的收藏")
        st.info("暂无收藏项目")

        st.markdown("**快速浏览热门项目**")
        if st.button("查看项目列表"):
            st.switch_page("pages/projects_list.py")

    with tab2:
        st.markdown("### 📝 我的申请")
        st.info("暂无申请记录")

        st.markdown("""
        **申请流程说明：**
        1. 在项目详情页点击「申请对接」
        2. 填写您的意向和联系方式
        3. 平台审核后安排双方对接
        """)

    with tab3:
        st.markdown("### ⚙️ 账户设置")

        with st.form("profile_form"):
            st.markdown("#### 基本信息")

            name = st.text_input("姓名/公司名", value=user.get("name", ""))
            email = st.text_input("邮箱", placeholder="用于接收平台通知")
            phone = st.text_input("手机号", placeholder="用于平台联系")

            st.markdown("#### 认证信息")

            company = st.text_input("所属公司", placeholder="您的公司名称")
            role = st.selectbox(
                "用户类型",
                ["投资机构", "FA/财务顾问", "企业", "个人投资者", "其他"]
            )

            if st.form_submit_button("保存修改", use_container_width=True):
                st.success("信息已保存")

    with tab4:
        st.markdown("### 🔐 安全设置")

        with st.form("password_form"):
            st.markdown("#### 修改密码")

            old_password = st.text_input("当前密码", type="password")
            new_password = st.text_input("新密码", type="password")
            confirm_password = st.text_input("确认新密码", type="password")

            if st.form_submit_button("修改密码", use_container_width=True):
                if new_password != confirm_password:
                    st.error("两次密码输入不一致")
                elif len(new_password) < 6:
                    st.error("密码长度至少6位")
                else:
                    st.success("密码已修改")

        st.markdown("---")

        st.markdown("#### 登录日志")

        log_data = {
            "时间": ["2026-06-26 10:30:00", "2026-06-26 09:00:00"],
            "IP": ["192.168.1.100", "192.168.1.100"],
            "设备": ["Chrome/Windows", "微信小程序"],
            "状态": ["成功", "成功"]
        }
        st.dataframe(pd.DataFrame(log_data), use_container_width=True)

    st.markdown("---")

    st.caption(f"最后登录：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | 平台版本：v1.0.0 (Demo)")

if __name__ == "__main__":
    render()
