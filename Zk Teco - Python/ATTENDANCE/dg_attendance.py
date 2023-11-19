from zklib import zklib, zkconst
import time
import cx_Oracle
from datetime import datetime, timedelta

def get_machine_ip():
    with open("D:\\ATTENDANCE\\dg_parameter\\ip_address.txt") as f:
        ip = f.readlines()
    ip = [x.strip() for x in ip] 
    return ip
	
def get_time_list():
    with open("D:\\ATTENDANCE\\dg_parameter\\iteration_time_duration.txt") as f:
        list_time = f.readlines()
    list_time = [x.strip() for x in list_time]
    return list_time

def get_connection_info():
    with open("D:\\ATTENDANCE\\dg_parameter\\db_connection.txt") as f:
        conn_info = f.readlines()
    conn_info = [x.strip() for x in conn_info]
    return conn_info
	
list_machine_ip = get_machine_ip()

print list_machine_ip

list_time_duration = get_time_list()
inner_loop_iteration_duration = float(list_time_duration[0])
middle_loop_iteration_duration = float(list_time_duration[1])
outer_loop_iteration_duration = float(list_time_duration[2])	

list_conn_info = get_connection_info()
db_connection_info = str(list_conn_info[0])

port = "4370"

while 1 == 1:
	try:
		con = cx_Oracle.connect(db_connection_info)
		cur = con.cursor()
		for machine_ip in list_machine_ip:
			zk = zklib.ZKLib(machine_ip, int(port))
			res = zk.connect()
			print res
			print cur
			print machine_ip
			time.sleep(5)
			if res == True:
				try:
					print zk.version()
					print zk.deviceName()
					#zk.getUser()
					att_list = zk.getAttendance()
					t_time = datetime.now()
					h = t_time.hour
					l = len(att_list)	
					print l				
					try:
						for t in att_list:
							try:
								in_attendance_device_code = t[0]
								in_verify_method = t[1]
								in_attendance_dttm = t[2]
								in_device_ip = machine_ip
								out_error_code = ''
								out_error_text = ''
								present_time = datetime.now()
								previous_year = datetime.now() - timedelta(days=365)
								time.sleep(inner_loop_iteration_duration)
								#if in_attendance_device_code != '' and (in_attendance_dttm <= present_time and in_attendance_dttm > previous_year):
								print list(t)
								#cur.callproc("hrm_payroll.attendance_biometric", [in_attendance_device_code, in_verify_method, in_attendance_dttm])
								#cur.callproc("hrm_payroll.process_attend_device_data", [in_attendance_device_code, in_verify_method, in_attendance_dttm, in_device_ip, out_error_code, out_error_text])
								cur.callproc("hrm_payroll.process_attend_device_punch", [in_attendance_device_code, in_verify_method, in_attendance_dttm, in_device_ip,'Finger', out_error_code, out_error_text])
								con.commit()
							except:
								pass
					except:
						pass	
					if l >= 1000 and h >= 3 and h <= 5: #and h == 3
						print 'Clearing att data'
						zk = zklib.ZKLib(machine_ip, int(port))
						conn = zk.connect()
						zk.clearAttendance()
						print 'Data Cleared'
				except:
					pass
			time.sleep(middle_loop_iteration_duration)
	except:
		pass
	time.sleep(outer_loop_iteration_duration)
zk.disconnect()
