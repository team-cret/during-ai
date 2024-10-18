import logging
import re
from datetime import datetime, timedelta
from tqdm import tqdm

from database.db import DB
from model.data_model import CoupleChat, ConnectionLog, Report, ReportRequest
from setting.service_config import ServiceConfig
from setting.logger_setting import logger_setting

class StatisticalAnalyzer:
    def __init__(self):
        self.setup_for_test()
        logger_setting()
        self.logger = logging.getLogger(__name__)

    def setup_for_test(self):
        self.db = DB()
        self.statistical_report:Report = Report()

    def analyze_statistics(self, couple_chat:list[CoupleChat], report_request:ReportRequest):
        try:
            self.couple_chat = couple_chat
            self.report_request = report_request

            self.analyze_response_time_zone()
            self.analyze_concurrent_time_zone()
            self.analyze_frequently_used_motion()
            self.analyze_number_of_love_words()
            self.analyze_average_reply_term()

            return self.statistical_report
        except Exception as e:
            self.logger.error(f"Error in analyzing statistics: {str(e)}", exc_info=True)
            raise Exception("Error in analyzing statistics")

    def analyze_response_time_zone(self):
        try:
            response_time_zone = [0 for _ in range(round(1440/ServiceConfig.REPORT_RESPONSE_TIME_ZONE_UNIT.value))]
            for chat in self.couple_chat:
                response_time_zone[
                    (chat.timestamp.hour * 60 + chat.timestamp.minute) // 
                    ServiceConfig.REPORT_RESPONSE_TIME_ZONE_UNIT.value
                ] += 1
            self.statistical_report.response_time_zone = response_time_zone
        except Exception as e:
            self.logger.error(f"Error in analyzing response time zone: {str(e)}", exc_info=True)
            raise Exception("Error in analyzing response time zone")
        
    def analyze_concurrent_time_zone(self) -> None:
        try:
            # couple log generation
            self.couple_logs = {}
            for user_id in self.report_request.couple_member_ids:
                self.couple_logs[user_id] = self.db.get_member_activity(user_id)
            
            # self.generate_dataset()

            # user_id -> couple range extract
            couple_range = {}
            for user_id, user_logs in self.couple_logs.items():
                if len(user_logs) == 0:
                    return
                
                if user_logs[0].connection_type == ServiceConfig.DB_CONNECTION_LOGOUT.value:
                    user_logs = [
                        ConnectionLog(
                            user_id = user_id,
                            connection_type = ServiceConfig.DB_CONNECTION_LOGIN.value,
                            timestamp = self.report_request.start_date,
                        )
                    ] + user_logs
                if user_logs[-1].connection_type == ServiceConfig.DB_CONNECTION_LOGIN.value:
                    user_logs.append(
                        ConnectionLog(
                            user_id = user_id,
                            connection_type = ServiceConfig.DB_CONNECTION_LOGOUT.value,
                            timestamp = self.report_request.end_date,
                        )
                    )
                
                couple_range[user_id] = []
                start_time = None
                end_time = None
                for user_log in user_logs:
                    if user_log.connection_type == ServiceConfig.DB_CONNECTION_LOGIN.value:
                        if end_time != None:
                            couple_range[user_log.user_id].append([start_time, end_time])
                            start_time = None
                            end_time = None
                        if start_time == None:
                            start_time = user_log.timestamp
                    elif user_log.connection_type == ServiceConfig.DB_CONNECTION_LOGOUT.value:
                        end_time = user_log.timestamp
            
            couple_range_list = list(couple_range.values())
            combined_time_range = couple_range_list[0]
            for couple_range in couple_range_list[1:]:
                combined_time_range = self.combine_couple_range(combined_time_range, couple_range)
            
            concurrent_time_zone = self.range_to_time_zone(combined_time_range)

            self.statistical_report.concurrent_time_zone = concurrent_time_zone
        except Exception as e:
            self.logger.error(f"Error in analyzing concurrent time zone: {str(e)}", exc_info=True)
            raise Exception("Error in analyzing concurrent time zone")
        
    def range_to_time_zone(self, time_range:tuple[datetime, datetime]) -> list[float]:
        try:
            modulo = round(1440/ServiceConfig.REPORT_RESPONSE_TIME_ZONE_UNIT.value)
            concurrent_time_zone = [0 for _ in range(modulo)]

            for start, end in tqdm(time_range):
                start:datetime
                end:datetime

                unit = ServiceConfig.REPORT_RESPONSE_TIME_ZONE_UNIT.value

                start_date = datetime(start.year, start.month, start.day)
                end_date = datetime(end.year, end.month, end.day)
                start_time = start - start_date
                end_time = end - end_date

                days_difference = (end_date - start_date).days
                concurrent_time_zone = [(days_difference - (start_date == end_date)) * unit + concurrent_time_zone[i] for i in range(modulo)]

                concurrent_time_zone[int(start_time.seconds) // (unit * 60)] = unit - float(start_time.seconds % (unit * 60)) / 60
                concurrent_time_zone[int(end_time.seconds) // (unit * 60)] = float(end_time.seconds % (unit * 60)) / 60
                for i in range(int(start_time.seconds) // (unit * 60) + 1, modulo):
                    concurrent_time_zone[i] += unit
                
                for i in range(0, end_time.seconds // (unit * 60)):
                    concurrent_time_zone[i] += unit
            return concurrent_time_zone
        except Exception as e:
            self.logger.error(f"Error in converting range to time zone: {str(e)}", exc_info=True)
            raise Exception("Error in converting range to time zone")
        
    def combine_couple_range(self, user_log1:list[tuple[datetime, datetime]], user_log2:list[tuple[datetime, datetime]]) -> list[tuple[datetime, datetime]]:
        try:
            combined_time_range = []
            i = 0
            j = 0
            while i < len(user_log1) and j < len(user_log2):
                four_point_sorting = sorted([(0, user_log1[i][0]), (0, user_log2[j][0]), (1, user_log1[i][1]), (1, user_log2[j][1])], key=lambda x:x[1])
                if four_point_sorting[0][1] != four_point_sorting[1][1]:
                    combined_time_range.append((four_point_sorting[1][1], four_point_sorting[2][1]))

                if user_log1[i][1] < user_log2[j][1]:
                    i += 1
                else:
                    j += 1
            return combined_time_range
        except Exception as e:
            self.logger.error(f"Error in combining couple range: {str(e)}", exc_info=True)
            raise Exception("Error in combining couple range")
    
    # def generate_dataset(self):
    #     # test data
    #     from random import randint

    #     randnum = 1000

    #     diff = self.report_request.end_date - self.report_request.start_date
    #     rand_value1 = sorted([randint(1, int(diff.days * 86400 + diff.seconds)) for _ in range(randnum)])
    #     rand_value2 = sorted([randint(1, int(diff.days * 86400 + diff.seconds)) for _ in range(randnum)])
    #     datetimes1 = [self.report_request.start_date + timedelta(seconds=rand_value1[i]) for i in range(randnum)]
    #     datetimes2 = [self.report_request.start_date + timedelta(seconds=rand_value2[i]) for i in range(randnum)]

    #     for i in range(randnum):
    #         self.couple_logs[ServiceConfig.DB_TEST_USER_ID_1.value].append(
    #             ConnectionLog(
    #                 user_id = ServiceConfig.DB_TEST_USER_ID_1.value,
    #                 connection_type = ServiceConfig.DB_CONNECTION_LOGIN.value if i % 2 == 0 else ServiceConfig.DB_CONNECTION_LOGOUT.value,
    #                 timestamp = datetimes1[i],
    #             )
    #         )
    #         self.couple_logs[ServiceConfig.DB_TEST_USER_ID_2.value].append(
    #             ConnectionLog(
    #                 user_id = ServiceConfig.DB_TEST_USER_ID_2.value,
    #                 connection_type = ServiceConfig.DB_CONNECTION_LOGIN.value if i % 2 == 0 else ServiceConfig.DB_CONNECTION_LOGOUT.value,
    #                 timestamp = datetimes2[i],
    #             )
    #         )
    
    def analyze_frequently_used_motion(self):
        try:
            motions = {}
            for chat in self.couple_chat:
                if chat.chat_type == ServiceConfig.CHAT_TYPE_MOTION.value:
                    if motions[chat.message] == None:
                        motions[chat.message] = 1
                    else:
                        motions[chat.message] += 1
            
            self.statistical_report.frequently_used_emotion = sorted(
                list(motions.items()),
                key=lambda x: -x[1],
            )[:6]
        except Exception as e:
            self.logger.error(f"Error in analyzing frequently used motion: {str(e)}", exc_info=True)
            raise Exception("Error in analyzing frequently used motion")

    def analyze_number_of_love_words(self):
        try:
            love_words = '|'.join(['사랑해'])
            num = 0
            for chat in self.couple_chat:
                num += len(re.findall(love_words, chat.message))

            self.statistical_report.number_of_love_words = num
        except Exception as e:
            self.logger.error(f"Error in analyzing number of love words: {str(e)}", exc_info=True)
            raise Exception("Error in analyzing number of love words")

    def analyze_average_reply_term(self):
        try:
            time_period = self.couple_chat[-1].timestamp - self.couple_chat[0].timestamp
            self.statistical_report.average_reply_term = time_period / len(self.couple_chat)
        except Exception as e:
            self.logger.error(f"Error in analyzing average reply term: {str(e)}", exc_info=True)
            raise Exception("Error in analyzing average reply term")