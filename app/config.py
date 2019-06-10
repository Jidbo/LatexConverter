import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "yoursecretkey"
    BOOTSTRAP_SERVE_LOCAL = os.environ.get("BOOTSTRAP_SERVE_LOCAL") or True

class DebugConfig(Config):
    DEBUG = True
    ENV = "development"

class ProductionConfig(Config):
    DEBUG = False


config = {
    "debug": DebugConfig,
    "production": ProductionConfig,
}
