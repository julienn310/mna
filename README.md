# M&A 并购重组项目信息交流平台

> 基于 Streamlit 的并购重组项目信息交流 MVP，支持卖方项目展示和买方需求发布。

## 🚀 快速启动（本地）

```bash
# 1. 克隆项目
git clone <your-repo-url>
cd 并购重组

# 2. 安装依赖
pip install -r requirements.txt

# 3. 启动
streamlit run app.py
```

## 🌐 部署到 Streamlit Cloud

1. 将代码推送到 GitHub
2. 访问 [share.streamlit.io](https://share.streamlit.io)
3. 选择你的 GitHub 仓库
4. 设置：`app.py` 作为主入口
5. 点击 Deploy

## 🔐 默认账户

| 用户名 | 密码 | 角色 |
|--------|------|------|
| `admin` | `admin123` | 管理员 |

> ⚠️ **正式发布前请修改默认密码！**

## 📁 项目结构

```
├── app.py                    # 主入口
├── pages/                    # 多页面
│   ├── projects_list.py      # 项目列表
│   ├── project_detail.py     # 项目详情
│   ├── search.py             # 搜索中心
│   ├── user_center.py        # 用户中心
│   └── admin_center.py       # 管理员后台
├── modules/                   # 核心模块
│   ├── auth.py               # 用户认证
│   └── data_manager.py       # 数据管理
├── data/                      # 数据存储
│   ├── projects.csv          # 项目数据
│   └── users.yaml            # 用户数据
├── requirements.txt          # 依赖
└── README.md
```

## 📊 功能

- [x] 用户注册 / 登录
- [x] 卖方项目发布（出售股权、被并购等）
- [x] 买方需求发布（收购、可参可控）
- [x] 项目列表浏览（支持类型/行业/地区筛选）
- [x] 项目详情展示
- [x] 关键词搜索
- [x] 管理员后台（发布/编辑/删除项目）
- [x] 用户管理

## 🔄 Streamlit Cloud 注意事项

1. **数据持久化**：Streamlit Cloud 免费版使用 Ephemeral 存储，重启后会重置数据
2. **如需持久化**：可连接 PostgreSQL / MySQL 数据库
3. **多用户**：当前为简化的单文件认证，生产环境建议接入 OAuth

## 📝 许可证

MIT License
