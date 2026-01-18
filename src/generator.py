import os
import time
import json
import base64
import requests
from google import genai
from google.genai import types
from dotenv import load_dotenv
from src.utils import load_image_safe
load_dotenv()

class ImageGenerator:
    def __init__(self):
        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        self.sd_api_url = os.getenv("SD_API_URL") 
        
        if self.google_api_key:
            self.client = genai.Client(api_key=self.google_api_key)
            self.imagen_model = "imagen-4.0-generate-001" 
            self.vision_model = "gemini-2.5-flash-image"

    def generate(self, image_path, prompt_data):
        """
        智能选择绘图引擎：默认使用 Google Imagen 4
        生成的图片将保存在与输入图片相同的目录下，文件名包含原文件名。
        """
        style_name = prompt_data.get('style_name', 'Unknown')
        style_key = prompt_data.get('style_key', 'unknown_style')
        # 构造完整的 Prompt
        full_prompt = f"{prompt_data['prompt']} --no {prompt_data.get('negative_prompt', 'text, watermark')}"
        
        print(f"🎨 [Generator] 启动 Imagen 4 绘制: {style_name}")
        
        try:
            # 调用 Google Imagen 4
            response = self.client.models.generate_images(
                model=self.imagen_model,
                prompt=full_prompt,
                config=types.GenerateImagesConfig(
                    number_of_images=1,
                    aspect_ratio="3:4", 
                    safety_filter_level="block_low_and_above", # 必须是 block_low_and_above
                    person_generation="allow_adult"
                )
            )

            if response.generated_images:
                image_bytes = response.generated_images[0].image.image_bytes
                
                # --- 核心修改：动态计算输出路径 ---
                # 1. 获取原图所在的目录 (例如 assets/inputs/2Dog)
                input_dir = os.path.dirname(image_path)
                # 如果是直接传文件名，dirname可能是空的，设为当前目录
                if not input_dir: 
                    input_dir = "."
                base_output_dir = input_dir.replace("inputs", "outputs")

                # 2. 获取原文件名 (不带后缀，例如 2Dog_2)
                base_name = os.path.splitext(os.path.basename(image_path))[0]
                output_dir = os.path.join(base_output_dir, base_name)
                os.makedirs(output_dir, exist_ok=True)
                # 3. 拼接新文件名: 原名_gen_风格_时间戳.png
                timestamp = int(time.time())

                new_filename = f"{base_name}_gen_{style_key}_{timestamp}.png"
                save_path = os.path.join(output_dir, new_filename)
                
                # -------------------------------
                
                # 保存文件
                with open(save_path, "wb") as f:
                    f.write(image_bytes)
                
                print(f"✅ [成功] 壁纸已保存: {save_path}")
                return save_path
            else:
                print("❌ [失败] Imagen 模型未返回图片")
                return None

        except Exception as e:
            print(f"❌ [异常] Google 绘图失败: {e}")
            if hasattr(e, 'message'):
                print(f"   详情: {e.message}")
            return None

    def generate_with_ref_image(self, image_path, prompt_data):
        style_name = prompt_data.get('style_name', 'Unknown')
        style_key = prompt_data.get('style_key', 'unknown_style')
        # 🔥 获取 Analyzer 决定的创造力等级 (默认为 Medium)
        creativity = prompt_data.get('creativity', 'Medium') 
        
        print(f"📥 [Gemini Vision] 读取参考图: {os.path.basename(image_path)}")
        try:
            ref_image = load_image_safe(image_path)
        except Exception as e:
            print(f"❌ 图片加载失败: {e}")
            return None

        # 🔥 核心：动态构建指令 (模拟 Denoising Strength)
        if creativity == "Low":
            instruction = "STRICTLY maintain the original image's structure, pose, and geometry. Only change the lighting and art style texture. Do not add or remove objects."
        elif creativity == "High":
            instruction = "Use the original image only as a loose reference for color and vibe. Feel free to reimagine the composition and pose to better fit the artistic style. Be creative!"
        else: # Medium
            instruction = "Maintain the main subject's pose and overall composition, but feel free to stylize the background and details to match the art style."

        full_prompt = f"""
        Generate a wallpaper image.
        
        Style Target: {style_name}
        Visual Description: {prompt_data['prompt']}
        
        Constraint Level: {creativity}
        Instructions: {instruction}
        
        Negative Prompt: {prompt_data.get('negative_prompt', 'low quality')}
        """
        
        print(f"🎨 [Gemini] 绘制: {style_name} (重绘策略: {creativity})")

        try:
            # 去掉 mime_type 限制，让模型自由发挥
            response = self.client.models.generate_content(
                model=self.vision_model,
                contents=[ref_image, full_prompt]
            )
            return self._save_response_image(response, image_path, style_key, extension=".jpg")

        except Exception as e:
            print(f"❌ [失败] {e}")
            return None

    def _save_response_image(self, response, original_image_path, style_key, engine_tag):
        """
        统一的保存逻辑：Input目录 -> Output目录
        """
        image_bytes = None

        # 解析 Imagen 格式
        if hasattr(response, 'generated_images') and response.generated_images:
            image_bytes = response.generated_images[0].image.image_bytes
        # 解析 Gemini 多模态格式 (inline_data)
        elif hasattr(response, 'candidates') and response.candidates:
            for part in response.candidates[0].content.parts:
                if part.inline_data:
                    image_bytes = part.inline_data.data
                    break
        
        if not image_bytes:
            print("❌ 未获取到图片数据")
            return None

        # --- 路径计算 (Inputs -> Outputs) ---
        file_stem = os.path.splitext(os.path.basename(original_image_path))[0]
        input_dir = os.path.dirname(original_image_path)
        base_output_path = input_dir.replace("inputs", "outputs")
        final_output_dir = os.path.join(base_output_path, file_stem)
        
        os.makedirs(final_output_dir, exist_ok=True)
        
        timestamp = int(time.time())
        new_filename = f"{file_stem}_gen_{style_key}_{timestamp}.png"
        save_path = os.path.join(final_output_dir, new_filename)
        # -----------------------------------

        with open(save_path, "wb") as f:
            f.write(image_bytes)
        
        print(f"✅ [成功] 已保存: {save_path}")
        return save_path