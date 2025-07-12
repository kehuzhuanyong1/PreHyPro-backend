"""
数据模型定义
"""

from pydantic import BaseModel
from typing import Optional
from datetime import date

# 预测模型请求
class FGRPredictionRequest(BaseModel):
    preterm: bool
    lmp_date: date
    diagnosis_date: date
    hypertension: bool
    nst: bool
    weight_growth: bool
    umbilical_flow: bool

class FGRNeonatalPredictionRequest(BaseModel):
    anc_visits: int
    umbilical_flow: bool
    pe_gestation: bool
    delivery_gestation: bool
    fetal_growth: bool

class MaternalCOXPredictionRequest(BaseModel):
    plt: float
    cr: float
    up24: float
    alt: float
    sbpmax: float
    pdas: bool
    cox1_time: int

class NeonatalCOXPredictionRequest(BaseModel):
    lmp_date: date
    admission_date: date
    gda_group: float
    cox2_time: int
    nst: bool
    sbp_admission: float
    dbp_admission: float
    cr2: float

# 患者数据请求模型
class PatientGeneralInfoRequest(BaseModel):
    age: Optional[int] = None
    ethnicity: Optional[str] = None
    education: Optional[str] = None
    occupation: Optional[str] = None
    economic_status: Optional[str] = None
    height: Optional[float] = None
    pre_pregnancy_weight: Optional[float] = None
    pre_pregnancy_bmi: Optional[float] = None
    last_menstrual_period: Optional[date] = None
    gestational_weeks: Optional[str] = None
    pre_pregnancy_systolic: Optional[float] = None
    pre_pregnancy_diastolic: Optional[float] = None
    pre_pregnancy_map: Optional[float] = None
    medical_history: Optional[str] = None
    gravidity: Optional[int] = None
    parity: Optional[int] = None
    uterine_surgery: Optional[str] = None
    family_history: Optional[str] = None
    allergy_history: Optional[str] = None
    conception_method: Optional[str] = None
    pregnancy_type: Optional[str] = None
    aspirin_use: Optional[str] = None
    complications: Optional[str] = None

class PatientLabImagingRequest(BaseModel):
    examination_date: Optional[date] = None
    ultrasound_date: Optional[date] = None
    rbc_count: Optional[float] = None
    wbc_count: Optional[float] = None
    hemoglobin: Optional[float] = None
    platelet_count: Optional[float] = None
    hematocrit: Optional[float] = None
    platelet_volume: Optional[float] = None
    urine_protein_qualitative: Optional[str] = None
    urine_cast: Optional[str] = None
    urine_protein_24h: Optional[float] = None
    total_bilirubin: Optional[float] = None
    total_protein: Optional[float] = None
    albumin: Optional[float] = None
    alt: Optional[float] = None
    ast: Optional[float] = None
    total_bile_acid: Optional[float] = None
    creatinine: Optional[float] = None
    urea: Optional[float] = None
    uric_acid: Optional[float] = None
    aptt: Optional[float] = None
    pt: Optional[float] = None
    inr: Optional[float] = None
    tt: Optional[float] = None
    fib: Optional[float] = None
    d_dimer: Optional[float] = None
    fasting_glucose: Optional[float] = None
    glucose_1h: Optional[float] = None
    glucose_2h: Optional[float] = None
    plgf: Optional[float] = None
    sflt1: Optional[float] = None
    sflt1_plgf_ratio: Optional[float] = None
    nt: Optional[float] = None
    uta_pi: Optional[float] = None
    ua_sd_ratio: Optional[float] = None
    ua_pi: Optional[float] = None
    ua_ri: Optional[float] = None
    mca_sd_ratio: Optional[float] = None
    mca_pi: Optional[float] = None
    mca_ri: Optional[float] = None
    cpr: Optional[float] = None

class PatientHomeMonitoringRequest(BaseModel):
    home_monitoring_date: Optional[date] = None
    home_systolic: Optional[float] = None
    home_diastolic: Optional[float] = None
    fetal_heart_rate: Optional[float] = None
    fetal_movement: Optional[float] = None
    home_sflt1_plgf_ratio: Optional[float] = None
    fetal_monitoring_file: Optional[bytes] = None
    urine_test_file: Optional[bytes] = None

# 响应模型
class PredictionResponse(BaseModel):
    prediction: float
    message: str
    additional_info: Optional[dict] = None

class SaveResponse(BaseModel):
    success: bool
    message: str
    id: Optional[int] = None 