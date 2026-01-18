import yaml
import os

class PromptMixer:
    def __init__(self, config_path="config/styles.yaml"):
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"❌ 找不到配置文件: {config_path}")
            
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
            self.styles = self.config.get('styles', {})

    def mix_prompt(self, style_key, image_description):
        """
        核心逻辑：将 'Gemini的描述' 注入 '风格模板'
        """
        if style_key not in self.styles:
            print(f"⚠️ 警告: 风格 '{style_key}' 不存在，回退到默认风格。")
            # 如果找不到，就找一个存在的，或者直接返回描述
            style_key = list(self.styles.keys())[0] if self.styles else None
            
        style_data = self.styles.get(style_key, {})
        style_name = style_data.get('name', style_key)
        template = style_data.get('prompt_template', '{description}')
        
        # 1. 填空：把 Gemini 的描述填入 {description}
        if "{description}" in template:
            final_prompt = template.format(description=image_description)
        else:
            final_prompt = f"{template}, {image_description}"
            
        # 2. 获取负向提示词 (Imagen 会用到 --no 参数)
        negative_prompt = style_data.get('negative_prompt', '')
        
        return {
            "style_name": style_name,
            "style_key": style_key,
            "prompt": final_prompt,
            "negative_prompt": negative_prompt
        }