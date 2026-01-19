# 🎨 AI Wallpaper Agent

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square)
![Google GenAI](https://img.shields.io/badge/Powered%20by-Gemini%202.5-4285F4?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)

[中文介绍](#-中文介绍) | [English](#-english)

</div>

---

## 🇨🇳 中文介绍

**Gemini Wallpaper Agent** 是一个基于 **Google Gemini 2.5 全栈技术** 的智能壁纸生成 Agent。

它不是简单的“滤镜”或随机生图工具，而是一个拥有 **“审美判断力”** 的 AI 艺术总监。它能深度理解你的照片内容，智能推荐最匹配的艺术风格，并根据风格特点自动调整“重绘幅度”，生成既保留原图神韵又极具艺术感的壁纸。

### 💡 核心创新点 (Key Innovations)

本项目探索了多模态大模型 (Multimodal LLM) 在艺术创作中的新范式：

1.  **🧠 双脑协同架构 (Dual-Brain Architecture)**
    * **分析脑 (Analyzer)**：使用 `Gemini 2.5 Flash` 进行视觉推理。它不只识别物体，还能分析构图、光影和情绪。
    * **执行手 (Generator)**：使用 `Gemini 2.5 Flash Image` 进行多模态生成。直接接受“原图+文本”输入，实现高保真的图生图。

2.  **🎚 动态创造力控制 (Dynamic Creativity Control)**
    * 这是本项目的最大亮点。Agent 摒弃了传统的固定参数（如 Stable Diffusion 的 `denoising_strength`），而是由 Analyzer 根据风格特性**自动决策**：
    * **低创造力 (Low)**：针对写实/证件照风格，Agent 会生成严格的 Prompt 约束，确保人物面部和构图不变。
    * **高创造力 (High)**：针对印象派/抽象风格，Agent 会下达“允许重构”的指令，让画面更具张力。

3.  **🍎 原生 HEIC 支持与智能归档**
    * 专为 iPhone 用户优化，底层无感处理 HEIC 格式。
    * 生成的图片会自动按“原文件名”创建专属文件夹归档，彻底告别混乱的 Output 目录。


### ✨ 功能特性

* **智能风格推荐 (Top-K)**：根据图片内容，从风格库中自动挑选最合适的 3-5 种风格。
* **全链路 Google 原生**：无需本地显卡，无需部署 Stable Diffusion，利用 Gemini 强大的多模态能力。
* **高度可扩展**：只需在 YAML 配置文件中添加一行，即可扩展新的艺术风格。

### 🚀 快速开始

1.  **克隆项目**
    ```bash
    git clone [https://github.com/mayuhao-213/wallpaper-agent.git](https://github.com/mayuhao-213/wallpaper-agent.git)
    cd gemini-wallpaper-agent
    ```

2.  **安装依赖**
    ```bash
    pip install -r requirements.txt
    ```

3.  **配置环境**
    在根目录下新建 `.env` 文件，填入你的 Google API Key：
    ```bash
    GOOGLE_API_KEY=你的_google_ai_studio_key
    ```
    *(前往 [Google AI Studio](https://aistudio.google.com/) 免费获取)*

4.  **运行**
    把照片（支持 HEIC/JPG/PNG）放入 `assets/raw/` 目录。
    ```bash
    # 基础运行 (默认生成 3 张推荐风格)
    python main.py --input assets/raw/photo.HEIC

    # 指定生成 5 种推荐风格
    python main.py --input assets/raw/photo.HEIC --top_k 5
    ```

### 📂 输出示例
生成的壁纸会自动按原文件名归档：
```text
assets/
├── inputs/
│   └── cat.HEIC
└── outputs/
    └── cat/  <-- 自动创建同名文件夹
        ├── cat_gen_ghibli_pure_1730001.jpg
        ├── cat_gen_pixar_3d_1730002.jpg
        └── ...


```
## 🎬 动态壁纸功能 (New!)
项目现已集成 **Motion Director** 模块，可将静态生成的艺术图转化为高品质动态壁纸：
- **智能剧本分析**：利用 `gemini-3-flash-preview` 深度理解画面风格与叙事逻辑，设计“有故事感”的微动脚本。
- **Veo 3.1 视频合成**：调用 Google 最先进的视频模型，实现基于原图的 1080p 电影级动态渲染。
- **风格适配动态**：针对不同媒介（如油画、动漫、3D）定制不同的物理运动规律。
---

## 🌏 English

**Gemini Wallpaper Agent** is an intelligent image generation pipeline powered by the **Google Gemini 2.5** stack.

Unlike traditional filters, this agent acts as an **AI Art Director**. It understands the semantic content of your photos, recommends the best-fitting art styles, and intelligently redraws them while preserving the original composition.

### 💡 Key Innovations

1. **Dual-Model Architecture**
* **Analyzer (Brain)**: Uses `Gemini 2.5 Flash` for visual reasoning to understand composition and mood.
* **Generator (Hand)**: Uses `Gemini 2.5 Flash Image` for high-fidelity Image-to-Image generation using multimodal inputs.


2. **Dynamic Creativity Control**
* Instead of manual parameter tuning (like `denoising_strength` in SD), the Agent **automatically decides** the transformation level based on the chosen style:
* **Low Creativity**: For realistic styles, strictly enforcing original structure.
* **High Creativity**: For artistic/abstract styles, allowing significant reimaging of the composition.


3. **Native HEIC Support & Smart Archiving**
* Seamlessly handles iPhone HEIC photos.
* Automatically organizes outputs into dedicated folders based on the source filename.



### 🚀 Quick Start

1. **Installation**
```bash
git clone [https://github.com/your-username/gemini-wallpaper-agent.git](https://github.com/your-username/gemini-wallpaper-agent.git)
pip install -r requirements.txt

```


2. **Configuration**
Create a `.env` file:
```bash
GOOGLE_API_KEY=your_google_key_here

```


3. **Usage**
```bash
python main.py --input assets/raw/photo.HEIC

```



---

## 🧩 Project Structure

* **`src/analyzer.py`**: The Brain. Analyzes images and determines the "Creativity Strategy".
* **`src/generator.py`**: The Artist. Handles Multimodal (Image+Text) generation.
* **`src/prompt_mixer.py`**: The Palette. Blends dynamic descriptions with style templates.
* **`config/styles.yaml`**: The Library. Configurable art styles and prompts.

## 🤝 Contributing

Pull requests are welcome! You can easily add new styles to `config/styles.yaml`.

## 👤 Author & Contact / 作者与联系方式

**Created by [Myh]**

如果你喜欢这个项目，或者有任何想法、合作意向，欢迎随时联系我！  
If you like this project, or have any ideas/collaboration requests, feel free to reach out!

* 📧 **Email**: `yuhao.ma.213 [at] outlook [dot] com`
* 💬 **WeChat**: `18646593213`


