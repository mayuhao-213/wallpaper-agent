import os
from google import genai
from dotenv import load_dotenv

# 加载 .env 文件中的 key
load_dotenv()

def check_available_models():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ 错误: 未在 .env 中找到 GOOGLE_API_KEY")
        return

    print(f"🔑 使用 API Key: {api_key[:5]}...{api_key[-5:]} 进行连接测试...\n")

    try:
        client = genai.Client(api_key=api_key)
        
        # 获取所有模型列表
        print("📡 正在向 Google 获取模型列表...")
        # config={'page_size': 100} 是为了防止分页太慢，一次取多点
        pager = client.models.list(config={'page_size': 100})
        
        all_models = []
        imagen_models = []
        gemini_models = []

        # 遍历迭代器
        for model in pager:
            name = model.name
            display_name = model.display_name or name
            
            all_models.append(name)
            
            # 分类筛选
            if "imagen" in name.lower():
                imagen_models.append(f"{name} ({display_name})")
            elif "gemini" in name.lower():
                gemini_models.append(f"{name} ({display_name})")

        # --- 打印报告 ---
        print("\n" + "="*40)
        print("🎨 【绘图模型 (Imagen)】")
        print("="*40)
        if imagen_models:
            for m in imagen_models:
                print(f"✅ {m}")
        else:
            print("❌ 未找到 Imagen 模型 (可能需要申请白名单或 Key 权限不足)")

        print("\n" + "="*40)
        print("🧠 【分析模型 (Gemini)】")
        print("="*40)
        if gemini_models:
            # 只打印 flash 和 pro 等常用模型，防止列表太长
            common_gemini = [m for m in gemini_models if "flash" in m or "pro" in m]
            for m in common_gemini:
                print(f"✅ {m}")
            print(f"... 以及其他 {len(gemini_models) - len(common_gemini)} 个 Gemini 变体")
        else:
            print("❌ 未找到 Gemini 模型")

        print("\n" + "="*40)
        print(f"📊 总计发现 {len(all_models)} 个可用模型")
        print("="*40)

    except Exception as e:
        print(f"\n❌ 连接失败: {e}")
        print("建议检查：")
        print("1. 科学上网连接是否正常？")
        print("2. API Key 是否已过期或被撤销？")

if __name__ == "__main__":
    check_available_models()