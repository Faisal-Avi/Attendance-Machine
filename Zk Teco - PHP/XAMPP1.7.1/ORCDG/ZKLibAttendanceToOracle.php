<?php 
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "attendancedg";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);
// Check connection
if ($conn->connect_error) {
	die("Connection failed: " . $conn->connect_error);
}
require_once('config/dbconnect.php');

while(1==1):
	$sel_sql = "SELECT device_code,verify_method,attendance_dttm,device_ip 
				FROM device_attendance 
				WHERE oracle_status = 0
				ORDER BY attendance_dttm ASC";
	$result = $conn->query($sel_sql);
	if ($result->num_rows > 0):
		echo "\n".$result->num_rows.' new records found'."\n";
		while($row = $result->fetch_object()):
			echo $txt = $row->device_code.';'.$row->verify_method.';'.$row->attendance_dttm.';'.$row->device_ip."\n";
			
			//$sql = "begin HRM_PAYROLL.process_attend_device_data(:in_attendance_device_code, :in_verify_method, :in_attendance_dttm, :in_device_ip, :out_error_code, :out_error_text); COMMIT; end;";
			//real// $sql = "begin HRM_PAYROLL.process_attend_device_data('".$row->device_code."', '".$row->verify_method."', TO_DATE('".$row->attendance_dttm."','rrrr-mm-dd hh24:mi:ss'), '".$row->device_ip."', :out_error_code, :out_error_text); COMMIT; end;";
			$sql = "begin HRM_PAYROLL.process_attend_device_punch('".$row->device_code."', '".$row->verify_method."', TO_DATE('".$row->attendance_dttm."','rrrr-mm-dd hh24:mi:ss'), '".$row->device_ip."','Finger', :out_error_code, :out_error_text); COMMIT; end;";
			$stmt = oci_parse($db,$sql);
			$in_attendance_device_code = $row->device_code;
			$in_verify_method = $row->verify_method;
			$in_attendance_dttm = $row->attendance_dttm;
			$in_device_ip = $row->device_ip;
			//oci_bind_by_name($stmt,':in_attendance_device_code',$in_attendance_device_code);
			//oci_bind_by_name($stmt,':in_verify_method',$in_verify_method);
			//oci_bind_by_name($stmt,':in_attendance_dttm',$in_attendance_dttm);
			//oci_bind_by_name($stmt,':in_device_ip',$in_device_ip);
			oci_bind_by_name($stmt,':out_error_code',$l_out_error_code);
			oci_bind_by_name($stmt,':out_error_text',$l_out_error_text);
			oci_execute($stmt);
			echo 'Code : '.$l_out_error_code.';Text : '.$l_out_error_text."\n";
			
			if((time()-(60*60*24*3)) > strtotime($row->attendance_dttm) || (time()+ (60*60*24*3)) < strtotime($row->attendance_dttm)):
				$upd_sql = "UPDATE device_attendance SET oracle_status = 1 
							WHERE device_code='".$row->device_code."' 
							AND attendance_dttm ='".$row->attendance_dttm."' 
							AND device_ip ='".$row->device_ip."'";
				$upd = $conn->query($upd_sql);
				echo $row->attendance_dttm.' >>> Locked from MYSQL'."\n";
			endif;
		endwhile;
	else:
		echo "\n".'No new records found'."\n";
	endif;
	sleep(300);
endwhile;
?>
