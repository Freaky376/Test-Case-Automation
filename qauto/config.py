"""
Configuration management for QAUTO
"""
import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional


class Config:
    """Handles loading and managing configuration"""
    
    DEFAULT_CONFIG = {
        'template': {
            'primary': str(Path(__file__).parent.parent / 'actual excel template' / 'Test_Case_Template.xlsx'),
            'fallback': './Test_Case_Template.xlsx'
        },
        'directories': {
            'batches': './batches',
            'output': './output'
        },
        'batch': {
            'size': 4,
            'image_extensions': ['png', 'jpg', 'jpeg']
        },
        'prompt': {
            'custom_template': None
        }
    }
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize config, loading from file if it exists"""
        self.config_path = config_path or self._get_default_config_path()
        self.data = self._load_config()
    
    def _get_default_config_path(self) -> str:
        """Get the default config file path"""
        # Look for config in current directory first, then in script directory
        current_dir_config = Path.cwd() / 'qauto.config.yaml'
        if current_dir_config.exists():
            return str(current_dir_config)
        
        script_dir = Path(__file__).parent.parent
        return str(script_dir / 'qauto.config.yaml')
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or create default"""
        config_file = Path(self.config_path)
        
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    user_config = yaml.safe_load(f) or {}
                # Merge with defaults
                return self._merge_configs(self.DEFAULT_CONFIG.copy(), user_config)
            except Exception as e:
                print(f"Warning: Error loading config file: {e}")
                print("Using default configuration.")
                return self.DEFAULT_CONFIG.copy()
        else:
            return self.DEFAULT_CONFIG.copy()
    
    def _merge_configs(self, default: Dict, user: Dict) -> Dict:
        """Recursively merge user config with defaults"""
        for key, value in user.items():
            if key in default and isinstance(default[key], dict) and isinstance(value, dict):
                default[key] = self._merge_configs(default[key], value)
            else:
                default[key] = value
        return default
    
    def save(self):
        """Save current configuration to file"""
        config_file = Path(self.config_path)
        config_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(config_file, 'w') as f:
            yaml.dump(self.data, f, default_flow_style=False, sort_keys=False)
        
        print(f"Configuration saved to: {config_file}")
    
    def get(self, key_path: str, default=None):
        """
        Get a config value using dot notation
        Example: config.get('template.primary')
        """
        keys = key_path.split('.')
        value = self.data
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value
    
    def set(self, key_path: str, value: Any):
        """
        Set a config value using dot notation
        Example: config.set('template.primary', '/path/to/template.xlsx')
        """
        keys = key_path.split('.')
        current = self.data
        
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        
        current[keys[-1]] = value
    
    def show(self) -> str:
        """Return configuration as formatted YAML string"""
        return yaml.dump(self.data, default_flow_style=False, sort_keys=False)
    
    def get_template_path(self) -> Optional[str]:
        """Get the first valid template path"""
        primary = self.get('template.primary')
        fallback = self.get('template.fallback')
        
        if primary and os.path.exists(primary):
            return primary
        elif fallback and os.path.exists(fallback):
            return fallback
        
        return None
    
    def resolve_path(self, path: str) -> str:
        """Resolve a path relative to current directory"""
        if os.path.isabs(path):
            return path
        return str(Path.cwd() / path)
