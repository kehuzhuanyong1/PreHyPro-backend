"""
预测模型模块
"""

import math
from datetime import date
from fastapi import HTTPException
from models import (
    FGRPredictionRequest, FGRNeonatalPredictionRequest,
    MaternalCOXPredictionRequest, NeonatalCOXPredictionRequest,
    PredictionResponse
)
from config import (
    cox1_model_coefficients, cox2_model_coefficients,
    H0_vec_cox1, H0_vec_cox2
)
from utils import calculate_gestational_days, calculate_map
from prediction_service import (
    save_fgr_prediction, save_fgr_neonatal_prediction,
    save_maternal_cox_prediction, save_neonatal_cox_prediction
)

def predict_fgr(request: FGRPredictionRequest) -> PredictionResponse:
    """
    胎儿生长受限围产不良结局Logistic模型预测
    """
    try:
        # 计算诊断时孕天数
        gestational_days = calculate_gestational_days(request.lmp_date, request.diagnosis_date)
        
        # Logistic回归计算
        logit_p = (0.864 + 
                   1.39 * int(request.preterm) - 
                   0.02 * gestational_days + 
                   1.05 * int(request.hypertension) + 
                   1.44 * int(request.nst) + 
                   1.12 * int(request.weight_growth) + 
                   2.58 * int(request.umbilical_flow))
        
        prob = math.exp(logit_p) / (1 + math.exp(logit_p))
        
        result = PredictionResponse(
            prediction=prob * 100,
            message=f"🎯 预测概率：{prob * 100:.1f}%",
            additional_info={
                "gestational_days": gestational_days,
                "logit_value": logit_p
            }
        )
        
        # 保存预测结果到数据库
        try:
            save_fgr_prediction(request, result)
        except Exception as save_error:
            print(f"保存FGR预测结果失败: {save_error}")
            # 不中断预测流程，只记录错误
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"预测计算错误: {str(e)}")

def predict_fgr_neonatal(request: FGRNeonatalPredictionRequest) -> PredictionResponse:
    """
    先发胎儿生长受限的子痫前期新生儿不良结局Logistic模型预测
    """
    try:
        logit_p = (-0.663 - 
                   0.246 * request.anc_visits + 
                   2.648 * int(request.umbilical_flow) + 
                   1.445 * int(request.pe_gestation) + 
                   1.378 * int(request.delivery_gestation) + 
                   1.363 * int(request.fetal_growth))
        
        prob = math.exp(logit_p) / (1 + math.exp(logit_p))
        
        result = PredictionResponse(
            prediction=prob * 100,
            message=f"🎯 预测概率：{prob * 100:.1f}%",
            additional_info={
                "logit_value": logit_p
            }
        )
        
        # 保存预测结果到数据库
        try:
            save_fgr_neonatal_prediction(request, result)
        except Exception as save_error:
            print(f"保存FGR-Neonatal预测结果失败: {save_error}")
            # 不中断预测流程，只记录错误
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"预测计算错误: {str(e)}")

def predict_maternal_cox(request: MaternalCOXPredictionRequest) -> PredictionResponse:
    """
    子痫前期母体不良结局COX模型预测
    """
    try:
        if request.cox1_time not in [2, 7, 14]:
            raise HTTPException(status_code=400, detail="cox1_time 必须是 2, 7, 或 14")
        
        # 计算线性预测值
        lp = (cox1_model_coefficients['PLT'] * request.plt +
              cox1_model_coefficients['Cr'] * request.cr +
              cox1_model_coefficients['UP24'] * request.up24 +
              cox1_model_coefficients['ALT'] * request.alt +
              cox1_model_coefficients['SBPMax'] * request.sbpmax +
              cox1_model_coefficients['PDAs'] * int(request.pdas))
        
        # 计算风险
        H0 = H0_vec_cox1[str(request.cox1_time)]
        S = math.exp(-H0 * math.exp(lp))
        risk = 1 - S
        
        result = PredictionResponse(
            prediction=risk * 100,
            message=f"🎯 第{request.cox1_time}天预测风险：{risk * 100:.1f}%",
            additional_info={
                "linear_predictor": lp,
                "baseline_hazard": H0,
                "survival_probability": S
            }
        )
        
        # 保存预测结果到数据库
        try:
            save_maternal_cox_prediction(request, result)
        except Exception as save_error:
            print(f"保存Maternal-COX预测结果失败: {save_error}")
            # 不中断预测流程，只记录错误
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"预测计算错误: {str(e)}")

def predict_neonatal_cox(request: NeonatalCOXPredictionRequest) -> PredictionResponse:
    """
    子痫前期新生儿不良结局COX模型预测
    """
    try:
        if request.cox2_time not in [2, 7, 14]:
            raise HTTPException(status_code=400, detail="cox2_time 必须是 2, 7, 或 14")
        
        # 计算入院时孕天数
        admission_gestational_days = calculate_gestational_days(request.lmp_date, request.admission_date)
        
        # 计算平均动脉压
        map_value = calculate_map(request.sbp_admission, request.dbp_admission)
        
        # 计算GDA.time
        gda_time = request.gda_group * math.log10(request.cox2_time + 20)
        
        # 计算线性预测值
        lp = (cox2_model_coefficients['GDA.time'] * gda_time +
              cox2_model_coefficients['PDA'] * admission_gestational_days +
              cox2_model_coefficients['NST'] * int(request.nst) +
              cox2_model_coefficients['MAP'] * map_value +
              cox2_model_coefficients['Cr'] * request.cr2)
        
        # 计算风险
        H0 = H0_vec_cox2[str(request.cox2_time)]
        S = math.exp(-H0 * math.exp(lp))
        risk = 1 - S
        
        result = PredictionResponse(
            prediction=risk * 100,
            message=f"🎯 第{request.cox2_time}天预测风险：{risk * 100:.1f}%",
            additional_info={
                "gestational_days": admission_gestational_days,
                "map_value": map_value,
                "gda_time": gda_time,
                "linear_predictor": lp,
                "baseline_hazard": H0,
                "survival_probability": S
            }
        )
        
        # 保存预测结果到数据库
        try:
            save_neonatal_cox_prediction(request, result)
        except Exception as save_error:
            print(f"保存Neonatal-COX预测结果失败: {save_error}")
            # 不中断预测流程，只记录错误
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"预测计算错误: {str(e)}") 