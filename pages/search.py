"""
搜索中心页面
支持关键词搜索和高级筛选
"""

import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.data_manager import search_projects, get_filter_options

def render():
    """渲染搜索页"""

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
    with st.expander(" 高级筛选"):
        filters = get_filter_options()

        col1, col2, col3 = st.columns(3)

        with col1:
            industry = st.selectbox("行业", ["全部"] + filters.get("industries", []))

        with col2:
            region = st.selectbox("地区", ["全部"] + filters.get("regions", []))

        with col3:
            phase = st.selectbox("交易阶段", ["全部"] + filters.get("phases", []))

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
            with st.container():
                col1, col2 = st.columns([4, 1])

                with col1:
                    # 匹配高亮
                    if keyword:
                        st.markdown(f"**匹配词：** {keyword}")

                    st.markdown(f"""
                    <div style="
                        padding: 16px;
                        background: #f8f9fa;
                        border-radius: 8px;
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
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.markdown(f"**{row.get('name', 'N/A')}**")
                    st.caption(f"{row.get('industry', 'N/A')} | {row.get('region', 'N/A')}")
                with col2:
                    if st.button(f"查看", key=f"rec_detail_{row['id']}"):
                        st.session_state.selected_project = row["id"]
                        st.switch_page("pages/project_detail.py")

if __name__ == "__main__":
    render()
