# 🎨 Gemini AI Wallpaper Agent

> A fully automated, intelligent wallpaper generator powered by **Google Gemini 2.5**. 
> It analyzes your photos, recommends suitable art styles, and intelligently redraws them using visual comprehension.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Google GenAI](https://img.shields.io/badge/Powered%20by-Google%20GenAI-4285F4)
![License](https://img.shields.io/badge/license-MIT-green)

## ✨ Features

Unlike traditional "filters" or random generation, this agent acts like a professional **Art Director**:

* **🧠 Intelligent Analysis (Brain)**: Uses `Gemini 2.5 Flash` to analyze image composition, subject, and lighting.
* **🎯 Top-K Recommendations**: Automatically selects the best 3-5 art styles (e.g., Ghibli, Pixar, Cyberpunk) from a curated library based on the image content.
* **🎚 Dynamic Creativity Control**: The agent decides the "Denoising Strength" (Creativity Level) automatically:
    * *Low:* For realistic styles (keeps strict structure).
    * *High:* For abstract styles (reimagines the composition).
* **🖼️ Visual Generation (Vision)**: Uses `Gemini 2.5 Flash Image` (Multimodal) for high-fidelity Image-to-Image generation.
* **🍎 Full Compatibility**: Native support for **HEIC** (iPhone photos), JPG, and PNG.
* **📂 Smart Archiving**: Automatically organizes outputs into folders named after the source file.

---

## 🛠️ Installation

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/your-username/gemini-wallpaper-agent.git](https://github.com/your-username/gemini-wallpaper-agent.git)
    cd gemini-wallpaper-agent
    ```

2.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Setup Configuration**
    Create a `.env` file in the root directory and add your Google API Key:
    ```bash
    GOOGLE_API_KEY=your_google_ai_studio_key_here
    ```
    *(Get your key from [Google AI Studio](https://aistudio.google.com/))*

---

## 🚀 Usage

Put your photos (HEIC/JPG) into the `assets/raw/` folder (or any path you like).

**Basic Run:**
```bash
python main.py --input assets/raw/my_photo.HEIC

```

**Generate Top 5 Recommendations:**

```bash
python main.py --input assets/raw/my_photo.HEIC --top_k 5

```

### Output Structure

The generated wallpapers are saved in `assets/outputs/`, organized by the input filename:

```text
assets/
├── inputs/
│   └── cat.HEIC
└── outputs/
    └── cat/
        ├── cat_Google_ghibli_pure_1730001.jpg
        ├── cat_Google_pixar_3d_1730002.jpg
        └── ...

```

---

## 🧩 Project Structure

* **`src/analyzer.py`**: The Brain. Calls Gemini to analyze the image and decide the "Creativity Level".
* **`src/generator.py`**: The Artist. Calls Gemini Vision model to generate the image using the prompt and reference image.
* **`src/prompt_mixer.py`**: Blends the dynamic description with pre-defined style templates.
* **`src/utils.py`**: Handles HEIC conversion and image loading safety.
* **`config/styles.yaml`**: The library of art styles and prompts.

---

## 🎨 Customizing Styles

You can add your own art styles in `config/styles.yaml`.
Example:

```yaml
styles:
  my_new_style:
    name: "Cyberpunk Neon"
    prompt_template: "cyberpunk city style, neon lights, rainy street, {description}"
    negative_prompt: "daylight, dull colors"

```

---

## 🤝 Contributing

Pull requests are welcome! Feel free to add more styles to the YAML or improve the prompt engineering logic.

## 📄 License

MIT

