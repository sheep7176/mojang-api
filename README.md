# Minecraft UUID & 皮肤查询工具 🎮

通过用户名快速查询 Minecraft 玩家的 UUID、皮肤和披风，并支持一键下载皮肤/披风图片到本地。

## ✨ 功能特性

- 🔍 **精确查询**：通过用户名查询玩家 UUID 及皮肤/披风信息。
- 🎨 **模型识别**：自动识别皮肤模型（Steve / Alex）及历史时间戳。
- 🖼️ **格式自适应**：自动识别图片真实格式（PNG / GIF / JPG），保存时使用正确的扩展名。
- ⬇️ **便捷下载**：支持通过简单的控制台交互下载皮肤和披风。
- 🌍 **多语言支持（i18n）**：代码与文本分离，所有提示语存于 `language/*` 中，方便未来扩展其他语言。
- 🛡️ **健壮性**：完善的错误捕获（404、429、500 等 HTTP 状态码）及语言文件缺失容错。

## 📦 环境要求

- Python 3.6 或更高版本
- 依赖库：`requests`

## 🔧 安装指南

1. **克隆仓库**：
   ```bash
   git clone https://github.com/sheep7176/mojang-api.git
   cd mojang-api
   ```
   *或者*
   ```bash
   git clone https://gitee.com/sheep7176/mojang-api.git
   ```

2. **安装依赖**：
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 使用方法

在命令行中运行主程序：

```bash
python main.py
# 或者如果你在 Windows 下且有多个 Python 版本：
py main.py
```

**操作流程**：

1. 根据提示输入 Minecraft 用户名（例如 `jeb_` 或 `Notch`）。
2. 程序将展示 UUID、皮肤链接、披风链接和模型类型。
3. 输入 `y` 或 `n` 决定是否下载对应的皮肤/披风图片。

## 📁 项目结构

```text
.
├── main.py                  # 核心代码：API 请求、数据解析与下载
├── requirements.txt         # 依赖列表
├── README.md                # 本文件
├── .gitignore               # Git 忽略规则
└── language/                # 语言包目录 (i18n)
    └── zh_cn.json           # 简体中文语言文件
```

## ⚠️ 注意事项

- **文件保存位置**：下载的皮肤/披风图片默认保存在与 `main.py` 同级的目录下。同名文件会被直接覆盖，请注意备份。
- **API 速率限制**：Mojang 公开 API 有调用频率限制，请勿在短时间内高频请求，避免触发 `429 Too Many Requests`。
- **语言文件**：请确保 `language` 文件夹与 `main.py` 处于同一层级，否则程序会提示“找不到语言文件”。

## 📄 许可证

本项目采用 [MIT License](LICENSE) 许可协议。你可以自由使用、修改和分发，但请保留原作者信息。

---

如果这个工具帮到了你，欢迎在右上角点个 ⭐ **Star** 支持一下 AWA

*注:本工具除了此[README.md](README.md)并未使用AI生成*