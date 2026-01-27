from pathlib import Path
from typing import Optional


class PromptLoader:
    
    def __init__(self, prompts_path: Optional[str] = None, version: str = "v1"):
        backend_dir = Path(__file__).parent.parent.parent.resolve()
        if prompts_path and prompts_path.strip():
            path_obj = Path(prompts_path)
            self.prompts_dir = path_obj if path_obj.is_absolute() else backend_dir / prompts_path
        else:
            self.prompts_dir = backend_dir / "application" / "services" / "prompts"
        self.version = version
    
    def load_template(self, template_name: str, version: Optional[str] = None) -> str:
        version = version or self.version
        template_file = self.prompts_dir / f"{template_name}_{version}.txt"
        
        if not template_file.exists():
            if version != 'v1':
                template_file = self.prompts_dir / f"{template_name}_v1.txt"
            if not template_file.exists():
                raise FileNotFoundError(f"Template not found: {template_name}_{version}.txt")
        
        return template_file.read_text(encoding='utf-8')
    
    def render_template(self, template_name: str, **kwargs) -> str:
        template = self.load_template(template_name)
        return template.format(**kwargs)
