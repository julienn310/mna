"""
项目列表页面
显示所有在售项目，支持筛选和快速预览
"""

import streamlit as st
import pandas as pd
from modules.data_manager import load_projects, get_filter_options
import sys
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

def render():
    """渲染项目列表页"""

    st.title("📋 并购重组项目列表")
    st.markdown("---")

    # 加载筛选选项
    filters = get_filter_options()

    # 侧边筛选器
    with st.sidebar:
        st.markdown("### 🔍 筛选条件")

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
            "交易阶段",
            ["全部"] + filters.get("phases", [])
        )

        # 应用筛选
        if st.button("🔄 重置筛选", use_container_width=True):
            industry = "全部"
            region = "全部"
            phase = "全部"

    # 加载项目数据
    df = load_projects()

    # 应用筛选
    if industry != "全部":
        df = df[df["industry"] == industry]
    if region != "全部":
        df = df[df["region"] == region]
    if phase != "全部":
        df = df[df["phase"] == phase]

    # 过滤只在售项目
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

    # 表格展示 + 详情预览
    st.markdown("### 项目概览")

    # 简化显示字段
    display_cols = ["id", "name", "industry", "region", "phase", "highlights"]

    for idx, row in df.iterrows():
        with st.container():
            col1, col2, col3 = st.columns([3, 1, 1])

            with col1:
                st.markdown(f"""
                <div style="
                    padding: 16px;
                    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
                    border-radius: 12px;
                    margin-bottom: 12px;
                    border-left: 4px solid #4263eb;
                ">
                    <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 8px;">
                        <span style="
                            background: #4263eb;
                            color: white;
                            padding: 2px 8px;
                            border-radius: 4px;
                            font-size: 12px;
                        ">{row.get('id', 'N/A')}</span>
                        <strong style="font-size: 16px; color: #1a1a2e;">{row.get('name', 'N/A')}</strong>
                    </div>
                    <div style="color: #666; font-size: 14px; margin-bottom: 8px;">
                        🏭 {row.get('industry', 'N/A')} | 📍 {row.get('region', 'N/A')} | 📊 {row.get('phase', 'N/A')}
                    </div>
                    <div style="color: #888; font-size: 13px;">
                        {row.get('highlights', '暂无简介')}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown("**交易类型**")
                st.write(row.get("phase", "N/A"))

            with col3:
                st.markdown("**股比**")
                st.write(row.get("share_ratio", "N/A"))

            # 详情按钮
            col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])
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
