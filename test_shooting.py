from src.motion_director import MotionDirector
import os
from dotenv import load_dotenv
# 加载环境变量 (API Key)
load_dotenv()
def test_full_workflow():
    director = MotionDirector()
    
    # 指向你想要测试的图片
    target_img = "assets/outputs/Dog/Dog_gen_monet_impressionism_1768752448.png"
    
    if not os.path.exists(target_img):
        print("❌ 找不到测试图，请检查路径。")
        return

    # 步骤 1: 视觉分析生成剧本
    script_info = director.create_motion_script(target_img)
    print(f"📜 剧本已生成: {script_info['video_prompt']}")

    # 步骤 2: 开机生成视频
    video_path = director.generate_video(target_img, script_info['video_prompt'])
    
    if video_path:
        print(f"🎉 测试成功！请打开 {video_path} 检查狗狗是否在‘互动’。")

if __name__ == "__main__":
    test_full_workflow()