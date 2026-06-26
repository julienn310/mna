"""
管理员后台
仅管理员可访问，用于发布和管理项目
"""

import streamlit as st
import pandas as pd
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.data_manager import (
    load_projects, add_project, delete_project,
    update_project as update_proj, get_filter_options,
    get_project_by_id
)

def render():
    """渲染管理员后台"""

    # 权限检查
    if not st.session_state.get("authenticated") or st.session_state.get("user_info", {}).get("role") != "admin":
        st.error("⛔ 您没有权限访问此页面")
        st.info("只有管理员才能发布项目。如需发布，请联系管理员。")
        return

    # 初始化编辑状态
    if "editing_project_id" not in st.session_state:
        st.session_state.editing_project_id = None

    st.title("🔧 管理员后台")
    st.markdown("---")

    # 功能标签页
    tab1, tab2, tab3 = st.tabs(["📝 发布新项目", "📋 项目管理", "👥 用户管理"])

    # ====================
    # 发布新项目
    # ====================
    with tab1:
        st.markdown("### 📝 发布新项目")

        with st.form("add_project_form", clear_on_submit=True):
            # 项目类型选择
            project_type = st.selectbox(
                "项目类型 *",
                ["卖方", "买方"],
                help="卖方=有项目要出售/被并购 | 买方=有收购需求"
            )

            st.markdown("#### 基本信息")

            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("项目名称 *", placeholder="例如：欧洲精密制造企业在华子公司")
            with col2:
                code = st.text_input("项目编号", placeholder="例如：MNA-2026-001")

            col3, col4 = st.columns(2)
            with col3:
                industry = st.selectbox("行业 *", [
                    "智能驾驶", "精密制造", "新能源", "汽车零部件", "医疗健康",
                    "半导体", "软件/IT", "消费品", "工业制造", "电子制造", "其他"
                ])
            with col4:
                region = st.selectbox("地区 *", [
                    "华东", "华北", "华南", "华中", "西南", "西北", "东北", "国内", "海外"
                ])

            col5, col6 = st.columns(2)
            with col5:
                if project_type == "卖方":
                    phase = st.selectbox("交易需求 *", [
                        "出售股权", "被并购", "可参可控", "战略合作", "融资"
                    ])
                else:
                    phase = st.selectbox("交易需求 *", [
                        "收购", "可参可控"
                    ])
            with col6:
                share_ratio = st.text_input("出让/收购股比", placeholder="例如：100% 或 控股")

            highlights = st.text_input("核心亮点", placeholder="用 | 分隔，例如：上市公司|智能驾驶|控制权收购")

            # ====================
            # 卖方项目表单
            # ====================
            if project_type == "卖方":
                st.markdown("#### 公司简介")

                company_intro = st.text_area(
                    "公司简介（支持换行）",
                    height=200,
                    placeholder="""【公司概况】
...

【主营业务】
...

【主营产品】
..."""
                )

                st.markdown("#### 财务概况")
                financial = st.text_area(
                    "财务信息",
                    height=150,
                    placeholder="""【营收】X 亿元人民币
【净利润】X 千万元人民币"""
                )

                st.markdown("#### 估值与合作")
                valuation = st.text_area(
                    "估值与合作方式",
                    height=100,
                    placeholder="""【估值】另议
【合作方向】买方顾问方向"""
                )

                # 买方字段留空
                buyer_requirements = ""
                buyer_profile = ""
                buyer_budget = ""
                buyer_synergy = ""

            # ====================
            # 买方项目表单
            # ====================
            else:
                st.markdown("#### 买方收购需求")

                buyer_requirements = st.text_area(
                    "目标公司要求",
                    height=180,
                    placeholder="""【目标公司要求】
• 行业：智能驾驶行业
• 业务规模：有一定业务规模
• 标的区域：国内
• 主营业务：智能驾驶产业链产品研发、生产和销售
• 主营产品：智能驾驶产业链相关产品
• 市场地位：细分领域市场前列
• 财务要求：亏损但接近盈亏平衡、或有净利
• 融资估值要求：历史融资估值规模超过10亿元"""
                )

                st.markdown("#### 买方简介")
                buyer_profile = st.text_area(
                    "买方简介",
                    height=100,
                    placeholder="""【买方简介】
上市公司，主营电子产品制造，有并购经验"""
                )

                col7, col8 = st.columns(2)
                with col7:
                    buyer_budget = st.text_input("并购预算", placeholder="例如：XX亿元")
                with col8:
                    buyer_synergy = st.text_input("协同资源", placeholder="产业链上下游、销售渠道等")

                # 卖方字段留空
                company_intro = ""
                financial = ""
                valuation = ""

            submitted = st.form_submit_button("🚀 发布项目", use_container_width=True)

            if submitted:
                if not name or not industry or not region:
                    st.error("请填写必填字段（*）")
                else:
                    project_data = {
                        "name": name,
                        "code": code or f"MNA-{datetime.now().strftime('%Y%m%d')}",
                        "project_type": project_type,
                        "industry": industry,
                        "region": region,
                        "phase": phase,
                        "share_ratio": share_ratio or "待定",
                        "highlights": highlights or "",
                        "company_intro": company_intro,
                        "financial": financial,
                        "valuation": valuation,
                        "status": "在售",
                        "company_type": "",
                        "sub_industry": "",
                        "buyer_requirements": buyer_requirements,
                        "buyer_profile": buyer_profile,
                        "buyer_budget": buyer_budget,
                        "buyer_synergy": buyer_synergy,
                    }

                    if add_project(project_data):
                        st.success(f"✅ 项目「{name}」发布成功！")
                    else:
                        st.error("发布失败，请重试")

    # ====================
    # 项目管理
    # ====================
    with tab2:
        st.markdown("### 📋 项目管理")

        df = load_projects()

        # 如果正在编辑，显示编辑表单
        if st.session_state.editing_project_id:
            project = get_project_by_id(st.session_state.editing_project_id)
            if project:
                st.markdown("#### ✏️ 编辑项目")

                with st.form("edit_project_form", clear_on_submit=True):
                    project_type_edit = st.selectbox(
                        "项目类型 *",
                        ["卖方", "买方"],
                        index=0 if project.get("project_type") == "卖方" else 1
                    )

                    col1, col2 = st.columns(2)
                    with col1:
                        name = st.text_input("项目名称 *", value=project.get("name", ""))
                    with col2:
                        code = st.text_input("项目编号", value=project.get("code", ""))

                    col3, col4 = st.columns(2)
                    industries = ["智能驾驶", "精密制造", "新能源", "汽车零部件", "医疗健康",
                        "半导体", "软件/IT", "消费品", "工业制造", "电子制造", "其他"]
                    current_industry = project.get("industry", "其他")
                    industry_idx = industries.index(current_industry) if current_industry in industries else 0
                    with col3:
                        industry = st.selectbox("行业 *", industries, index=industry_idx)
                    regions = ["华东", "华北", "华南", "华中", "西南", "西北", "东北", "国内", "海外"]
                    current_region = project.get("region", "华东")
                    region_idx = regions.index(current_region) if current_region in regions else 0
                    with col4:
                        region = st.selectbox("地区 *", regions, index=region_idx)

                    phases_seller = ["出售股权", "被并购", "可参可控", "战略合作", "融资"]
                    phases_buyer = ["收购", "可参可控"]
                    phases = phases_seller if project_type_edit == "卖方" else phases_buyer
                    current_phase = project.get("phase", "出售股权")
                    phase_idx = phases.index(current_phase) if current_phase in phases else 0
                    col5, col6 = st.columns(2)
                    with col5:
                        phase = st.selectbox("交易需求 *", phases, index=phase_idx)
                    with col6:
                        share_ratio = st.text_input("出让/收购股比", value=project.get("share_ratio", ""))

                    highlights = st.text_input("核心亮点", value=project.get("highlights", ""))

                    if project_type_edit == "卖方":
                        st.markdown("#### 公司简介")
                        company_intro = st.text_area("公司简介", value=project.get("company_intro", ""), height=200)
                        st.markdown("#### 财务概况")
                        financial = st.text_area("财务信息", value=project.get("financial", ""), height=150)
                        st.markdown("#### 估值与合作")
                        valuation = st.text_area("估值与合作", value=project.get("valuation", ""), height=100)
                        buyer_requirements = project.get("buyer_requirements", "")
                        buyer_profile = project.get("buyer_profile", "")
                        buyer_budget = project.get("buyer_budget", "")
                        buyer_synergy = project.get("buyer_synergy", "")
                    else:
                        st.markdown("#### 买方收购需求")
                        buyer_requirements = st.text_area("目标公司要求", value=project.get("buyer_requirements", ""), height=180)
                        st.markdown("#### 买方简介")
                        buyer_profile = st.text_area("买方简介", value=project.get("buyer_profile", ""), height=100)
                        col7, col8 = st.columns(2)
                        with col7:
                            buyer_budget = st.text_input("并购预算", value=project.get("buyer_budget", ""))
                        with col8:
                            buyer_synergy = st.text_input("协同资源", value=project.get("buyer_synergy", ""))
                        company_intro = project.get("company_intro", "")
                        financial = project.get("financial", "")
                        valuation = project.get("valuation", "")

                    col_save, col_cancel = st.columns(2)
                    with col_save:
                        submitted = st.form_submit_button("💾 保存修改", use_container_width=True)
                    with col_cancel:
                        if st.form_submit_button("取消编辑", use_container_width=True):
                            st.session_state.editing_project_id = None
                            st.rerun()

                    if submitted:
                        if not name or not industry or not region:
                            st.error("请填写必填字段（*）")
                        else:
                            updated_data = {
                                "name": name,
                                "code": code,
                                "project_type": project_type_edit,
                                "industry": industry,
                                "region": region,
                                "phase": phase,
                                "share_ratio": share_ratio or "待定",
                                "highlights": highlights or "",
                                "company_intro": company_intro or "",
                                "financial": financial or "",
                                "valuation": valuation or "",
                                "buyer_requirements": buyer_requirements or "",
                                "buyer_profile": buyer_profile or "",
                                "buyer_budget": buyer_budget or "",
                                "buyer_synergy": buyer_synergy or "",
                            }
                            update_proj(st.session_state.editing_project_id, updated_data)
                            st.session_state.editing_project_id = None
                            st.success("✅ 项目修改成功！")
                            st.rerun()

                st.markdown("---")

        if len(df) == 0:
            st.info("暂无项目")
        else:
            # 筛选器
            col1, col2, col3 = st.columns(3)
            with col1:
                filter_type = st.selectbox("类型", ["全部", "卖方", "买方"])
            with col2:
                filter_status = st.selectbox("状态", ["全部", "在售", "已下架"])
            with col3:
                filter_industry = st.selectbox("行业", ["全部"] + df["industry"].unique().tolist())

            # 应用筛选
            if filter_type != "全部":
                df = df[df["project_type"] == filter_type]
            if filter_status != "全部":
                df = df[df["status"] == filter_status]
            if filter_industry != "全部":
                df = df[df["industry"] == filter_industry]

            st.markdown(f"共 **{len(df)}** 个项目")

            # 展示项目列表
            for idx, row in df.iterrows():
                with st.container():
                    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])

                    with col1:
                        type_icon = "📤" if row.get("project_type") == "卖方" else "📥"
                        status_icon = "🟢" if row.get("status") == "在售" else "🔴"
                        st.markdown(f"{type_icon}{status_icon} **{row.get('name', 'N/A')}**")
                        st.caption(f"ID: {row.get('id', 'N/A')} | {row.get('industry', 'N/A')} | {row.get('phase', 'N/A')}")

                    with col2:
                        if st.button("✏️", key=f"edit_{row['id']}"):
                            st.session_state.editing_project_id = row["id"]
                            st.rerun()

                    with col3:
                        new_status = "已下架" if row.get("status") == "在售" else "在售"
                        if st.button("设", key=f"toggle_{row['id']}"):
                            update_proj(row["id"], {"status": new_status})
                            st.rerun()

                    with col4:
                        if st.button("🗑️", key=f"del_{row['id']}"):
                            delete_project(row["id"])
                            st.success("已删除")
                            st.rerun()

                    st.markdown("---")

    # ====================
    # 用户管理
    # ====================
    with tab3:
        st.markdown("### 👥 用户管理")

        from modules.auth import load_users
        users = load_users()

        if not users:
            st.info("暂无注册用户")
        else:
            user_list = []
            for username, data in users.items():
                user_list.append({
                    "用户名": username,
                    "姓名": data.get("name", ""),
                    "手机": data.get("phone", ""),
                    "角色": data.get("role", "user"),
                    "注册时间": data.get("created_at", "")
                })

            st.dataframe(pd.DataFrame(user_list), use_container_width=True)

            st.markdown("---")
            st.info("👤 普通用户角色：user | 🔧 管理员角色：admin")

if __name__ == "__main__":
    render()
