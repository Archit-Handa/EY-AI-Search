# TODO: Integrate with other frontend and backend components

class Config:
    def __init__(self):
        self.BACKEND_URL_PATH = 'http://127.0.0.1:5000'
        self.FRONTEND_URL_PATH = 'http://127.0.0.1:8501'
        
class DevelopmentConfig(Config):
    def __init__(self):
        super().__init__()

class TestingConfig(Config):
    def __init__(self):
        super().__init__()

class ProductionConfig(Config):
    def __init__(self):
        super().__init__()

  
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}

def get_config(type: str) -> Config:
    return config['production'] if type.lower() == 'production' \
        else config['testing'] if type.lower() == 'testing' \
            else config['development']