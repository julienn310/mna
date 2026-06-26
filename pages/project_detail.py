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

    project_type = project.get("project_type", "卖方")
    is_seller = project_type == "卖方"

    # 返回按钮
    if st.button("← 返回项目列表"):
        st.switch_page("pages/projects_list.py")

    st.markdown("---")

    # 项目头部信息
    type_label = "📤 卖方项目" if is_seller else "📥 买方需求"
    type_color = "#1e3a5f" if is_seller else "#0d7377"

    st.markdown(f"""
    <style>
        .detail-header {{
            padding: 24px;
            background: linear-gradient(135deg, #0f2439 0%, #1e3a5f 100%);
            border-radius: 12px;
            margin-bottom: 24px;
        }}
        .detail-section {{
            background: #ffffff;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 16px;
            border: 1px solid #e2e8f0;
        }}
        .section-title {{
            color: #1e3a5f;
            font-size: 16px;
            font-weight: 600;
            margin-bottom: 12px;
            padding-bottom: 8px;
            border-bottom: 2px solid #14919b;
        }}
    </style>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([3, 1])

    with col1:
        st.markdown(f"""
        <div class="detail-header">
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 16px;">
                <span style="background: {type_color}; color: white; padding: 6px 14px; border-radius: 6px; font-size: 14px; font-weight: 500;">
                    {type_label}
                </span>
                <span style="background: rgba(255,255,255,0.15); color: #94a3b8; padding: 6px 14px; border-radius: 6px; font-size: 14px;">
                    {project.get('id', 'N/A')}
                </span>
                <span style="background: #0d7377; color: white; padding: 6px 14px; border-radius: 6px; font-size: 14px;">
                    🟢 {project.get('status', '在售')}
                </span>
            </div>
            <h1 style="color: white; margin: 0; font-size: 24px; font-weight: 600;">{project.get('name', 'N/A')}</h1>
            <p style="color: #94a3b8; margin-top: 12px; font-size: 15px;">
                🏭 {project.get('industry', 'N/A')} &nbsp;|&nbsp; 📍 {project.get('region', 'N/A')} &nbsp;|&nbsp; 📊 {project.get('phase', 'N/A')}
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="background: #ffffff; padding: 20px; border-radius: 10px; border: 1px solid #e2e8f0; text-align: center;">
            <div style="color: #64748b; font-size: 13px; margin-bottom: 8px;">交易股比</div>
            <div style="font-size: 28px; font-weight: 700; color: #1e3a5f;">{}</div>
        </div>
        """.format(project.get('share_ratio', 'N/A')), unsafe_allow_html=True)

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
        if project.get("company_intro"):
            st.markdown('<div class="detail-section">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">🏢 公司简介</div>', unsafe_allow_html=True)
            st.markdown(project.get("company_intro"))
            st.markdown('</div>', unsafe_allow_html=True)

        if project.get("financial"):
            st.markdown('<div class="detail-section">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">💰 财务概况</div>', unsafe_allow_html=True)
            st.markdown(project.get("financial"))
            st.markdown('</div>', unsafe_allow_html=True)

        if project.get("valuation"):
            st.markdown('<div class="detail-section">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">📊 估值与合作</div>', unsafe_allow_html=True)
            st.markdown(project.get("valuation"))
            st.markdown('</div>', unsafe_allow_html=True)

    # ====================
    # 买方项目详情
    # ====================
    else:
        if project.get("buyer_requirements"):
            st.markdown('<div class="detail-section">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">🎯 目标公司要求</div>', unsafe_allow_html=True)
            st.markdown(project.get("buyer_requirements"))
            st.markdown('</div>', unsafe_allow_html=True)

        if project.get("buyer_profile"):
            st.markdown('<div class="detail-section">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">👤 买方简介</div>', unsafe_allow_html=True)
            st.markdown(project.get("buyer_profile"))
            st.markdown('</div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            if project.get("buyer_budget"):
                st.markdown('<div class="detail-section">', unsafe_allow_html=True)
                st.markdown('<div class="section-title">💵 并购预算</div>', unsafe_allow_html=True)
                st.markdown(project.get("buyer_budget"))
                st.markdown('</div>', unsafe_allow_html=True)
        with col2:
            if project.get("buyer_synergy"):
                st.markdown('<div class="detail-section">', unsafe_allow_html=True)
                st.markdown('<div class="section-title">🤝 协同资源</div>', unsafe_allow_html=True)
                st.markdown(project.get("buyer_synergy"))
                st.markdown('</div>', unsafe_allow_html=True)

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
