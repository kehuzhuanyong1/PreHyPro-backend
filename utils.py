"""
工具函数模块
"""

from datetime import date
import math

def calculate_gestational_days(lmp_date: date, current_date: date) -> int:
    """计算孕天数"""
    return (current_date - lmp_date).days + 14

def calculate_map(sbp: float, dbp: float) -> float:
    """计算平均动脉压"""
    return dbp + (sbp - dbp) / 3 