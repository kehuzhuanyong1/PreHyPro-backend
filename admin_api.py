"""
后台管理API模块
提供用户数据查看和统计分析功能
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional, Dict, Any
from datetime import date, datetime, timedelta
from pydantic import BaseModel
import pymysql
from config import DB_CONFIG

# 创建路由器
admin_router = APIRouter(prefix="/admin", tags=["后台管理"])

# 响应模型
class PatientDataResponse(BaseModel):
    id: int
    created_at: datetime
    data: Dict[str, Any]

class StatisticsResponse(BaseModel):
    total_patients: int
    total_predictions: int
    data_by_date: List[Dict[str, Any]]
    prediction_distribution: Dict[str, int]

class PatientDetailResponse(BaseModel):
    general_info: Optional[Dict[str, Any]]
    lab_imaging: List[Dict[str, Any]]
    home_monitoring: List[Dict[str, Any]]
    predictions: List[Dict[str, Any]]

# 数据库连接函数
def get_db_connection():
    """获取数据库连接"""
    try:
        connection = pymysql.connect(**DB_CONFIG)
        return connection
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"数据库连接失败: {str(e)}")

# 1. 患者基本信息管理接口
@admin_router.get("/patients/general-info", response_model=List[PatientDataResponse])
async def get_patient_general_info(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    start_date: Optional[date] = Query(None, description="开始日期"),
    end_date: Optional[date] = Query(None, description="结束日期"),
    age_min: Optional[int] = Query(None, ge=0, description="最小年龄"),
    age_max: Optional[int] = Query(None, ge=0, description="最大年龄")
):
    """获取患者基本信息列表"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        
        # 构建查询条件
        where_conditions = []
        params = []
        
        if start_date:
            where_conditions.append("created_at >= %s")
            params.append(start_date)
        
        if end_date:
            where_conditions.append("created_at <= %s")
            params.append(end_date)
        
        if age_min is not None:
            where_conditions.append("age >= %s")
            params.append(age_min)
        
        if age_max is not None:
            where_conditions.append("age <= %s")
            params.append(age_max)
        
        where_clause = " WHERE " + " AND ".join(where_conditions) if where_conditions else ""
        
        # 计算偏移量
        offset = (page - 1) * page_size
        
        # 查询数据
        sql = f"""
        SELECT id, age, ethnicity, education, occupation, economic_status, 
               height, pre_pregnancy_weight, pre_pregnancy_bmi, 
               last_menstrual_period, gestational_weeks, 
               pre_pregnancy_systolic, pre_pregnancy_diastolic, pre_pregnancy_map,
               medical_history, gravidity, parity, uterine_surgery,
               family_history, allergy_history, conception_method,
               pregnancy_type, aspirin_use, complications, created_at
        FROM patient_general_info
        {where_clause}
        ORDER BY created_at DESC
        LIMIT %s OFFSET %s
        """
        
        params.extend([page_size, offset])
        cursor.execute(sql, params)
        results = cursor.fetchall()
        
        # 格式化响应
        formatted_results = []
        for row in results:
            formatted_results.append(PatientDataResponse(
                id=row['id'],
                created_at=row['created_at'],
                data=row
            ))
        
        cursor.close()
        connection.close()
        
        return formatted_results
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询失败: {str(e)}")

# 2. 实验室检查数据管理接口
@admin_router.get("/patients/lab-imaging", response_model=List[PatientDataResponse])
async def get_patient_lab_imaging(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    start_date: Optional[date] = Query(None, description="开始日期"),
    end_date: Optional[date] = Query(None, description="结束日期")
):
    """获取实验室检查数据列表"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        
        # 构建查询条件
        where_conditions = []
        params = []
        
        if start_date:
            where_conditions.append("examination_date >= %s")
            params.append(start_date)
        
        if end_date:
            where_conditions.append("examination_date <= %s")
            params.append(end_date)
        
        where_clause = " WHERE " + " AND ".join(where_conditions) if where_conditions else ""
        
        # 计算偏移量
        offset = (page - 1) * page_size
        
        # 查询数据
        sql = f"""
        SELECT id, examination_date, ultrasound_date, rbc_count, wbc_count,
               hemoglobin, platelet_count, hematocrit, platelet_volume,
               urine_protein_qualitative, urine_cast, urine_protein_24h,
               total_bilirubin, total_protein, albumin, alt, ast, total_bile_acid,
               creatinine, urea, uric_acid, aptt, pt, inr, tt, fib, d_dimer,
               fasting_glucose, glucose_1h, glucose_2h, plgf, sflt1, sflt1_plgf_ratio,
               nt, uta_pi, ua_sd_ratio, ua_pi, ua_ri, mca_sd_ratio, mca_pi, mca_ri, cpr,
               created_at
        FROM patient_lab_imaging
        {where_clause}
        ORDER BY created_at DESC
        LIMIT %s OFFSET %s
        """
        
        params.extend([page_size, offset])
        cursor.execute(sql, params)
        results = cursor.fetchall()
        
        # 格式化响应
        formatted_results = []
        for row in results:
            formatted_results.append(PatientDataResponse(
                id=row['id'],
                created_at=row['created_at'],
                data=row
            ))
        
        cursor.close()
        connection.close()
        
        return formatted_results
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询失败: {str(e)}")

# 3. 家庭监测数据管理接口
@admin_router.get("/patients/home-monitoring", response_model=List[PatientDataResponse])
async def get_patient_home_monitoring(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    start_date: Optional[date] = Query(None, description="开始日期"),
    end_date: Optional[date] = Query(None, description="结束日期")
):
    """获取家庭监测数据列表"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        
        # 构建查询条件
        where_conditions = []
        params = []
        
        if start_date:
            where_conditions.append("home_monitoring_date >= %s")
            params.append(start_date)
        
        if end_date:
            where_conditions.append("home_monitoring_date <= %s")
            params.append(end_date)
        
        where_clause = " WHERE " + " AND ".join(where_conditions) if where_conditions else ""
        
        # 计算偏移量
        offset = (page - 1) * page_size
        
        # 查询数据（不包含文件内容）
        sql = f"""
        SELECT id, home_monitoring_date, home_systolic, home_diastolic,
               fetal_heart_rate, fetal_movement, home_sflt1_plgf_ratio,
               CASE WHEN fetal_monitoring_file IS NOT NULL THEN '有文件' ELSE '无文件' END as fetal_monitoring_file_status,
               CASE WHEN urine_test_file IS NOT NULL THEN '有文件' ELSE '无文件' END as urine_test_file_status,
               created_at
        FROM patient_home_monitoring
        {where_clause}
        ORDER BY created_at DESC
        LIMIT %s OFFSET %s
        """
        
        params.extend([page_size, offset])
        cursor.execute(sql, params)
        results = cursor.fetchall()
        
        # 格式化响应
        formatted_results = []
        for row in results:
            formatted_results.append(PatientDataResponse(
                id=row['id'],
                created_at=row['created_at'],
                data=row
            ))
        
        cursor.close()
        connection.close()
        
        return formatted_results
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询失败: {str(e)}")

# 4. 预测结果管理接口
@admin_router.get("/predictions", response_model=List[PatientDataResponse])
async def get_predictions(
    model_type: Optional[str] = Query(None, description="模型类型: fgr, fgr_neonatal, maternal_cox, neonatal_cox"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    start_date: Optional[date] = Query(None, description="开始日期"),
    end_date: Optional[date] = Query(None, description="结束日期"),
    min_prediction: Optional[float] = Query(None, ge=0, le=100, description="最小预测值"),
    max_prediction: Optional[float] = Query(None, ge=0, le=100, description="最大预测值")
):
    """获取预测结果列表"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        
        # 根据模型类型选择表
        table_mapping = {
            'fgr': 'model_fgr_params',
            'fgr_neonatal': 'model_fgr_neonatal_params',
            'maternal_cox': 'model_maternal_cox_params',
            'neonatal_cox': 'model_neonatal_cox_params'
        }
        
        if model_type and model_type not in table_mapping:
            raise HTTPException(status_code=400, detail="无效的模型类型")
        
        # 构建查询条件
        where_conditions = []
        params = []
        
        if model_type:
            # 如果指定了模型类型，只查询该模型
            table_name = table_mapping[model_type]
            sql = f"SELECT * FROM {table_name}"
        else:
            # 否则查询所有模型的结果
            sql = """
            SELECT 'fgr' as model_type, id, prediction_result, created_at FROM model_fgr_params
            UNION ALL
            SELECT 'fgr_neonatal' as model_type, id, prediction_result, created_at FROM model_fgr_neonatal_params
            UNION ALL
            SELECT 'maternal_cox' as model_type, id, prediction_result, created_at FROM model_maternal_cox_params
            UNION ALL
            SELECT 'neonatal_cox' as model_type, id, prediction_result, created_at FROM model_neonatal_cox_params
            """
        
        if start_date:
            where_conditions.append("created_at >= %s")
            params.append(start_date)
        
        if end_date:
            where_conditions.append("created_at <= %s")
            params.append(end_date)
        
        if min_prediction is not None:
            where_conditions.append("prediction_result >= %s")
            params.append(min_prediction)
        
        if max_prediction is not None:
            where_conditions.append("prediction_result <= %s")
            params.append(max_prediction)
        
        if where_conditions:
            sql += " WHERE " + " AND ".join(where_conditions)
        
        sql += " ORDER BY created_at DESC"
        
        # 计算偏移量
        offset = (page - 1) * page_size
        sql += f" LIMIT %s OFFSET %s"
        params.extend([page_size, offset])
        
        cursor.execute(sql, params)
        results = cursor.fetchall()
        
        # 格式化响应
        formatted_results = []
        for row in results:
            formatted_results.append(PatientDataResponse(
                id=row['id'],
                created_at=row['created_at'],
                data=row
            ))
        
        cursor.close()
        connection.close()
        
        return formatted_results
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询失败: {str(e)}")

# 5. 统计分析接口
@admin_router.get("/statistics", response_model=StatisticsResponse)
async def get_statistics(
    start_date: Optional[date] = Query(None, description="开始日期"),
    end_date: Optional[date] = Query(None, description="结束日期")
):
    """获取统计数据"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        
        # 构建日期条件
        date_condition = ""
        params = []
        if start_date and end_date:
            date_condition = "WHERE created_at BETWEEN %s AND %s"
            params = [start_date, end_date]
        elif start_date:
            date_condition = "WHERE created_at >= %s"
            params = [start_date]
        elif end_date:
            date_condition = "WHERE created_at <= %s"
            params = [end_date]
        
        # 统计患者总数
        cursor.execute(f"SELECT COUNT(*) as count FROM patient_general_info {date_condition}", params)
        total_patients = cursor.fetchone()['count']
        
        # 统计预测总数
        cursor.execute(f"SELECT COUNT(*) as count FROM model_fgr_params {date_condition}", params)
        fgr_count = cursor.fetchone()['count']
        
        cursor.execute(f"SELECT COUNT(*) as count FROM model_fgr_neonatal_params {date_condition}", params)
        fgr_neonatal_count = cursor.fetchone()['count']
        
        cursor.execute(f"SELECT COUNT(*) as count FROM model_maternal_cox_params {date_condition}", params)
        maternal_cox_count = cursor.fetchone()['count']
        
        cursor.execute(f"SELECT COUNT(*) as count FROM model_neonatal_cox_params {date_condition}", params)
        neonatal_cox_count = cursor.fetchone()['count']
        
        total_predictions = fgr_count + fgr_neonatal_count + maternal_cox_count + neonatal_cox_count
        
        # 按日期统计数据
        cursor.execute(f"""
        SELECT DATE(created_at) as date, COUNT(*) as count
        FROM patient_general_info
        {date_condition}
        GROUP BY DATE(created_at)
        ORDER BY date DESC
        LIMIT 30
        """, params)
        data_by_date = cursor.fetchall()
        
        # 预测结果分布
        prediction_distribution = {
            "fgr": fgr_count,
            "fgr_neonatal": fgr_neonatal_count,
            "maternal_cox": maternal_cox_count,
            "neonatal_cox": neonatal_cox_count
        }
        
        cursor.close()
        connection.close()
        
        return StatisticsResponse(
            total_patients=total_patients,
            total_predictions=total_predictions,
            data_by_date=data_by_date,
            prediction_distribution=prediction_distribution
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"统计失败: {str(e)}")

# 6. 患者详细信息接口
@admin_router.get("/patients/{patient_id}/detail", response_model=PatientDetailResponse)
async def get_patient_detail(patient_id: int):
    """获取患者详细信息"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        
        # 获取基本信息
        cursor.execute("SELECT * FROM patient_general_info WHERE id = %s", (patient_id,))
        general_info = cursor.fetchone()
        
        # 获取实验室检查数据
        cursor.execute("SELECT * FROM patient_lab_imaging ORDER BY created_at DESC")
        lab_imaging = cursor.fetchall()
        
        # 获取家庭监测数据（不包含文件内容）
        cursor.execute("""
        SELECT id, home_monitoring_date, home_systolic, home_diastolic,
               fetal_heart_rate, fetal_movement, home_sflt1_plgf_ratio,
               CASE WHEN fetal_monitoring_file IS NOT NULL THEN '有文件' ELSE '无文件' END as fetal_monitoring_file_status,
               CASE WHEN urine_test_file IS NOT NULL THEN '有文件' ELSE '无文件' END as urine_test_file_status,
               created_at
        FROM patient_home_monitoring
        ORDER BY created_at DESC
        """)
        home_monitoring = cursor.fetchall()
        
        # 获取预测结果
        predictions = []
        
        # FGR预测
        cursor.execute("SELECT 'fgr' as model_type, * FROM model_fgr_params ORDER BY created_at DESC")
        fgr_predictions = cursor.fetchall()
        predictions.extend(fgr_predictions)
        
        # FGR-Neonatal预测
        cursor.execute("SELECT 'fgr_neonatal' as model_type, * FROM model_fgr_neonatal_params ORDER BY created_at DESC")
        fgr_neonatal_predictions = cursor.fetchall()
        predictions.extend(fgr_neonatal_predictions)
        
        # Maternal-COX预测
        cursor.execute("SELECT 'maternal_cox' as model_type, * FROM model_maternal_cox_params ORDER BY created_at DESC")
        maternal_cox_predictions = cursor.fetchall()
        predictions.extend(maternal_cox_predictions)
        
        # Neonatal-COX预测
        cursor.execute("SELECT 'neonatal_cox' as model_type, * FROM model_neonatal_cox_params ORDER BY created_at DESC")
        neonatal_cox_predictions = cursor.fetchall()
        predictions.extend(neonatal_cox_predictions)
        
        cursor.close()
        connection.close()
        
        return PatientDetailResponse(
            general_info=general_info,
            lab_imaging=lab_imaging,
            home_monitoring=home_monitoring,
            predictions=predictions
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询失败: {str(e)}")

# 7. 数据导出接口
@admin_router.get("/export/patients")
async def export_patients(
    format: str = Query("csv", description="导出格式: csv, json"),
    start_date: Optional[date] = Query(None, description="开始日期"),
    end_date: Optional[date] = Query(None, description="结束日期")
):
    """导出患者数据"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        
        # 构建查询条件
        where_conditions = []
        params = []
        
        if start_date:
            where_conditions.append("created_at >= %s")
            params.append(start_date)
        
        if end_date:
            where_conditions.append("created_at <= %s")
            params.append(end_date)
        
        where_clause = " WHERE " + " AND ".join(where_conditions) if where_conditions else ""
        
        # 查询数据
        sql = f"""
        SELECT p.*, 
               l.examination_date, l.rbc_count, l.wbc_count, l.hemoglobin,
               h.home_monitoring_date, h.home_systolic, h.home_diastolic
        FROM patient_general_info p
        LEFT JOIN patient_lab_imaging l ON p.id = l.id
        LEFT JOIN patient_home_monitoring h ON p.id = h.id
        {where_clause}
        ORDER BY p.created_at DESC
        """
        
        cursor.execute(sql, params)
        results = cursor.fetchall()
        
        cursor.close()
        connection.close()
        
        if format.lower() == "json":
            return {"data": results}
        else:
            # CSV格式（简化处理）
            return {"data": results, "format": "csv"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"导出失败: {str(e)}")

# 8. 系统健康检查接口
@admin_router.get("/health")
async def admin_health_check():
    """后台管理系统健康检查"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # 检查各表记录数
        tables = [
            'patient_general_info',
            'patient_lab_imaging', 
            'patient_home_monitoring',
            'model_fgr_params',
            'model_fgr_neonatal_params',
            'model_maternal_cox_params',
            'model_neonatal_cox_params'
        ]
        
        table_stats = {}
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) as count FROM {table}")
            count = cursor.fetchone()[0]
            table_stats[table] = count
        
        cursor.close()
        connection.close()
        
        return {
            "status": "healthy",
            "database": "connected",
            "table_statistics": table_stats,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        } 