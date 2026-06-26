"""
项目列表页面
显示所有在售项目，支持筛选和快速预览
"""

import streamlit as st
import pandas as pd
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.data_manager import load_projects, get_filter_options

def render():
    """渲染项目列表页"""

    st.markdown("""
    <style>
        .project-card {
            padding: 20px;
            background: #ffffff;
            border-radius: 10px;
            margin-bottom: 16px;
            border: 1px solid #e2e8f0;
            box-shadow: 0 2px 8px rgba(15, 36, 57, 0.05);
            border-left: 4px solid #14919b;
        }
        .project-card:hover {
            box-shadow: 0 4px 16px rgba(15, 36, 57, 0.1);
        }
        .badge {
            display: inline-block;
            padding: 3px 10px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: 500;
        }
        .badge-seller { background: #1e3a5f; color: white; }
        .badge-buyer { background: #0d7377; color: white; }
        .badge-onsale { background: #ecfdf5; color: #0d7377; border: 1px solid #0d7377; }
        .badge-sold { background: #fef2f2; color: #dc2626; border: 1px solid #dc2626; }
    </style>
    """, unsafe_allow_html=True)

    st.title("📋 并购重组项目列表")
    st.markdown("---")

    # 加载筛选选项
    filters = get_filter_options()

    # 侧边筛选器
    with st.sidebar:
        st.markdown("### 🔍 筛选条件")

        # 项目类型
        project_type = st.selectbox(
            "项目类型",
            ["全部", "卖方", "买方"]
        )

        # 行业
        industry = st.selectbox(
            "行业",
            ["全部"] + filters.get("industries", [])
        )

        # 地区
        region = st.selectbox(
            "地区",
            ["全部"] + filters.get("regions", [])
        )

        # 交易阶段
        phase = st.selectbox(
            "交易需求",
            ["全部"] + filters.get("phases", [])
        )

        # 重置筛选
        if st.button("🔄 重置筛选", use_container_width=True):
            project_type = "全部"
            industry = "全部"
            region = "全部"
            phase = "全部"

    # 加载项目数据
    df = load_projects()

    # 应用筛选
    if project_type != "全部":
        df = df[df["project_type"] == project_type]
    if industry != "全部":
        df = df[df["industry"] == industry]
    if region != "全部":
        df = df[df["region"] == region]
    if phase != "全部":
        df = df[df["phase"] == phase]

    # 过滤在售项目
    df = df[df["status"] == "在售"]

    # 显示统计
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("在售项目", len(df))
    with col2:
        st.metric("行业覆盖", len(df["industry"].unique()) if len(df) > 0 else 0)
    with col3:
        if len(df) > 0:
            st.metric("最新更新", df["created_at"].max())

    st.markdown("---")

    # 项目卡片展示
    if len(df) == 0:
        st.info("暂无符合条件的项目")
        return

    st.markdown("### 项目概览")

    for idx, row in df.iterrows():
        is_seller = row.get("project_type", "卖方") == "卖方"
        type_badge = '<span class="badge badge-seller">📤 卖方</span>' if is_seller else '<span class="badge badge-buyer">📥 买方</span>'
        status_badge = '<span class="badge badge-onsale">🟢 在售</span>' if row.get("status") == "在售" else '<span class="badge badge-sold">🔴 已下架</span>'

        with st.container():
            col1, col2 = st.columns([4, 1])

            with col1:
                st.markdown(f"""
                <div class="project-card">
                    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 12px;">
                        {type_badge}
                        {status_badge}
                        <span style="background: #f1f5f9; color: #64748b; padding: 3px 10px; border-radius: 4px; font-size: 12px;">
                            {row.get('id', 'N/A')}
                        </span>
                    </div>
                    <h3 style="color: #1e293b; margin: 0 0 10px 0; font-size: 18px;">{row.get('name', 'N/A')}</h3>
                    <div style="color: #64748b; font-size: 14px; margin-bottom: 10px;">
                        🏭 {row.get('industry', 'N/A')} &nbsp;|&nbsp; 📍 {row.get('region', 'N/A')} &nbsp;|&nbsp; 📊 {row.get('phase', 'N/A')}
                    </div>
                    <div style="color: #94a3b8; font-size: 13px;">
                        {row.get('highlights', '暂无简介')}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown("**交易类型**")
                st.markdown(f"**{row.get('phase', 'N/A')}**")
                st.markdown(f"股比：{row.get('share_ratio', 'N/A')}")

            # 操作按钮
            col_btn1, col_btn2 = st.columns([1, 1])
            with col_btn1:
                if st.button(f"📄 详情", key=f"detail_{row['id']}", use_container_width=True):
                    st.session_state.selected_project = row["id"]
                    st.switch_page("pages/project_detail.py")
            with col_btn2:
                if st.button(f"⭐ 收藏", key=f"fav_{row['id']}", use_container_width=True):
                    st.success("已收藏")

            st.markdown("---")

if __name__ == "__main__":
    render()
