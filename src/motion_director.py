import os
import re
import yaml
from google import genai
from src.utils import load_image_safe
from google.genai import types
import time
import requests
class MotionDirector:
    def __init__(self, styles_path="config/styles.yaml"):
        """
        初始化动态导演，加载风格库并配置 Google GenAI 客户端
        """
        # 1. 加载重构后的学术化 styles.yaml
        try:
            with open(styles_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                self.styles = config.get('styles', {})
        except Exception as e:
            print(f"⚠️ [Director] 无法加载风格配置文件: {e}")
            self.styles = {}

        # 2. 初始化客户端 (确保环境变量中已配置 GOOGLE_API_KEY)
        api_key = os.getenv("GOOGLE_API_KEY")
        self.api_key = api_key
        if not api_key:
            raise ValueError("❌ GOOGLE_API_KEY 未在环境变量中设置")
        
        self.client = genai.Client(api_key=api_key)
        # 使用最新的 Gemini 3 图像预览模型进行视觉分析
        self.vision_model = "gemini-2.5-flash" 

    def parse_style_from_filename(self, image_path):
        """
        [函数 1] 逆向解析文件名以提取 style_key
        示例: cat_gen_makoto_shinkai_1737244800.png -> makoto_shinkai
        """
        filename = os.path.basename(image_path)
        try:
            if "_gen_" in filename:
                # 提取 _gen_ 之后的部分
                style_part = filename.split("_gen_")[1]
                # 使用正则移除最后的时间戳和后缀 (例如 _1737244800.png)
                style_key = re.sub(r'_\d+\.(png|jpg|heic|JPG|PNG)$', '', style_part)
                return style_key
        except Exception as e:
            print(f"⚠️ [Director] 文件名解析失败: {e}")
        
        return "default"

    def _build_director_prompt(self, style_key):
        style_info = self.styles.get(style_key, {})
        motion_guide = style_info.get('motion_guide', "Subtle and organic motion.")
        
        prompt = f"""
        # Role: Elite Multi-Style AI Motion Director
        
        # Style Logic:
        Respect the medium (Painting/Anime/3D/Photo). Style Principle: {motion_guide}
        
        # Your Core Mission:
        Design a "Living Moment" for a wallpaper. It must have a subtle "Story" behind the motion.
        
        # Motion Strategy (The "10% Rule"):
        1. **Stable World**: Start with "Cinemagraph, Static Camera." The environment is the stage, it must remain steady.
        2. **Purposeful Subject Motion**: If there are characters or animals, they should NOT be frozen. 
           - Allow "Micro-Interactions": Two subjects might glance at each other, a dog might tilt its head curiously, or a bird might preen its feathers.
           - Their movement should be "Slightly Positional": They can move within a small 10% radius of their original spot to create a sense of life and story.
           - Movements must be intentional (e.g., "looking at the horizon") rather than random jitters.
        3. **Artistic Secondary Motion**: 
           - In paintings (e.g. Ink/Van Gogh): Animate the *texture* or *brushstrokes* as if the paint is alive.
           - In nature: Wind and light should complement the subjects' actions.
        4. **Loopability**: All movements must resolve back to the starting pose smoothly for a perfect infinite loop.
        
        # Output Format:
        Provide ONLY the final video prompt in a single English paragraph. Focus on the INTERACTION and the STORY of the micro-movements.
        """
        return prompt
    
    def analyze_scene_for_motion(self, image_path, style_key):
        """
        [函数 3] 调用 Gemini 3 Pro 执行视觉分析并返回 Video Prompt
        """
        print(f"🧠 [Motion Director] 正在分析画面动态 (Style: {style_key})...")
        
        try:
            # 加载本地静态图
            img = load_image_safe(image_path)
            # 生成针对该风格的导演指令
            director_prompt = self._build_director_prompt(style_key)
            
            # 调用 Gemini 进行多模态推理
            response = self.client.models.generate_content(
                model=self.vision_model,
                contents=[img, director_prompt]
            )
            
            video_prompt = response.text.strip()
            print(f"🎬 [Director's Script]: {video_prompt}")
            return video_prompt
            
        except Exception as e:
            print(f"❌ [Director] 分析失败: {e}")
            return "Cinemagraph, Static Camera, subtle ambient motion, high quality, loopable."

    def create_motion_script(self, image_path):
        """
        [工作流] 顶层入口：从图片到视频脚本的转换
        """
        # 1. 识别图片风格
        style_key = self.parse_style_from_filename(image_path)
        
        # 2. 生成专业的运动提示词
        video_prompt = self.analyze_scene_for_motion(image_path, style_key)
        
        return {
            "source_image": image_path,
            "style_detected": style_key,
            "video_prompt": video_prompt
        }


    def generate_video(self, image_path, video_prompt):
        """
        [函数 4] 使用 Veo 3.1 最终修复版：构造符合规范的 Image 类型
        """
        print(f"🎬 [Veo 3.1] 正在开机拍摄... 预计耗时 1-2 分钟")
        
        try:
            # 1. 以二进制模式读取图片
            with open(image_path, "rb") as f:
                image_bytes = f.read()
            # 2. 识别 MIME 类型
            ext = image_path.split('.')[-1].lower()
            mime_type = "image/png" if "png" in ext else "image/jpeg"

            # 3. 构造符合 API 要求的 Image 实例
            input_image = types.Image(
                image_bytes=image_bytes,
                mime_type=mime_type
            )

            # 4. 指定模型 ID
            model_id = "veo-3.1-generate-preview" 

            # 5. 提交任务
            operation = self.client.models.generate_videos(
                model=model_id,
                prompt=video_prompt,
                image=input_image,  # 传入构造好的 Image 对象
                config=types.GenerateVideosConfig(
                    aspect_ratio="16:9",
                    duration_seconds=4
                )
            )

            print(f"⏳ 任务已提交 (ID: {operation.name})，云端渲染中...")

            while not operation.done:
                time.sleep(5)
                operation = self.client.operations.get(operation)
                print(".", end="", flush=True)
            print() 
            
            output_path = image_path.replace(".png", "_raw.mp4")
            if operation.result and operation.result.generated_videos:
                video_result = operation.result.generated_videos[0]
                video_uri = video_result.video.uri
                print(f"🔗 [VideoAgent] 获取到下载链接: {video_uri}...")
                
                response = requests.get(
                    video_uri, 
                    headers={"x-goog-api-key": self.api_key}  # 👈 这就是 403 的解药
                )
                
                if response.status_code == 200:
                    os.makedirs(os.path.dirname(output_path), exist_ok=True)
                    with open(output_path, "wb") as f:
                        f.write(response.content)
                    print(f"✅ [VideoAgent] 视频下载成功: {output_path}")
                    return True
                else:
                    print(f"❌ [VideoAgent] 下载失败，状态码: {response.status_code}")
                    # 打印更多错误信息
                    print(f"   Response: {response.text[:200]}")
                    return False
            else:
                print("❌ [VideoAgent] 生成失败: 未返回视频数据")
                return False


        except Exception as e:
            print(f"❌ [Video Gen] 拍摄失败: {e}")
            return None
    
    
    def post_process_loop(self, video_path):
        """
        [函数 5 - 待实现] 使用 FFmpeg 进行 3s 裁剪与 Crossfade 无缝循环处理
        """
        pass