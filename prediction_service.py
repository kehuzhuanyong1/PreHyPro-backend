"""
预测结果服务模块
"""

from fastapi import HTTPException
from models import (
    FGRPredictionRequest, FGRNeonatalPredictionRequest,
    MaternalCOXPredictionRequest, NeonatalCOXPredictionRequest,
    PredictionResponse, SaveResponse
)
from database import execute_insert

def save_fgr_prediction(request: FGRPredictionRequest, result: PredictionResponse) -> SaveResponse:
    """保存FGR预测结果"""
    sql = """
    INSERT INTO model_fgr_params (
        preterm, lmp_date, diagnosis_date, hypertension, nst, weight_growth, 
        umbilical_flow, prediction_result, gestational_days, logit_value
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    values = (
        request.preterm, request.lmp_date, request.diagnosis_date, 
        request.hypertension, request.nst, request.weight_growth, 
        request.umbilical_flow, result.prediction, 
        result.additional_info.get('gestational_days'), 
        result.additional_info.get('logit_value')
    )
    
    record_id, error = execute_insert(sql, values)
    if error:
        raise HTTPException(status_code=500, detail=error)
    
    return SaveResponse(
        success=True,
        message="FGR预测结果保存成功",
        id=record_id
    )

def save_fgr_neonatal_prediction(request: FGRNeonatalPredictionRequest, result: PredictionResponse) -> SaveResponse:
    """保存FGR-Neonatal预测结果"""
    sql = """
    INSERT INTO model_fgr_neonatal_params (
        anc_visits, umbilical_flow, pe_gestation, delivery_gestation, 
        fetal_growth, prediction_result, logit_value
    ) VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    
    values = (
        request.anc_visits, request.umbilical_flow, request.pe_gestation, 
        request.delivery_gestation, request.fetal_growth, result.prediction,
        result.additional_info.get('logit_value')
    )
    
    record_id, error = execute_insert(sql, values)
    if error:
        raise HTTPException(status_code=500, detail=error)
    
    return SaveResponse(
        success=True,
        message="FGR-Neonatal预测结果保存成功",
        id=record_id
    )

def save_maternal_cox_prediction(request: MaternalCOXPredictionRequest, result: PredictionResponse) -> SaveResponse:
    """保存Maternal-COX预测结果"""
    sql = """
    INSERT INTO model_maternal_cox_params (
        plt, cr, up24, alt, sbpmax, pdas, cox1_time, prediction_result,
        linear_predictor, baseline_hazard, survival_probability
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    values = (
        request.plt, request.cr, request.up24, request.alt, request.sbpmax, 
        request.pdas, request.cox1_time, result.prediction,
        result.additional_info.get('linear_predictor'),
        result.additional_info.get('baseline_hazard'),
        result.additional_info.get('survival_probability')
    )
    
    record_id, error = execute_insert(sql, values)
    if error:
        raise HTTPException(status_code=500, detail=error)
    
    return SaveResponse(
        success=True,
        message="Maternal-COX预测结果保存成功",
        id=record_id
    )

def save_neonatal_cox_prediction(request: NeonatalCOXPredictionRequest, result: PredictionResponse) -> SaveResponse:
    """保存Neonatal-COX预测结果"""
    sql = """
    INSERT INTO model_neonatal_cox_params (
        lmp_date, admission_date, gda_group, cox2_time, nst, sbp_admission,
        dbp_admission, cr2, prediction_result, gestational_days, map_value,
        gda_time, linear_predictor, baseline_hazard, survival_probability
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    values = (
        request.lmp_date, request.admission_date, request.gda_group, 
        request.cox2_time, request.nst, request.sbp_admission, request.dbp_admission,
        request.cr2, result.prediction, result.additional_info.get('gestational_days'),
        result.additional_info.get('map_value'), result.additional_info.get('gda_time'),
        result.additional_info.get('linear_predictor'), result.additional_info.get('baseline_hazard'),
        result.additional_info.get('survival_probability')
    )
    
    record_id, error = execute_insert(sql, values)
    if error:
        raise HTTPException(status_code=500, detail=error)
    
    return SaveResponse(
        success=True,
        message="Neonatal-COX预测结果保存成功",
        id=record_id
    ) 