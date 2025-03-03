class Config:
    def __init__(self):
        self.BACKEND_URL_PATH = 'http://127.0.0.1:5000'
        self.FRONTEND_URL_PATH = 'http://127.0.0.1:8501'
        
class DevelopmentConfig(Config):
    def __init__(self):
        super().__init__()
        self.BACKEND_URL_PATH = 'http://127.0.0.1:5000'
        self.FRONTEND_URL_PATH = 'http://127.0.0.1:8501'
        
class ProductionConfig(Config):
    def __init__(self):
        super().__init__()
        self.BACKEND_URL_PATH = 'http://127.0.0.1:5000'
        self.FRONTEND_URL_PATH = 'http://127.0.0.1:8501'
        
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}

def get_config(dev=True):
    return config['development'] if dev else config['production']