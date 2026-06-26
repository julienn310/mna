"""
项目详情页面
展示单个项目的完整信息（支持卖方/买方项目）
"""

import streamlit as st
import pandas as pd
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.data_manager import get_project_by_id

def render():
    """渲染项目详情页"""

    # 获取项目ID
    if "selected_project" not in st.session_state:
        st.error("请先从项目列表选择项目")
        if st.button("返回项目列表"):
            st.switch_page("pages/projects_list.py")
        return

    project_id = st.session_state.selected_project
    project = get_project_by_id(project_id)

    if not project:
        st.error("项目不存在或已下架")
        if st.button("返回项目列表"):
            st.switch_page("pages/projects_list.py")
        return

    # 返回按钮
    if st.button("← 返回项目列表"):
        st.switch_page("pages/projects_list.py")

    st.markdown("---")

    project_type = project.get("project_type", "卖方")
    is_seller = project_type == "卖方"

    # 项目头部信息
    col1, col2 = st.columns([3, 1])

    with col1:
        type_label = "📤 卖方项目" if is_seller else "📥 买方需求"
        type_color = "#4263eb" if is_seller else "#2ecc71"

        st.markdown(f"""
        <div style="
            padding: 20px;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            border-radius: 12px;
            margin-bottom: 20px;
        ">
            <div style="display: flex; align-items: center; gap: 16px; margin-bottom: 12px;">
                <span style="
                    background: {type_color};
                    color: white;
                    padding: 4px 12px;
                    border-radius: 6px;
                    font-size: 14px;
                ">{type_label}</span>
                <span style="
                    background: #6c757d;
                    color: white;
                    padding: 4px 12px;
                    border-radius: 6px;
                    font-size: 14px;
                ">{project.get('id', 'N/A')}</span>
                <span style="
                    background: #2ecc71;
                    color: white;
                    padding: 4px 12px;
                    border-radius: 6px;
                    font-size: 14px;
                ">{project.get('status', '在售')}</span>
            </div>
            <h1 style="color: white; margin: 0; font-size: 24px;">{project.get('name', 'N/A')}</h1>
            <p style="color: #a0a0a0; margin-top: 8px;">
                🏭 {project.get('industry', 'N/A')} | 📍 {project.get('region', 'N/A')} | 📊 {project.get('phase', 'N/A')}
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("### 交易信息")
        st.markdown(f"""
        <div style="
            padding: 16px;
            background: #f8f9fa;
            border-radius: 8px;
            text-align: center;
        ">
            <div style="color: #666; font-size: 12px;">{project_type}股比</div>
            <div style="font-size: 24px; font-weight: bold; color: #1a1a2e;">{project.get('share_ratio', 'N/A')}</div>
        </div>
        """, unsafe_allow_html=True)

    # 核心亮点
    if project.get("highlights"):
        st.markdown("### ✨ 核心亮点")
        highlights = project.get("highlights", "").split("|")
        cols = st.columns(len(highlights))
        for i, h in enumerate(highlights):
            with cols[i]:
                st.info(h.strip())

    st.markdown("---")

    # ====================
    # 卖方项目详情
    # ====================
    if is_seller:
        # 公司简介
        if project.get("company_intro"):
            st.markdown("### 🏢 公司简介")
            st.markdown(project.get("company_intro"))

        st.markdown("---")

        # 财务概况
        if project.get("financial"):
            st.markdown("### 💰 财务概况")
            st.markdown(project.get("financial"))

        st.markdown("---")

        # 估值与合作
        if project.get("valuation"):
            st.markdown("### 📊 估值与合作")
            st.markdown(project.get("valuation"))

    # ====================
    # 买方项目详情
    # ====================
    else:
        # 买方收购需求
        if project.get("buyer_requirements"):
            st.markdown("### 🎯 目标公司要求")
            st.markdown(project.get("buyer_requirements"))

        st.markdown("---")

        # 买方简介
        if project.get("buyer_profile"):
            st.markdown("### 👤 买方简介")
            st.markdown(project.get("buyer_profile"))

        st.markdown("---")

        # 并购预算 & 协同资源
        col1, col2 = st.columns(2)
        with col1:
            if project.get("buyer_budget"):
                st.markdown("### 💵 并购预算")
                st.markdown(project.get("buyer_budget"))
        with col2:
            if project.get("buyer_synergy"):
                st.markdown("### 🤝 协同资源")
                st.markdown(project.get("buyer_synergy"))

    st.markdown("---")

    # 底部操作按钮
    st.markdown("### 📞 联系获取更多资料")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📋 申请对接", use_container_width=True, type="primary"):
            st.info("请联系平台管理员获取详细资料")

    with col2:
        if st.button("⭐ 收藏项目", use_container_width=True):
            st.success("已收藏")

    with col3:
        if st.button("📤 分享给同事", use_container_width=True):
            st.info("链接已复制到剪贴板")

    # 敏感信息提示
    st.markdown("---")
    st.caption("""
    ⚠️ **保密提示**：本页面所载信息仅供授权用户查看，未经授权不得对外披露。
    如需深入了解项目详情，请联系平台进行 NDA/NCA 签署。
    """)

if __name__ == "__main__":
    render()
