# 妊娠期高血压母婴监测及结局预测平台 - 后端API

## 功能概述

本系统提供完整的患者数据收集和预测功能，包括：

1. **患者基本信息收集** - 一般临床资料及本次妊娠情况
2. **实验室检查数据收集** - 血常规、尿常规、肝功能、肾功能等
3. **家庭监测数据收集** - 血压、胎心、胎动等动态监测数据
4. **预测模型API** - 四种不同的预测模型

## 系统架构

项目采用模块化设计，代码结构清晰：

```
backend/
├── main.py                 # FastAPI主应用和路由
├── config.py               # 配置文件（数据库、模型参数）
├── models.py               # Pydantic数据模型定义
├── database.py             # 数据库连接和操作
├── utils.py                # 工具函数
├── prediction_models.py    # 预测模型逻辑
├── patient_service.py      # 患者数据服务
├── requirements.txt        # Python依赖
├── init.sql               # 数据库初始化脚本
├── test_patient_api.py    # API测试脚本
└── README.md              # 项目说明
```

## 系统要求

- Python 3.8+
- MySQL 5.7+
- 现代浏览器（支持ES6+）

## 安装和配置

### 1. 安装Python依赖

```bash
cd backend
pip install -r requirements.txt
```

### 2. 配置数据库

1. 创建MySQL数据库：
```sql
CREATE DATABASE medical_platform DEFAULT CHARACTER SET utf8mb4;
```

2. 运行初始化脚本：
```bash
mysql -u root -p medical_platform < init.sql
```

3. 修改数据库配置（在 `config.py` 中）：
```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'your_username',
    'password': 'your_password',
    'database': 'medical_platform',
    'charset': 'utf8mb4'
}
```

### 3. 启动后端服务

```bash
cd backend
python main.py
```

服务将在 `http://localhost:8000` 启动

## 模块说明

### config.py
- 数据库连接配置
- 预测模型参数配置
- 基线风险函数值

### models.py
- 所有Pydantic数据模型定义
- 请求和响应模型
- 数据验证规则

### database.py
- 数据库连接管理
- 数据库操作封装
- 错误处理

### utils.py
- 通用工具函数
- 孕天数计算
- 平均动脉压计算

### prediction_models.py
- 四个预测模型的实现
- 数学计算逻辑
- 错误处理

### patient_service.py
- 患者数据保存服务
- SQL语句构建
- 业务逻辑处理

### main.py
- FastAPI应用配置
- 路由定义
- 中间件配置

## API端点

### 患者数据收集API

#### 1. 保存患者基本信息
- **POST** `/api/patient/general-info`
- 保存患者的基本临床资料和妊娠情况

#### 2. 保存实验室检查数据
- **POST** `/api/patient/lab-imaging`
- 保存血常规、尿常规、肝功能、肾功能等检查数据

#### 3. 保存家庭监测数据
- **POST** `/api/patient/home-monitoring`
- 保存家庭动态监测数据

### 预测模型API

#### 1. FGR模型预测
- **POST** `/predict/fgr`
- 胎儿生长受限围产不良结局预测

#### 2. FGR-Neonatal模型预测
- **POST** `/predict/fgr-neonatal`
- 先发胎儿生长受限的子痫前期新生儿不良结局预测

#### 3. Maternal-COX模型预测
- **POST** `/predict/maternal-cox`
- 子痫前期母体不良结局COX模型预测

#### 4. Neonatal-COX模型预测
- **POST** `/predict/neonatal-cox`
- 子痫前期新生儿不良结局COX模型预测

### 其他API

- **GET** `/health` - 健康检查
- **GET** `/` - API根路径，显示所有可用端点

## 数据库表结构

系统包含以下数据表：

1. `patient_general_info` - 患者基本信息
2. `patient_lab_imaging` - 实验室检查数据
3. `patient_home_monitoring` - 家庭监测数据
4. `model_fgr_params` - FGR模型参数
5. `model_fgr_neonatal_params` - FGR-Neonatal模型参数
6. `model_maternal_cox_params` - Maternal-COX模型参数
7. `model_neonatal_cox_params` - Neonatal-COX模型参数

## 测试

运行测试脚本验证API功能：

```bash
cd backend
python test_patient_api.py
```

测试内容包括：
- 健康检查
- 患者基本信息保存
- 实验室检查数据保存
- 家庭监测数据保存
- 预测模型功能

## 前端集成

前端页面已配置为自动提交数据到后端API：

1. `patient-form.html` - 患者基本信息收集
2. `patient-lab.html` - 实验室检查数据收集
3. `patient-monitoring.html` - 家庭监测数据收集

每个表单都有独立的提交按钮，数据会保存到对应的数据库表中。

## 开发指南

### 添加新的预测模型

1. 在 `config.py` 中添加模型参数
2. 在 `models.py` 中定义请求模型
3. 在 `prediction_models.py` 中实现预测逻辑
4. 在 `main.py` 中添加路由

### 添加新的数据表

1. 在 `init.sql` 中定义表结构
2. 在 `models.py` 中定义数据模型
3. 在 `patient_service.py` 中实现保存逻辑
4. 在 `main.py` 中添加API端点

### 代码规范

- 使用类型注解
- 添加详细的文档字符串
- 遵循 PEP 8 代码规范
- 模块职责单一，便于维护

## 注意事项

1. 确保MySQL服务正在运行
2. 检查数据库连接配置是否正确
3. 前端页面需要后端服务运行在 `http://localhost:8000`
4. 所有API都支持CORS，可以从前端页面直接调用

## 故障排除

### 数据库连接错误
- 检查MySQL服务是否运行
- 验证数据库配置信息
- 确认数据库和表已创建

### API调用失败
- 检查后端服务是否启动
- 验证API端点URL是否正确
- 查看浏览器控制台的错误信息

### 模块导入错误
- 确保所有Python文件在同一目录下
- 检查import语句是否正确
- 验证Python路径配置

### 前端页面无法访问
- 确保后端服务在正确的端口运行
- 检查CORS配置
- 验证API响应格式 