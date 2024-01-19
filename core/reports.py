from .models import *
from .serializers import *

from .utils import get_formatted_date

class Report:
    def __init__(self, type, request):
        self.type = type 
        self.request = request
        self.date = get_formatted_date()
    
    def get_report(self):
        function_map = {
            "occupancy_trends": self.get_occupancy_trends(),
            # "revenue_analysis": self.get_revenue_analysis(),
            # "time_analysis": self.get_time_analysis(),
            # "usage_patterns": self.get_usage_patterns(),
            # "peak_usage_hours": self.get_peak_usage_hours(),
            # "session_duration": self.get_session_duration(),
            # "session_distribution": self.get_session_distribution(),
            # "user_activity": self.get_user_activity(),
        }
        return function_map[self.type]
    
    def get_occupancy_trends(self):
        tmp_parking_lots = ParkingLot.objects.all()
        parking_lots = ParkingLotSerializer(tmp_parking_lots, many=True, context={'request': self.request}).data
        total_slots, total_occupied_slots, overall_percentage = 0, 0, 0
        parking_lot_details = []
        for lot in parking_lots:
            tmp = lot['occupancy'].split('/')
            total_occupied_slots += int(tmp[0])
            total_slots += int(tmp[1])
            parking_lot_details.append({
                "name": lot['name'],
                "percentage_occupancy": round(int(tmp[0])/int(tmp[1]) * 100, 2),
                "occupancy": lot['occupancy']
            })
        overall_percentage = round((total_occupied_slots/total_slots) * 100, 2)
        return {
            "date": self.date,
            "overall_percentage": overall_percentage,
            "overall_occupancy": f"{total_occupied_slots}/{total_slots}",
            "parking_lot_details": parking_lot_details
        }
