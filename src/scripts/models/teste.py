import os
import sys
sys.path.insert(0,os.path.abspath('.'))
from src.config import config

print(config.DB_HOST)