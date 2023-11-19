import socketserver, time, cx_Oracle
from datetime import datetime, timedelta

with open('server_ip.config') as host:
    HOST, PORT = host.readline().split()

class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.in_device_ip = self.client_address[0]
        self.con = ''
        self.connstring = ''

        self.con_exception = ''
        self.connstring_exception = ''
        self.card_no = ''
        try:
            with open('client_ip.config') as clients:
                for client in clients:
                    if client.startswith(self.in_device_ip):
                        self.connstring = client.split()[1]
                        print(self.connstring)
                        break

            if self.connstring:
                self.con = cx_Oracle.connect(self.connstring)
                self.cur = self.con.cursor()

            self.out_error_code = ''
            self.out_error_text = ''
        except Exception as e:
            print('Exception: ' + str(e))

        if self.connstring:
            self.data = self.request.recv(2048).strip()
            print(self.data)

            if self.data.decode('utf-8').startswith('PostRecord'):
                print('In post record block')
                self.request.sendall(bytes('Return(result="success" postphoto="false")', 'utf-8'))
                while self.data and self.data.decode('utf-8').find('fail') < 0:
                    self.data = self.request.recv(2048).strip()
                    self.present_time = datetime.now()
                    self.success_failure_ind = "failed"

                    if self.data.decode('utf-8').find('name') >= 0:
                        self.attData = self.data.decode('utf-8').replace('Record(', '').replace(')', '').split('"')
                        print(self.attData)
                        self.in_attendance_device_code = self.attData[3]
                        self.in_verify_method = self.attData[9]
                        self.in_attendance_dttm = datetime.strptime(self.attData[1], '%Y-%m-%d %H:%M:%S')
                        # self.in_device_ip = self.client_address[0]
                        self.in_input_type = "Face"
                        # self.present_time = datetime.now()
                        self.previous_year = datetime.now() - timedelta(days=365)
                        self.present_hour = int(self.present_time.strftime("%H"))
                        self.success_failure_ind = "success" if self.present_hour >= 9 and self.present_hour <= 18 else "failed"

                        try:
                            if self.in_attendance_device_code != '' and (self.in_attendance_dttm <= self.present_time + timedelta(seconds=300) and self.in_attendance_dttm > self.previous_year):
                                try:
                                    with open('exception_cards.config') as cards:
                                        for card in cards:
                                            if card.split()[0] == self.in_attendance_device_code:
                                                self.connstring_exception = card.split()[1]
                                                break

                                    if self.connstring_exception:
                                        self.con_exception = cx_Oracle.connect(self.connstring_exception)
                                        self.cur_exception = self.con_exception.cursor()

                                        try:
                                            if self.in_attendance_device_code != '' and (self.in_attendance_dttm <= self.present_time + timedelta(seconds=300) and self.in_attendance_dttm > self.previous_year):
                                                self.cur_exception.callproc("hrm_payroll.process_attend_device_punch", [self.in_attendance_device_code, self.in_verify_method, self.in_attendance_dttm, self.in_device_ip, self.in_input_type, self.out_error_code, self.out_error_text])
                                                self.con_exception.commit()
                                        except Exception as e:
                                            print('Exception: ' + str(e))

                                        if self.con_exception:
                                            self.con_exception.close()
                                            self.con_exception = ''
                                            self.connstring_exception = ''
                                            self.card_no = ''
                                    else:
                                        try:
                                            if self.in_attendance_device_code != '' and (self.in_attendance_dttm <= self.present_time + timedelta(seconds=300) and self.in_attendance_dttm > self.previous_year):
                                                self.cur.callproc("hrm_payroll.process_attend_device_punch", [self.in_attendance_device_code, self.in_verify_method, self.in_attendance_dttm, self.in_device_ip, self.in_input_type, self.out_error_code, self.out_error_text])
                                                self.con.commit()
                                        except Exception as e:
                                            print('Exception: ' + str(e))
                                except Exception as e:
                                    print('Exception: ' + str(e))
                        except Exception as e:
                            print('Exception: ' + str(e))

                    # self.request.sendall(bytes('Return(result="failed" postphoto="false")', 'utf-8'))
                    self.request.sendall(bytes('Return(result="' + self.success_failure_ind + '" postphoto="false")', 'utf-8'))
                    #print('Server Time: ' + self.present_time.strftime('%Y-%m-%d %H:%M:%S') + ' Device: ' + self.in_device_ip + ' >> ' + self.data.decode('utf-8'))
            elif self.data.decode('utf-8').startswith('GetRequest'):
                print('In get request block')
                self.data = self.request.recv(2048).strip()
                print(self.data)
                while self.data and self.data.decode('utf-8').find('fail') >= 0:
                    self.data = self.request.recv(2048).strip()
                    self.present_time = datetime.now()
                    self.success_failure_ind = "failed"

                    if self.data.decode('utf-8').find('name') >= 0:
                        self.attData = self.data.decode('utf-8').replace('Record(', '').replace(')', '').split('"')
                        print(self.attData)
                        self.in_attendance_device_code = self.attData[3]
                        self.in_verify_method = self.attData[9]
                        self.in_attendance_dttm = datetime.strptime(self.attData[1], '%Y-%m-%d %H:%M:%S')
                        # self.in_device_ip = self.client_address[0]
                        self.in_input_type = "Face"
                        # self.present_time = datetime.now()
                        self.previous_year = datetime.now() - timedelta(days=365)
                        self.present_hour = int(self.present_time.strftime("%H"))
                        self.success_failure_ind = "success" if self.present_hour >= 9 and self.present_hour <= 18 else "failed"

                        try:
                            if self.in_attendance_device_code != '' and (self.in_attendance_dttm <= self.present_time + timedelta(seconds=300) and self.in_attendance_dttm > self.previous_year):
                                try:
                                    with open('exception_cards.config') as cards:
                                        for card in cards:
                                            if card.split()[0] == self.in_attendance_device_code:
                                                self.connstring_exception = card.split()[1]
                                                break

                                    if self.connstring_exception:
                                        self.con_exception = cx_Oracle.connect(self.connstring_exception)
                                        self.cur_exception = self.con_exception.cursor()

                                        try:
                                            if self.in_attendance_device_code != '' and (self.in_attendance_dttm <= self.present_time + timedelta(seconds=300) and self.in_attendance_dttm > self.previous_year):
                                                self.cur_exception.callproc("hrm_payroll.process_attend_device_punch", [self.in_attendance_device_code, self.in_verify_method, self.in_attendance_dttm, self.in_device_ip, self.in_input_type, self.out_error_code, self.out_error_text])
                                                self.con_exception.commit()
                                        except Exception as e:
                                            print('Exception: ' + str(e))

                                        if self.con_exception:
                                            self.con_exception.close()
                                            self.con_exception = ''
                                            self.connstring_exception = ''
                                            self.card_no = ''
                                    else:
                                        try:
                                            if self.in_attendance_device_code != '' and (self.in_attendance_dttm <= self.present_time + timedelta(seconds=300) and self.in_attendance_dttm > self.previous_year):
                                                self.cur.callproc("hrm_payroll.process_attend_device_punch", [self.in_attendance_device_code, self.in_verify_method, self.in_attendance_dttm, self.in_device_ip, self.in_input_type, self.out_error_code, self.out_error_text])
                                                self.con.commit()
                                        except Exception as e:
                                            print('Exception: ' + str(e))
                                except Exception as e:
                                    print('Exception: ' + str(e))
                        except Exception as e:
                            print('Exception: ' + str(e))

                    # self.request.sendall(bytes('Return(result="failed" postphoto="false")', 'utf-8'))
                    self.request.sendall(bytes('Return(result="' + self.success_failure_ind + '" postphoto="false")', 'utf-8'))
                    print('Server Time: ' + self.present_time.strftime('%Y-%m-%d %H:%M:%S') + ' Device: ' + self.in_device_ip + ' >> ' + self.data.decode('utf-8'))
            elif not self.data.decode('utf-8').startswith('Quit'):
                self.request.sendall(bytes('Return(result="success")', 'utf-8'))
            else:
                None

            if self.con:
                self.con.close()

if __name__ == "__main__":
    server = socketserver.TCPServer((HOST, int(PORT)), MyTCPHandler)
    server.serve_forever()
