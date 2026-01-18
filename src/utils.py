import os
import base64
from PIL import Image
from io import BytesIO
# 关键：注册 HEIC 打开器
from pillow_heif import register_heif_opener

# 只要导入这个模块，就会自动注册
register_heif_opener()

def load_image_converted(image_path):
    """
    读取图片（支持 HEIC/JPG/PNG），并统一转换为 RGB 模式的 PIL Image 对象。
    解决 HEIC 兼容性问题。
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"❌ 找不到图片: {image_path}")

    # Pillow 现在可以打开 HEIC 了
    img = Image.open(image_path)
    
    # 如果是 RGBA (透明底) 或 HEIC 的特殊模式，转为 RGB 标准模式
    if img.mode not in ('RGB', 'L'):
        img = img.convert('RGB')
        
    return img

def image_to_base64_str(image_path):
    """
    读取任意格式图片 (HEIC/JPG)，转为标准的 PNG Base64 字符串。
    给 Nanobanana/SD API 用这个最稳，因为 API 可能不懂 HEIC。
    """
    # 1. 先用 PIL 打开并转为 RGB
    img = load_image_converted(image_path)
    
    # 2. 在内存中存为 PNG 格式
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    
    # 3. 转 Base64
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

import os
from PIL import Image
# 引入 HEIC 支持库
from pillow_heif import register_heif_opener

# ✅ 关键：一被导入就自动注册 HEIC 打开器
register_heif_opener()

def load_image_safe(image_path):
    """
    安全读取图片，支持 JPG/PNG/HEIC 等格式。
    返回标准的 PIL Image 对象。
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"❌ 找不到图片: {image_path}")
    
    # 因为上面注册了 opener，这里直接 open 就能读 HEIC 了
    img = Image.open(image_path)
    
    # 确保图片模式兼容 (避免某些 PNG/HEIC 的特殊模式导致 AI 报错)
    if img.mode != 'RGB':
        img = img.convert('RGB')
        
    return img