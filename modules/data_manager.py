"""
数据管理模块
处理项目数据、用户数据的读写操作
"""

import pandas as pd
import os
from datetime import datetime
from pathlib import Path

# ======================
# 路径配置
# ======================
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
PROJECTS_FILE = DATA_DIR / "projects.csv"
USERS_FILE = DATA_DIR / "users.yaml"

# 确保数据目录存在
DATA_DIR.mkdir(exist_ok=True)

# ======================
# 示例项目数据
# ======================
SAMPLE_PROJECTS = [
    {
        # ===== 卖方项目 =====
        "id": "MNA-2026-001",
        "name": "欧洲精密制造企业在华全资子公司",
        "code": "PM-CNSUB-001",
        "project_type": "卖方",  # 卖方/买方
        "industry": "精密制造",
        "sub_industry": "金属粉末制造",
        "region": "华东",
        "phase": "出售股权",
        "share_ratio": "100%",
        "company_intro": """【公司概况】
欧洲知名精密制造企业在华全资子公司，专注于金属粉末制造技术与工艺，拥有全球知名企业客户。

【股东结构】
欧洲企业100%持有

【主营业务】
齿轮、粉末冶金部件等产品的研发、设计和生产制造

【主营产品】
• 伞齿轮组
• 曲柄轴
• 转子轴
• 工具夹头等精密粉末冶金金属部件

【应用领域】
• 汽车
• 电动工具
• 户外产品
• 摩托车
• 园林机械等""",
        "financial": """【财务概况】
• 营收：X 亿元人民币
• EBITDA：X 千万元人民币

【出让股比】
100%

【合作方向】
• 买方顾问方向
• 买方付费对接

【对接流程】
本线索 → BT → NDA/NCA（我司） → 提供详细资料 → 安排直接考察/交流""",
        "valuation": "另议",
        "highlights": "全球知名企业客户 | 欧洲技术背景 | 100%股权转让",
        "status": "在售",
        "created_at": "2026-01-15",
        # 买方字段留空
        "buyer_requirements": "",
        "buyer_profile": "",
        "buyer_budget": "",
        "buyer_synergy": ""
    },
    {
        # ===== 买方项目 =====
        "id": "MNA-2026-002",
        "name": "上市公司智能驾驶产业链收购需求",
        "code": "NRG-SOFT-2026",
        "project_type": "买方",
        "industry": "智能驾驶",
        "sub_industry": "智能驾驶产业链",
        "region": "国内",
        "phase": "收购",
        "share_ratio": "控制权",
        "company_intro": "",  # 买方项目不需要这个
        "financial": "",      # 买方项目不需要这个
        "valuation": "",      # 买方项目不需要这个
        "highlights": "上市公司并购 | 智能驾驶赛道 | 控制权收购",
        "status": "在售",
        "created_at": "2026-02-20",
        # 买方详细需求
        "buyer_requirements": """【目标公司要求】
• 行业：智能驾驶行业
• 业务规模：有一定业务规模
• 细分领域：细分领域市场前列

【标的区域】
国内

【主营业务】
智能驾驶产业链产品研发、生产和销售

【主营产品】
智能驾驶产业链相关产品

【财务要求】
亏损但接近盈亏平衡、或有净利

【融资估值要求】
历史融资估值规模超过10亿元""",
        "buyer_profile": """【买方简介】
上市公司，主营电子产品制造，有并购经验""",
        "buyer_budget": """【并购预算】
XX亿元""",
        "buyer_synergy": """【买方协同资源】
• 产业链上下游
• 销售渠道
• 主机厂订单"""
    },
    {
        # ===== 卖方项目：新能源电站软件 =====
        "id": "MNA-2026-003",
        "name": "新能源电站软件产品服务商",
        "code": "NRG-SOFT-003",
        "project_type": "卖方",
        "industry": "新能源软件",
        "sub_industry": "功率预测/能源管理",
        "region": "华北",
        "phase": "被并购",
        "share_ratio": "控制权",
        "company_intro": """【项目简称】
XXXX

【主营】
为新能源电站、发电集团、电网公司及分布式电源拥有者提供以新能源发电功率预测产品为基础，以新能源电力交易辅助决策系统、新能源并网智能控制系统、新能源电网智能调度管理系统、储能EMS能源管理系统、虚拟电厂智慧运营管理平台为拓展的新能源软件产品及相关技术服务。

【对标企业】
国能日新（301162），目前市值90亿，市盈率70倍""",
        "financial": """【财务数据（2025年）】
• 收入：2.51 亿元
• 净利润：4360 万元
• 未来三年预计增长：20%/年

【资产状况】
• 总资产：3.78 亿元
• 净资产：1.96 亿元""",
        "valuation": """【估值】
另议

【并购意向】
现拟被并购""",
        "highlights": "新能源软件龙头对标 | 高增长 | 拟被并购",
        "status": "在售",
        "created_at": "2026-03-01",
        "buyer_requirements": "",
        "buyer_profile": "",
        "buyer_budget": "",
        "buyer_synergy": ""
    }
]

# ======================
# 数据操作函数
# ======================

def init_sample_data():
    """初始化示例项目数据"""
    if not PROJECTS_FILE.exists():
        df = pd.DataFrame(SAMPLE_PROJECTS)
        df.to_csv(PROJECTS_FILE, index=False, encoding="utf-8-sig")
        return df
    return load_projects()


def load_projects() -> pd.DataFrame:
    """加载项目数据"""
    if not PROJECTS_FILE.exists():
        init_sample_data()

    df = pd.read_csv(PROJECTS_FILE, encoding="utf-8-sig")

    # 确保字段存在
    for col in ["project_type", "buyer_requirements", "buyer_profile", "buyer_budget", "buyer_synergy"]:
        if col not in df.columns:
            df[col] = ""

    return df


def get_project_by_id(project_id: str) -> dict:
    """根据ID获取项目详情"""
    df = load_projects()
    project = df[df["id"] == project_id]
    if len(project) == 0:
        return None
    return project.iloc[0].to_dict()


def search_projects(
    keyword: str = "",
    industry: str = "",
    region: str = "",
    phase: str = "",
    status: str = "在售",
    project_type: str = ""
) -> pd.DataFrame:
    """搜索项目"""
    df = load_projects()

    # 应用筛选条件
    if keyword:
        mask = (
            df["name"].str.contains(keyword, case=False, na=False) |
            df["company_intro"].str.contains(keyword, case=False, na=False) |
            df["highlights"].str.contains(keyword, case=False, na=False) |
            df["buyer_requirements"].str.contains(keyword, case=False, na=False) |
            df["buyer_profile"].str.contains(keyword, case=False, na=False)
        )
        df = df[mask]

    if industry:
        df = df[df["industry"] == industry]

    if region:
        df = df[df["region"] == region]

    if phase:
        df = df[df["phase"] == phase]

    if status:
        df = df[df["status"] == status]

    if project_type:
        df = df[df["project_type"] == project_type]

    return df


def get_filter_options() -> dict:
    """获取筛选选项"""
    df = load_projects()

    return {
        "industries": sorted(df["industry"].dropna().unique().tolist()),
        "regions": sorted(df["region"].dropna().unique().tolist()),
        "phases": sorted(df["phase"].dropna().unique().tolist()),
        "statuses": sorted(df["status"].dropna().unique().tolist()),
        "project_types": ["卖方", "买方"],
    }


def add_project(project_data: dict) -> bool:
    """添加新项目"""
    try:
        df = load_projects()

        # 生成新ID
        new_id = f"MNA-{datetime.now().strftime('%Y%m%d')}-{len(df) + 1:03d}"
        project_data["id"] = new_id
        project_data["created_at"] = datetime.now().strftime("%Y-%m-%d")
        project_data["status"] = "在售"

        # 追加到DataFrame
        new_df = pd.DataFrame([project_data])
        df = pd.concat([df, new_df], ignore_index=True)

        # 保存
        df.to_csv(PROJECTS_FILE, index=False, encoding="utf-8-sig")
        return True
    except Exception as e:
        print(f"添加项目失败: {e}")
        return False


def update_project(project_id: str, project_data: dict) -> bool:
    """更新项目"""
    try:
        df = load_projects()
        idx = df[df["id"] == project_id].index
        if len(idx) == 0:
            return False

        for key, value in project_data.items():
            df.loc[idx, key] = value

        df.to_csv(PROJECTS_FILE, index=False, encoding="utf-8-sig")
        return True
    except Exception as e:
        print(f"更新项目失败: {e}")
        return False


def delete_project(project_id: str) -> bool:
    """删除项目"""
    try:
        df = load_projects()
        df = df[df["id"] != project_id]
        df.to_csv(PROJECTS_FILE, index=False, encoding="utf-8-sig")
        return True
    except Exception as e:
        print(f"删除项目失败: {e}")
        return False
