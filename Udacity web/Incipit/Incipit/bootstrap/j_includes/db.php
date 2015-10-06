<?php
if(!class_exists('sankyDatabase')){
	class sankyDatabase {
	
		function sankyDatabase() {
			return $this->__construct();
		}
		
		function __construct() {
			$this->connect();
		}
	
		function connect() {
			$link = mysql_connect('localhost', DB_USER, DB_PASS);

			if (!$link) {
				die('Could not connect: ' . mysql_error());
			}

			$db_selected = mysql_select_db(DB_NAME, $link);

			if (!$db_selected) {
				die('Can\'t use ' . DB_NAME . ': ' . mysql_error());
			}
		}
		
		function clean($array) {
			return array_map('mysql_real_escape_string', $array);
		}
		
		function hash_password($password, $nonce) {
		  $secureHash = hash_hmac('sha512', $password . $nonce, SITE_KEY);
		  
		  return $secureHash;
		}
		
		function insert($link, $table, $fields, $values) {
			$fields = implode(", ", $fields);
			$values = implode("', '", $values);
			$sql="INSERT INTO $table (id, $fields) VALUES ('', '$values')";

			if (!mysql_query($sql)) {
				die('Error: ' . mysql_error());
			} else {
				return TRUE;
			}
		}
		
		function select($sql) {
			$results = mysql_query($sql);
			
			return $results;
		}
	}
}
$jdb = new sankyDatabase;
?>