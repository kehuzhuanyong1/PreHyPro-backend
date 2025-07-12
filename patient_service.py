"""
患者数据服务模块
"""

from fastapi import HTTPException
from models import (
    PatientGeneralInfoRequest, PatientLabImagingRequest, 
    PatientHomeMonitoringRequest, SaveResponse
)
from database import execute_insert

def save_patient_general_info(request: PatientGeneralInfoRequest) -> SaveResponse:
    """保存患者基本信息"""
    sql = """
    INSERT INTO patient_general_info (
        age, ethnicity, education, occupation, economic_status, height,
        pre_pregnancy_weight, pre_pregnancy_bmi, last_menstrual_period,
        gestational_weeks, pre_pregnancy_systolic, pre_pregnancy_diastolic,
        pre_pregnancy_map, medical_history, gravidity, parity, uterine_surgery,
        family_history, allergy_history, conception_method, pregnancy_type,
        aspirin_use, complications
    ) VALUES (
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s, %s
    )
    """
    
    values = (
        request.age, request.ethnicity, request.education, request.occupation,
        request.economic_status, request.height, request.pre_pregnancy_weight,
        request.pre_pregnancy_bmi, request.last_menstrual_period,
        request.gestational_weeks, request.pre_pregnancy_systolic,
        request.pre_pregnancy_diastolic, request.pre_pregnancy_map,
        request.medical_history, request.gravidity, request.parity,
        request.uterine_surgery, request.family_history, request.allergy_history,
        request.conception_method, request.pregnancy_type, request.aspirin_use,
        request.complications
    )
    
    record_id, error = execute_insert(sql, values)
    if error:
        raise HTTPException(status_code=500, detail=error)
    
    return SaveResponse(
        success=True,
        message="患者基本信息保存成功",
        id=record_id
    )

def save_patient_lab_imaging(request: PatientLabImagingRequest) -> SaveResponse:
    """保存患者实验室检查数据"""
    sql = """
    INSERT INTO patient_lab_imaging (
        examination_date, ultrasound_date, rbc_count, wbc_count, hemoglobin,
        platelet_count, hematocrit, platelet_volume, urine_protein_qualitative,
        urine_cast, urine_protein_24h, total_bilirubin, total_protein, albumin,
        alt, ast, total_bile_acid, creatinine, urea, uric_acid, aptt, pt, inr,
        tt, fib, d_dimer, fasting_glucose, glucose_1h, glucose_2h, plgf, sflt1,
        sflt1_plgf_ratio, nt, uta_pi, ua_sd_ratio, ua_pi, ua_ri, mca_sd_ratio,
        mca_pi, mca_ri, cpr
    ) VALUES (
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s
    )
    """
    
    values = (
        request.examination_date, request.ultrasound_date, request.rbc_count,
        request.wbc_count, request.hemoglobin, request.platelet_count,
        request.hematocrit, request.platelet_volume, request.urine_protein_qualitative,
        request.urine_cast, request.urine_protein_24h, request.total_bilirubin,
        request.total_protein, request.albumin, request.alt, request.ast,
        request.total_bile_acid, request.creatinine, request.urea, request.uric_acid,
        request.aptt, request.pt, request.inr, request.tt, request.fib,
        request.d_dimer, request.fasting_glucose, request.glucose_1h,
        request.glucose_2h, request.plgf, request.sflt1, request.sflt1_plgf_ratio,
        request.nt, request.uta_pi, request.ua_sd_ratio, request.ua_pi,
        request.ua_ri, request.mca_sd_ratio, request.mca_pi, request.mca_ri,
        request.cpr
    )
    
    record_id, error = execute_insert(sql, values)
    if error:
        raise HTTPException(status_code=500, detail=error)
    
    return SaveResponse(
        success=True,
        message="实验室检查数据保存成功",
        id=record_id
    )

def save_patient_home_monitoring(request: PatientHomeMonitoringRequest) -> SaveResponse:
    """保存患者家庭监测数据"""
    sql = """
    INSERT INTO patient_home_monitoring (
        home_monitoring_date, home_systolic, home_diastolic, fetal_heart_rate,
        fetal_movement, home_sflt1_plgf_ratio, fetal_monitoring_file, urine_test_file
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    values = (
        request.home_monitoring_date, request.home_systolic, request.home_diastolic,
        request.fetal_heart_rate, request.fetal_movement, request.home_sflt1_plgf_ratio,
        request.fetal_monitoring_file, request.urine_test_file
    )
    
    record_id, error = execute_insert(sql, values)
    if error:
        raise HTTPException(status_code=500, detail=error)
    
    return SaveResponse(
        success=True,
        message="家庭监测数据保存成功",
        id=record_id
    ) 