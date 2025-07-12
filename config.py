"""
配置文件
"""

import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 数据库配置
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', '123123qwe'),
    'database': os.getenv('DB_DATABASE', 'medical_platform'),
    'charset': os.getenv('DB_CHARSET', 'utf8mb4')
}

# 应用配置
APP_CONFIG = {
    'host': os.getenv('APP_HOST', '0.0.0.0'),
    'port': int(os.getenv('APP_PORT', 8000)),
    'debug': os.getenv('APP_DEBUG', 'True').lower() == 'true'
}

# 预定义的 COX 模型参数
cox1_model_coefficients = {
    'PLT': -0.0042557634938221612,
    'Cr': 0.010409835010157001,
    'UP24': 4.6316653571796355e-05,
    'ALT': 0.0089270404049626561,
    'SBPMax': 0.017089075146461921,
    'PDAs': 0.98017990629549234
}

cox2_model_coefficients = {
    'GDA.time': -1.5028012954898466,
    'PDA': 0.12399924268311081,
    'NST': 0.58280288270031,
    'MAP': 0.0089758049607547696,
    'Cr': 0.0072253318806071304
}

# 基线风险函数值
H0_vec_cox1 = {"2": 0.02, "7": 0.15, "14": 0.35}
H0_vec_cox2 = {"2": 0.04998589, "7": 0.13582579, "14": 0.34366626} 