"""
Configuration management for Email Automation Suite
"""
import os
import configparser

class ConfigManager:
    def __init__(self, config_file: str = "config/settings.ini"):
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        self.load_config()
    
    def load_config(self):
        """Load configuration from file"""
        if os.path.exists(self.config_file):
            self.config.read(self.config_file)
        else:
            self.create_default_config()
    
    def create_default_config(self):
        """Create default configuration file"""
        self.config['EMAIL'] = {
            'smtp_server': 'smtp.gmail.com',
            'smtp_port': '587',
            'use_tls': 'True',
            'username': '',
            'password': ''
        }
        
        self.config['APP'] = {
            'theme': 'default',
            'auto_save': 'True',
            'check_interval': '60'
        }
        
        self.save_config()
    
    def save_config(self):
        """Save configuration to file"""
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)
    
    def get(self, section: str, key: str, fallback=None):
        """Get configuration value"""
        return self.config.get(section, key, fallback=fallback)