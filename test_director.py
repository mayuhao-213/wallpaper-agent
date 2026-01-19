import os
from dotenv import load_dotenv
from src.motion_director import MotionDirector

# 加载环境变量 (API Key)
load_dotenv()

def test_motion_analysis():
    # 1. 初始化导演
    director = MotionDirector()
    
    # 2. 准备测试用例 (请确保你的 assets/outputs/ 目录下有这些文件，或者修改为实际存在的路径)
    test_images = [
        # 案例 A
        "assets/outputs/Dog/Dog_gen_makoto_shinkai_1768752426.png",
        # 案例 B
        "assets/outputs/italy/italy_gen_cyberpunk_neon_1768751243.png",
        
        # 案例 C: 现代科技感 (验证霓虹闪烁和故障感)
        "assets/outputs/bird/bird_gen_new_chinese_ink_1768549683.png"
    ]
    
    print("🚀 开始动态壁纸剧本分析测试...\n")
    print("-" * 50)

    for img_path in test_images:
        if not os.path.exists(img_path):
            print(f"⚠️ 跳过测试: 找不到文件 {img_path}")
            continue
            
        # 执行分析工作流
        result = director.create_motion_script(img_path)
        
        print(f"📁 文件: {os.path.basename(result['source_image'])}")
        print(f"🎨 识别风格: {result['style_detected']}")
        print(f"🎬 生成脚本: \n   \"{result['video_prompt']}\"")
        print("-" * 50)

if __name__ == "__main__":
    test_motion_analysis()