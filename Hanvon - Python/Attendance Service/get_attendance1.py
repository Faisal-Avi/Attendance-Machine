import sqlite3
import socketserver, time, cx_Oracle
from datetime import datetime, timedelta

HOST = "192.168.66.24"
PORT = 9920

class GetAttendance(socketserver.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print("{} wrote:".format(self.client_address[0]))
        print(self.data)
        self.in_attendance_device_code = ''
        self.in_verify_method = ''
        self.in_attendance_dttm = ''
        self.in_device_ip = self.client_address[0]
        self.in_input_type = ''
        self.out_error_code = ''
        self.out_error_text = ''
        with open('D:\\Attendance Service\\ip_vs_database.txt') as ips:
            for ip in ips:
                if ip.startswith(self.in_device_ip):
                    self.db = ip.split()[1]
                    break                
        
        try:
            if self.db:
                self.con = cx_Oracle.connect(self.db)
                self.cur = self.con.cursor()
        except:
            pass
              
        if self.data.decode('utf-8').startswith('PostRecord'):
        
            self.request.sendall(bytes('Return(result="success" postphoto="false")', 'utf-8'))
            while self.data and self.data.decode('utf-8').find('fail') < 0:
                self.data = self.request.recv(1024).strip()
                self.present_time = datetime.now()
                self.success_failure_ind = "failed"
                if self.data.decode('utf-8').find('name') >= 0:
                    self.AttendanceData = self.data.decode('utf-8').replace('Record(', '').replace(')', '').split('"')
                    print(self.AttendanceData)
                    time.sleep(.2)
                    self.in_attendance_device_code = self.AttendanceData[3]
                    self.in_verify_method = self.AttendanceData[9]
                    self.in_attendance_dttm = datetime.strptime(self.AttendanceData[1], '%Y-%m-%d %H:%M:%S')
                    self.conn = sqlite3.connect('D:\\Attendance Service\\attendance.db')
                    self.c = self.conn.cursor()
                    self.c.execute("INSERT INTO attendance_detail VALUES (?, ? , ? )", (self.in_attendance_device_code, self.in_attendance_dttm , self.in_device_ip))
                    self.conn.commit()
                    if self.db:
                        self.cur.callproc("hrm_payroll.process_attend_device_punch", [self.in_attendance_device_code, self.in_verify_method, self.in_attendance_dttm, self.in_device_ip, self.in_input_type, self.out_error_code, self.out_error_text])
                        self.con.commit()
                        
        elif self.data.decode('utf-8').startswith('GetRequest'):
        
            self.request.sendall(bytes('Return(result="success" postphoto="false")', 'utf-8'))
            while self.data and self.data.decode('utf-8').find('fail') < 0:
                self.data = self.request.recv(1024).strip()
                self.present_time = datetime.now()
                self.success_failure_ind = "failed"
                if self.data.decode('utf-8').find('name') >= 0:
                    self.AttendanceData = self.data.decode('utf-8').replace('Record(', '').replace(')', '').split('"')
                    print(self.AttendanceData)
                    time.sleep(.2)
                    self.in_attendance_device_code = self.AttendanceData[3]
                    self.in_verify_method = self.AttendanceData[9]
                    self.in_attendance_dttm = datetime.strptime(self.AttendanceData[1], '%Y-%m-%d %H:%M:%S')
                    self.conn = sqlite3.connect('D:\\Attendance Service\\attendance.db')
                    self.c = self.conn.cursor()
                    self.c.execute("INSERT INTO attendance_detail VALUES (?, ? , ? )", (self.in_attendance_device_code, self.in_attendance_dttm , self.in_device_ip))
                    self.conn.commit()
                    if self.db:
                        self.cur.callproc("hrm_payroll.process_attend_device_punch", [self.in_attendance_device_code, self.in_verify_method, self.in_attendance_dttm, self.in_device_ip, self.in_input_type, self.out_error_code, self.out_error_text])
                        self.con.commit()
                        
                        
                        
        #self.request.sendall(bytes('Return(result="' + self.success_failure_ind + '" postphoto="false")', 'utf-8'))
        self.request.sendall(self.data.upper())
        
        if self.con:
            self.con.close()
            
if __name__ == "__main__":
    server = socketserver.TCPServer((HOST, int(PORT)), GetAttendance)
    server.serve_forever()