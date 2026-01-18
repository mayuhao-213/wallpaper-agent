import os
import json
import yaml
from google import genai
from dotenv import load_dotenv
from src.utils import load_image_safe 

load_dotenv()

class ImageAnalyzer:
    def __init__(self, styles_config_path="config/styles.yaml"):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key: raise ValueError("❌ 未找到 GOOGLE_API_KEY")
        self.client = genai.Client(api_key=api_key)
        self.model_name = "gemini-2.5-flash" 
        
        # 读取配置
        if not os.path.exists(styles_config_path):
             raise FileNotFoundError(f"❌ 找不到配置: {styles_config_path}")
        with open(styles_config_path, 'r', encoding='utf-8') as f:
            self.full_config = yaml.safe_load(f)
            self.style_menu = {k: v['name'] for k, v in self.full_config.get('styles', {}).items()}

    def analyze_and_recommend(self, image_path, top_k=3):
        print(f"🧠 [Analyzer] Gemini 2.5 正在分析图片与规划重绘策略...")
        try:
            img = load_image_safe(image_path)
            
            # 🔥 升级版 Prompt：要求返回 creativity_level
            prompt = f"""
            Act as an expert AI Art Director. 
            Styles Library: {json.dumps(self.style_menu, ensure_ascii=False)}
            
            Task:
            1. Recommend TOP {top_k} styles for this image.
            2. For EACH style, determine the optimal "Creativity Level" (how much to deviate from the original image):
               - "High": For abstract/artistic styles (e.g., Cubism, Impressionism). Change structure freely.
               - "Medium": For illustrative styles (e.g., Anime, 3D). Keep composition, change textures.
               - "Low": For realistic styles. Keep strict structure, only change lighting/color.
            3. Write a visual description.

            Output JSON:
            {{
                "description": "...",
                "recommendations": [
                    {{ "style_key": "style1", "creativity": "High" }},
                    {{ "style_key": "style2", "creativity": "Low" }}
                ],
                "reasoning": "..."
            }}
            """

            response = self.client.models.generate_content(
                model=self.model_name,
                contents=[img, prompt],
                config={"response_mime_type": "application/json"}
            )
            
            result = json.loads(response.text)
            print(f"✅ [推荐] 方案已生成")
            return result

        except Exception as e:
            print(f"❌ [异常] 分析失败: {e}")
            # 保底返回
            return {
                "description": "A nice photo",
                "recommendations": [{"style_key": k, "creativity": "Medium"} for k in list(self.style_menu.keys())[:top_k]]
            }