from .models import *
from .serializers import *

from .utils import get_formatted_date, format_number, hours_between_timestamps, process_sessions, convert_timestamp
from operator import itemgetter
from datetime import datetime


class Report:
    def __init__(self, type, request):
        self.type = type
        self.request = request
        self.date = get_formatted_date()

    def get_report(self):
        function_map = {
            "occupancy_trends": self.get_occupancy_trends,
            "revenue_analysis": self.get_revenue_analysis,
            "time_analysis": self.get_time_analysis,
            "usage_patterns": self.get_usage_patterns,
            "peak_usage_hours": self.get_peak_usage_hours,
            "session_duration": self.get_session_duration,
            "session_distribution": self.get_session_distribution,
            "user_activity": self.get_user_activity,
        }
        
        report_function = function_map.get(self.type)
        return report_function()

    def get_occupancy_trends(self):
        tmp_parking_lots = ParkingLot.objects.all()
        parking_lots = ParkingLotSerializer(tmp_parking_lots, many=True, context={
                                            'request': self.request}).data
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

    def get_revenue_analysis(self):
        tmp_parking_sessions = ParkingSession.objects.all()
        parking_sessions = ParkingSessionSerializer(
            tmp_parking_sessions, many=True).data
        total_expected_income = 0
        lot_details = {}
        for session in parking_sessions:
            total_expected_income += session['amount_accumulated']
            try:
                lot_details[session['lot']] += session['amount_accumulated']
            except KeyError:
                lot_details[session['lot']] = 0

        parking_lot_details = []
        for k, v in lot_details.items():
            parking_lot_details.append({
                "name": k,
                "expected_income": format_number(v)
            })

        session_count = tmp_parking_sessions.count()
        return ({
            "date": self.date,
            "total_expected_income": format_number(total_expected_income),
            "session_count": format_number(session_count),
            "parking_lot_details": parking_lot_details
        })

    def get_time_analysis(self):
        tmp_parking_sessions = ParkingSession.objects.all()
        parking_sessions = ParkingSessionSerializer(
            tmp_parking_sessions, many=True).data
        session_count = tmp_parking_sessions.count()
        total_session_duration = 0
        for session in parking_sessions:
            total_session_duration += hours_between_timestamps(
                session['timestamp_start'], session['timestamp_end'])
        average_session_duration = round(
            (total_session_duration/session_count), 2)
        session_data = process_sessions(parking_sessions)
        sorted_session_data = sorted(session_data, key=itemgetter("count"))
        peak_hours = sorted_session_data[:10]
        return ({
            "date": self.date,
            "average_session_duration": average_session_duration,
            "peak_hours": peak_hours,
        })

    def get_usage_patterns(self):
        tmp_parking_sessions = ParkingSession.objects.all()
        parking_sessions = ParkingSessionSerializer(
            tmp_parking_sessions, many=True).data
        results = []
        for session in parking_sessions:
            results.append({
                "session_id": session['uuid'],
                "user_id": session['user'],
                "start_time": session['parked_on']
            })
        return results

    def get_peak_usage_hours(self):
        tmp_parking_sessions = ParkingSession.objects.all()
        parking_sessions = ParkingSessionSerializer(
            tmp_parking_sessions, many=True).data
        session_data = process_sessions(parking_sessions)
        temp = {}
        for i in range(25):
            suf = 'am'
            if i > 12:
                suf = 'pm'
            temp[f"{i}{suf}"] = []
        for session in parking_sessions:
            tmp = session['parked_on'].split(' ')[1]
            hour, min = int(tmp.split(':')[0]), int(tmp.split(':')[1])
            if min > 30:
                hour = hour + 1

            suf = 'am'
            if hour > 12:
                suf = 'pm'
            temp[f"{hour}{suf}"].append(hours_between_timestamps(
                session['timestamp_start'], session['timestamp_end']))
        results = []
        for hour in session_data:
            results.append({
                "hour": hour['time'],
                "count": hour['count'],
                "average_duration": round(sum(temp[hour['time']]) / hour['count'], 2)
            })
        return results

    def get_session_duration(self):
        tmp_parking_sessions = ParkingSession.objects.all()
        parking_sessions = ParkingSessionSerializer(tmp_parking_sessions, many=True).data 
        results = []
        for session in parking_sessions:
            results.append({
                "session_id": session['uuid'],
                "duration": hours_between_timestamps(session['timestamp_start'], session['timestamp_end'])
            })
        return results
    
    def get_session_distribution(self):
        parking_sessions = ParkingSession.objects.all()
        num_of_sessions = {}
        parking_lot_count = {}
        for session in parking_sessions:
            tmp = convert_timestamp(session.timestamp_start)
            date = tmp.split(', ')[0]
    
            if parking_lot_count.get(date):
                try:
                    parking_lot_count[date][session.slot.parking_lot.name] += 1
                except KeyError:
                    parking_lot_count[date][session.slot.parking_lot.name] = 1 
            else:
                parking_lot_count[date] = {}
                parking_lot_count[date][session.slot.parking_lot.name] = 1

            try:
                num_of_sessions[date]['count'] += 1
            except KeyError:
                num_of_sessions[date] = {}
                num_of_sessions[date]['count'] = 1
            
            num_of_sessions[date]['location'] = max(parking_lot_count[date], key=parking_lot_count[date].get)

        results = []
        for k, v in num_of_sessions.items():
            results.append({
                "date": k,
                "count": v['count'],
                "busiest_location": v['location']
            })

        return results
    
    def get_user_activity(self):
        tmp_users = User.objects.all()
        users = UserSerializer(tmp_users, many=True).data 
        results = []
        for user in users:
            results.append({
                "user_id": user['user_id'],
                "sessions": [session['parked_on'] for session in user['sessions']]
            })
        return ({
            "date": self.date,
            "users": results,
        })