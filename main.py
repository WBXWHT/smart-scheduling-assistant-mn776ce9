import json
import random
import datetime
from typing import List, Dict, Any

class SmartSchedulingAssistant:
    """智能排产助手核心类"""
    
    def __init__(self):
        # 模拟历史工单数据
        self.history_orders = self._load_history_data()
        # 模拟设备信息
        self.equipments = [
            {"id": "EQ001", "type": "CNC", "capacity": 8, "status": "idle"},
            {"id": "EQ002", "type": "Assembly", "capacity": 10, "status": "idle"},
            {"id": "EQ003", "type": "Painting", "capacity": 6, "status": "idle"}
        ]
        # 约束参数（模拟通过历史数据优化的参数）
        self.constraints = {
            "max_daily_hours": 20,
            "min_batch_size": 5,
            "priority_weight": 0.7,
            "equipment_utilization_target": 0.85
        }
    
    def _load_history_data(self) -> List[Dict]:
        """加载历史工单数据（模拟）"""
        return [
            {"order_id": "ORD001", "product": "A", "quantity": 100, "deadline": "2024-01-15", "priority": "high"},
            {"order_id": "ORD002", "product": "B", "quantity": 50, "deadline": "2024-01-20", "priority": "medium"},
            {"order_id": "ORD003", "product": "C", "quantity": 200, "deadline": "2024-01-10", "priority": "high"}
        ]
    
    def _simulate_llm_analysis(self, order: Dict, constraints: Dict) -> Dict:
        """模拟大模型分析生产约束并生成排产建议"""
        # 在实际项目中，这里会调用GPT-4等大模型API
        # 这里用规则模拟大模型的推理过程
        
        # 计算预计工时
        base_hours = order["quantity"] / 10
        priority_factor = 1.2 if order["priority"] == "high" else 1.0
        
        # 模拟大模型考虑约束条件
        adjusted_hours = base_hours * priority_factor
        if adjusted_hours > constraints["max_daily_hours"]:
            adjusted_hours = constraints["max_daily_hours"]
        
        # 分配设备（模拟大模型的优化决策）
        suitable_equipments = [eq for eq in self.equipments 
                              if eq["capacity"] >= order["quantity"] / 20]
        
        return {
            "order_id": order["order_id"],
            "estimated_hours": round(adjusted_hours, 1),
            "suggested_equipments": [eq["id"] for eq in suitable_equipments[:2]],
            "start_date": self._calculate_start_date(order["deadline"], adjusted_hours),
            "confidence_score": round(random.uniform(0.7, 0.95), 2)  # 模拟置信度
        }
    
    def _calculate_start_date(self, deadline: str, hours_needed: float) -> str:
        """根据交期和所需工时计算建议开始日期"""
        deadline_date = datetime.datetime.strptime(deadline, "%Y-%m-%d")
        days_needed = max(1, int(hours_needed / 8))  # 按8小时/天计算
        start_date = deadline_date - datetime.timedelta(days=days_needed + 2)  # 预留缓冲
        return start_date.strftime("%Y-%m-%d")
    
    def generate_schedule(self, new_orders: List[Dict]) -> Dict[str, Any]:
        """生成智能排产方案"""
        print("正在分析生产约束...")
        print(f"使用优化后的约束参数: {self.constraints}")
        
        schedule_results = []
        total_utilization = 0
        
        for order in new_orders:
            # 模拟大模型分析每个订单
            analysis = self._simulate_llm_analysis(order, self.constraints)
            schedule_results.append(analysis)
            
            # 计算设备利用率（模拟）
            utilization = min(0.95, analysis["confidence_score"] * 1.1)
            total_utilization += utilization
            
            print(f"订单 {order['order_id']}: 预计工时{analysis['estimated_hours']}小时, "
                  f"建议设备{analysis['suggested_equipments']}")
        
        # 计算平均接受率（模拟从60%提升到85%）
        avg_acceptance_rate = 0.60 + (self.constraints["priority_weight"] * 0.25)
        avg_acceptance_rate = min(0.85, avg_acceptance_rate)
        
        avg_utilization = total_utilization / len(new_orders) if new_orders else 0
        
        return {
            "schedule": schedule_results,
            "summary": {
                "total_orders": len(new_orders),
                "avg_acceptance_rate": round(avg_acceptance_rate, 2),
                "avg_equipment_utilization": round(avg_utilization, 2),
                "estimated_delivery_reduction": "18%"  # 模拟交付周期缩短
            },
            "constraints_used": self.constraints
        }
    
    def display_schedule(self, schedule_result: Dict):
        """可视化展示排产方案"""
        print("\n" + "="*50)
        print("智能排产方案生成完成")
        print("="*50)
        
        print("\n详细排产计划:")
        for item in schedule_result["schedule"]:
            print(f"- 订单 {item['order_id']}:")
            print(f"  开始日期: {item['start_date']}")
            print(f"  预计工时: {item['estimated_hours']}小时")
            print(f"  推荐设备: {', '.join(item['suggested_equipments'])}")
            print(f"  置信度: {item['confidence_score']*100}%")
        
        print("\n方案摘要:")
        summary = schedule_result["summary"]
        print(f"总订单数: {summary['total_orders']}")
        print(f"预计方案接受率: {summary['avg_acceptance_rate']*100}%")
        print(f"平均设备利用率: {summary['avg_equipment_utilization']*100}%")
        print(f"预计交付周期缩短: {summary['estimated_delivery_reduction']}")
        
        print("\n使用的约束参数:")
        for key, value in schedule_result["constraints_used"].items():
            print(f"  {key}: {value}")


def main():
    """主函数 - 智能排产助手演示"""
    print("智能排产助手启动...")
    print("模拟B端AI产品场景: 中小型制造企业生产排产优化\n")
    
    # 创建智能排产助手实例
    assistant = SmartSchedulingAssistant()
    
    # 模拟新订单数据
    new_orders = [
        {"order_id": "ORD202401", "product": "D", "quantity": 150, 
         "deadline": "2024-01-25", "priority": "high"},
        {"order_id": "ORD202402", "product": "E", "quantity": 80, 
         "deadline": "2024-01-28", "priority": "medium"},
        {"order_id": "ORD202403", "product": "F", "quantity": 120, 
         "deadline": "2024-01-30", "priority": "high"}
    ]
    
    print(f"收到 {len(new_orders)} 个新订单:")
    for order in new_orders:
        print(f"- {order['order_id']}: {order['product']} x{order['quantity']}, "
              f"交期 {order['deadline']}, 优先级 {order['priority']}")
    
    # 生成智能排产方案
    print("\n" + "-"*50)
    schedule_result = assistant.generate_schedule(new_orders)
    
    # 展示排产方案
    assistant.display_schedule(schedule_result)
    
    print("\n" + "="*50)
    print("演示完成 - 模拟AI产品从数据分析到方案生成的完整流程")
    print("="*50)


if __name__ == "__main__":
    main()