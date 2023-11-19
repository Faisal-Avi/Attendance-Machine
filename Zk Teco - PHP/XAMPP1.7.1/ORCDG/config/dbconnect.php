<?php
date_default_timezone_set('Etc/GMT-6');	
$db = oci_connect("bottomerp", "dekkkoerp#sdi#","192.168.0.217:1521/DCOPRODDB1");
if(!($db))
trigger_error("Could not connect to the database", E_USER_ERROR);
?>