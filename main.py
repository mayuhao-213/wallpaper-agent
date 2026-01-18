import argparse
import os
import time
from src.utils import load_image_safe 
from src.analyzer import ImageAnalyzer
from src.prompt_mixer import PromptMixer
from src.generator import ImageGenerator

def main():
    # 1. 命令行参数设置
    parser = argparse.ArgumentParser(description="AI Wallpaper Agent (Google Powered)")
    parser.add_argument("--input", required=True, help="输入图片路径 (支持 HEIC/JPG/PNG)")
    parser.add_argument("--top_k", type=int, default=3, help="生成几种推荐风格 (默认: 3)")
    args = parser.parse_args()

    # 检查输入文件是否存在
    if not os.path.exists(args.input):
        print(f"❌ 错误: 找不到输入图片 '{args.input}'")
        return

    print("\n🚀 === 启动 AI 壁纸生成 Agent (Google Gemini 2.5 全栈) ===\n")

    try:
        # 2. 初始化核心模块
        analyzer = ImageAnalyzer() 
        mixer = PromptMixer()
        generator = ImageGenerator()
        
    except Exception as e:
        print(f"❌ 初始化失败: {e}")
        print("💡 提示: 请检查 .env 文件配置是否正确")
        return

    # ---------------------------------------------------------
    # Step 1: 视觉分析 (Visual Analysis)
    # ---------------------------------------------------------
    start_time = time.time()
    
    # 获取 Gemini 的分析结果
    analysis_result = analyzer.analyze_and_recommend(args.input, top_k=args.top_k)
    
    description = analysis_result.get('description', '')
    # ✅ 适配新结构: 获取 'recommendations' 列表 (里面包含 style_key 和 creativity)
    recommendations = analysis_result.get('recommendations', [])
    reasoning = analysis_result.get('reasoning', '无')

    print(f"\n📋 [分析报告]")
    print(f"   - 图片描述: {description[:60]}...")
    print(f"   - 推荐方案: {len(recommendations)} 种")
    print(f"   - 整体思路: {reasoning}")
    print("-" * 50)

    if not recommendations:
        print("⚠️ 未能获取推荐风格，程序终止。")
        return

    # ---------------------------------------------------------
    # Step 2: 批量绘图 (Batch Generation)
    # ---------------------------------------------------------
    print(f"\n🎨 开始生成 {len(recommendations)} 张壁纸...\n")

    generated_files = []

    # ✅ 适配新循环: 遍历字典列表
    for i, item in enumerate(recommendations, 1):
        # 从字典中提取 key 和 creativity
        style_key = item.get('style_key')
        creativity = item.get('creativity', 'Medium') # 默认中等
        
        print(f"[{i}/{len(recommendations)}] 正在处理: {style_key} (策略: {creativity}) ...")
        
        try:
            # A. 组装 Prompt (混合风格模板 + 描述)
            prompt_data = mixer.mix_prompt(style_key, description)
            
            # ✅ 关键点: 将 analyzer 决定的 creativity 塞入 prompt_data
            # 这样 generator 里的 generate_with_ref_image 就能读到了
            prompt_data['creativity'] = creativity
            
            # B. 调用 Gemini Vision 生成 (原图 + 文本 + 策略)
            save_path = generator.generate_with_ref_image(args.input, prompt_data)
            
            if save_path:
                generated_files.append(save_path)
            
        except Exception as e:
            print(f"   ⚠️ 风格 {style_key} 生成出错: {e}")

    # ---------------------------------------------------------
    # Step 3: 总结 (Summary)
    # ---------------------------------------------------------
    duration = time.time() - start_time
    print(f"\n✨ === 全部完成! 耗时: {duration:.2f}s ===")
    
    if generated_files:
        print(f"📂 生成结果保存在 (原图所在目录的 outputs 文件夹):")
        for path in generated_files:
            print(f"   👉 {path}")
    else:
        print("❌ 本次没有生成任何图片。")

if __name__ == "__main__":
    main()