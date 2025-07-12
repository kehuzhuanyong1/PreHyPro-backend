"""
妊娠期高血压母婴监测及结局预测平台 - 主应用
"""

from fastapi import FastAPI, Form, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from typing import Optional
from datetime import date

# 导入模块
from models import (
    FGRPredictionRequest, FGRNeonatalPredictionRequest,
    MaternalCOXPredictionRequest, NeonatalCOXPredictionRequest,
    PatientGeneralInfoRequest, PatientLabImagingRequest, 
    PatientHomeMonitoringRequest, PredictionResponse, SaveResponse
)
from prediction_models import (
    predict_fgr, predict_fgr_neonatal, predict_maternal_cox, predict_neonatal_cox
)
from patient_service import (
    save_patient_general_info, save_patient_lab_imaging, save_patient_home_monitoring
)
from admin_api import admin_router

# 创建FastAPI应用
app = FastAPI(
    title="妊娠期高血压母婴监测及结局预测平台 API",
    description="基于机器学习的妊娠期高血压疾病预测模型 API 服务",
    version="1.0.0"
)

# 添加 CORS 中间件，解决跨域问题
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源，生产环境建议设置具体域名
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有 HTTP 方法
    allow_headers=["*"],  # 允许所有请求头
)

# 包含后台管理API
app.include_router(admin_router)

@app.get("/")
async def root():
    """API 根路径"""
    return {
        "message": "妊娠期高血压母婴监测及结局预测平台 API",
        "version": "1.0.0",
        "endpoints": {
            "/predict/fgr": "胎儿生长受限围产不良结局预测",
            "/predict/fgr-neonatal": "先发胎儿生长受限的子痫前期新生儿不良结局预测",
            "/predict/maternal-cox": "子痫前期母体不良结局COX模型预测",
            "/predict/neonatal-cox": "子痫前期新生儿不良结局COX模型预测",
            "/api/patient/general-info": "保存患者基本信息",
            "/api/patient/lab-imaging": "保存实验室检查数据",
            "/api/patient/home-monitoring": "保存家庭监测数据"
        }
    }

@app.get("/health")
async def health_check():
    """健康检查端点"""
    return {"status": "healthy", "service": "pregnancy_prediction_api"}

# 预测模型API端点
@app.post("/predict/fgr", response_model=PredictionResponse)
async def predict_fgr_endpoint(request: FGRPredictionRequest):
    """
    胎儿生长受限围产不良结局Logistic模型预测
    
    参数:
    - preterm: 是否早产
    - lmp_date: 末次月经日期
    - diagnosis_date: 诊断日期
    - hypertension: 是否有高血压
    - nst: 是否有NST异常
    - weight_growth: 是否有体重增长异常
    - umbilical_flow: 是否有脐血流异常
    """
    return predict_fgr(request)

@app.post("/predict/fgr-neonatal", response_model=PredictionResponse)
async def predict_fgr_neonatal_endpoint(request: FGRNeonatalPredictionRequest):
    """
    先发胎儿生长受限的子痫前期新生儿不良结局Logistic模型预测
    
    参数:
    - anc_visits: 产前检查次数
    - umbilical_flow: 是否有脐血流异常
    - pe_gestation: 是否有子痫前期
    - delivery_gestation: 是否有分娩异常
    - fetal_growth: 是否有胎儿生长异常
    """
    return predict_fgr_neonatal(request)

@app.post("/predict/maternal-cox", response_model=PredictionResponse)
async def predict_maternal_cox_endpoint(request: MaternalCOXPredictionRequest):
    """
    子痫前期母体不良结局COX模型预测
    
    参数:
    - plt: 血小板计数
    - cr: 肌酐
    - up24: 24小时尿蛋白
    - alt: 丙氨酸氨基转移酶
    - sbpmax: 收缩压最大值
    - pdas: 是否有PDA
    - cox1_time: 预测时间点(2, 7, 或 14天)
    """
    return predict_maternal_cox(request)

@app.post("/predict/neonatal-cox", response_model=PredictionResponse)
async def predict_neonatal_cox_endpoint(request: NeonatalCOXPredictionRequest):
    """
    子痫前期新生儿不良结局COX模型预测
    
    参数:
    - lmp_date: 末次月经日期
    - admission_date: 入院日期
    - gda_group: GDA分组
    - cox2_time: 预测时间点(2, 7, 或 14天)
    - nst: 是否有NST异常
    - sbp_admission: 入院时收缩压
    - dbp_admission: 入院时舒张压
    - cr2: 肌酐
    """
    return predict_neonatal_cox(request)

# 患者数据保存API端点
@app.post("/api/patient/general-info", response_model=SaveResponse)
async def save_patient_general_info_endpoint(request: PatientGeneralInfoRequest):
    """保存患者基本信息"""
    return save_patient_general_info(request)

@app.post("/api/patient/lab-imaging", response_model=SaveResponse)
async def save_patient_lab_imaging_endpoint(request: PatientLabImagingRequest):
    """保存患者实验室检查数据"""
    return save_patient_lab_imaging(request)

@app.post("/api/patient/home-monitoring", response_model=SaveResponse)
async def save_patient_home_monitoring_endpoint(
    home_monitoring_date: Optional[date] = Form(None),
    home_systolic: Optional[float] = Form(None),
    home_diastolic: Optional[float] = Form(None),
    fetal_heart_rate: Optional[float] = Form(None),
    fetal_movement: Optional[float] = Form(None),
    home_sflt1_plgf_ratio: Optional[float] = Form(None),
    fetal_monitoring_file: Optional[UploadFile] = File(None),
    urine_test_file: Optional[UploadFile] = File(None)
):
    """保存患者家庭监测数据"""
    # 读取文件内容
    fetal_monitoring_data = None
    urine_test_data = None
    
    if fetal_monitoring_file:
        fetal_monitoring_data = await fetal_monitoring_file.read()
    
    if urine_test_file:
        urine_test_data = await urine_test_file.read()
    
    # 创建请求对象
    request = PatientHomeMonitoringRequest(
        home_monitoring_date=home_monitoring_date,
        home_systolic=home_systolic,
        home_diastolic=home_diastolic,
        fetal_heart_rate=fetal_heart_rate,
        fetal_movement=fetal_movement,
        home_sflt1_plgf_ratio=home_sflt1_plgf_ratio,
        fetal_monitoring_file=fetal_monitoring_data,
        urine_test_file=urine_test_data
    )
    
    return save_patient_home_monitoring(request)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 