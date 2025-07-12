#!/usr/bin/env python3
"""
妊娠期高血压母婴监测及结局预测平台 API 启动脚本
"""

import uvicorn
from main import app

if __name__ == "__main__":
    print("🚀 启动妊娠期高血压母婴监测及结局预测平台 API...")
    print("📖 API 文档地址: http://localhost:8000/docs")
    print("🔍 健康检查: http://localhost:8000/health")
    print("🌐 根路径: http://localhost:8000/")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    ) 