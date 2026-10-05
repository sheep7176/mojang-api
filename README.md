# minecraft UUID查询工具

通过用户名查询 Minecraft 玩家的 UUID、皮肤和披风，并支持下载皮肤/披风图片到本地。

## ✨ 功能

- 通过用户名查询玩家 UUID
- 获取皮肤链接、皮肤模型（Steve / Alex）
- 获取披风链接（如果有）
- 自动识别图片真实格式（PNG / GIF / JPG），保存时使用正确扩展名
- 支持下载皮肤和披风到脚本所在目录
- 控制台交互式操作，简单易用

## 📦 环境

- Python 3.6+
- `requests` 库

## 🔧 安装

1. 克隆仓库：
   ```bash
   git clone https://github.com/sheep7176/mojang-api.git
   cd mojang-api
   ```

2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 使用方法

### 命令行运行

```bash
python main.py
```

按照提示输入 Minecraft 用户名（例如 `jeb_`），程序会显示查询结果，并询问是否下载皮肤/披风图片。

## 📁 项目结构

```
.
├── main.py           # 核心代码：查询、下载
├── requirements.txt  # 依赖列表
├── README.md         # 本文件
└── .gitignore        # Git 忽略规则
```

## ⚠️ 注意事项

- **文件保存位置**：下载的图片默认保存在与 `main.py` 相同的目录下。
- **速率限制**：Mojang 公开 API 有调用频率限制，请勿在短时间内大量请求。

## 📄 许可证

本项目采用 MIT License。你可以自由使用、修改、分发，但请保留原作者信息。

---

如果你觉得这个工具有用，欢迎点个 Star 支持一下AWA！