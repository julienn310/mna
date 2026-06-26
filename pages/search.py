"""
搜索中心页面
支持关键词搜索和高级筛选
"""

import streamlit as st
import pandas as pd
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.data_manager import search_projects, get_filter_options

def render():
    """渲染搜索页"""

    st.markdown("""
    <style>
        .search-result-card {
            padding: 20px;
            background: #ffffff;
            border-radius: 10px;
            margin-bottom: 16px;
            border: 1px solid #e2e8f0;
            border-left: 4px solid #14919b;
        }
        .search-result-card:hover {
            box-shadow: 0 4px 16px rgba(15, 36, 57, 0.1);
        }
    </style>
    """, unsafe_allow_html=True)

    st.title("🔍 项目搜索中心")
    st.markdown("---")

    # 搜索框
    col1, col2 = st.columns([4, 1])
    with col1:
        keyword = st.text_input(
            "🔎 关键词搜索",
            placeholder="输入行业、公司名、产品、关键词...",
            label_visibility="collapsed"
        )
    with col2:
        search_btn = st.button("搜索", use_container_width=True)

    # 高级筛选
    with st.expander("⚡ 高级筛选"):
        filters = get_filter_options()

        col1, col2, col3 = st.columns(3)

        with col1:
            industry = st.selectbox("行业", ["全部"] + filters.get("industries", []))

        with col2:
            region = st.selectbox("地区", ["全部"] + filters.get("regions", []))

        with col3:
            phase = st.selectbox("交易需求", ["全部"] + filters.get("phases", []))

    st.markdown("---")

    # 执行搜索
    if keyword or search_btn:
        df = search_projects(
            keyword=keyword,
            industry=industry if industry != "全部" else "",
            region=region if region != "全部" else "",
            phase=phase if phase != "全部" else ""
        )

        # 过滤在售
        df = df[df["status"] == "在售"]

        st.markdown(f"### 搜索结果：找到 {len(df)} 个项目")

        if len(df) == 0:
            st.info("未找到符合条件的项目，请尝试其他关键词")
            return

        # 结果展示
        for idx, row in df.iterrows():
            is_seller = row.get("project_type", "卖方") == "卖方"
            type_icon = "📤" if is_seller else "📥"

            with st.container():
                col1, col2 = st.columns([4, 1])

                with col1:
                    if keyword:
                        st.markdown(f"**匹配词：** `{keyword}`")

                    st.markdown(f"""
                    <div class="search-result-card">
                        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;">
                            <span style="background: #1e3a5f; color: white; padding: 3px 10px; border-radius: 4px; font-size: 12px;">
                                {type_icon} {row.get('id', 'N/A')}
                            </span>
                            <strong style="font-size: 17px; color: #1e293b;">{row.get('name', 'N/A')}</strong>
                        </div>
                        <div style="color: #64748b; font-size: 14px; margin-bottom: 8px;">
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

                    if st.button(f"查看详情 →", key=f"search_detail_{row['id']}"):
                        st.session_state.selected_project = row["id"]
                        st.switch_page("pages/project_detail.py")

                st.markdown("---")
    else:
        # 空搜索显示推荐
        st.info("👆 输入关键词开始搜索，或使用高级筛选")

        df = search_projects(status="在售").head(5)
        if len(df) > 0:
            st.markdown("### 📌 推荐项目")
            for idx, row in df.iterrows():
                is_seller = row.get("project_type", "卖方") == "卖方"
                type_icon = "📤" if is_seller else "📥"

                col1, col2 = st.columns([4, 1])
                with col1:
                    st.markdown(f"**{type_icon} {row.get('name', 'N/A')}**")
                    st.caption(f"{row.get('industry', 'N/A')} | {row.get('region', 'N/A')} | {row.get('phase', 'N/A')}")
                with col2:
                    if st.button(f"查看", key=f"rec_detail_{row['id']}"):
                        st.session_state.selected_project = row["id"]
                        st.switch_page("pages/project_detail.py")

if __name__ == "__main__":
    render()
