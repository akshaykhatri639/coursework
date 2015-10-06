<?php

if(!class_exists('sanky')){
	class sanky {
		
		function register($redirect) {
			global $jdb;
			if ( !empty ( $_POST ) ) {
					require_once('db.php');
					$table = 'i_users';
					$fields = array('user_fname', 'user_lname', 'user_email', 'user_pass', 'user_bdate', 'user_rdate');
					$values = $jdb->clean($_POST);
					$userfname = $_POST['fname'];
                    $userlname = $_POST['lname'];
					$userlogin = $_POST['email'];
					$userpass = $_POST['pass'];
					$userbdate = $_POST['bdate'];
					$userreg = $_POST['date'];
                    
                    
                    $sql = "SELECT * FROM $table WHERE user_email = '" . $userlogin . "'";
                    $result = mysql_query($sql);
				//    if ($result) {
				//	   die('Sorry, email is already registered');
				//    }
					$nonce = md5('registration-' . $userlogin . $userreg . NONCE_SALT);
					$userpass = $jdb->hash_password($userpass, $nonce);
					$values = array(
								'fname' => $userfname,
                        		'lname' => $userlname,
                                'email' => $userlogin,
								'pass' => $userpass,
								'bdate' => $userbdate,
                                'date' => $userreg
							);
					$insert = $jdb->insert($link, $table, $fields, $values);
					
					if ( $insert == TRUE ) {
						$url = "http" . ((!empty($_SERVER['HTTPS'])) ? "s" : "") . "://".$_SERVER['SERVER_NAME'].$_SERVER['REQUEST_URI'];
						$aredirect = str_replace('register.php', 'index.php', $url);
						
						header("Location: $redirect?reg=true");
						exit;
					}
			}
		}
		
		function login($redirect) {
			global $jdb;
		
			if ( !empty ( $_POST ) ) {
				$values = $jdb->clean($_POST);
				$subname = $_POST['email'];
                $subpass = $values['pass'];
				$table = 'i_users';
				$sql = "SELECT * FROM $table WHERE user_email = '" . $subname . "'";
				$results = $jdb->select($sql);
				if (!$results) {
					die('Sorry, that username does not exist!');
				}

				$results = mysql_fetch_assoc( $results );

                $storeg = $results['user_rdate'];

				$stopass = $results['user_pass'];

				$nonce = md5('registration-' . $subname . $storeg . NONCE_SALT);

				$subpass = $jdb->hash_password($subpass, $nonce);

				if ( $subpass == $stopass ) {
					
					$authnonce = md5('cookie-' . $subname . $storeg . AUTH_SALT);
					$authID = $jdb->hash_password($subpass, $authnonce);
					
					setcookie('logauth[user]', $subname, 0, '', '', '', true);
					setcookie('logauth[authID]', $authID, 0, '', '', '', true);
					
				
                	header("Location: $redirect");   
                    exit;	
				} else {
					return 'invalid';
				}
			} else {
				return 'empty';
			}
		}
		
		function logout() {
			$idout = setcookie('logauth[authID]', '', -3600, '', '', '', true);
			$userout = setcookie('logauth[user]', '', -3600, '', '', '', true);
			
			if ( $idout == true && $userout == true ) {
				return true;
			} else {
				return false;
			}
		}
		
		function checkLogin() {
			global $jdb;
		if(isset($_COOKIE['logauth'])){
			$cookie = $_COOKIE['logauth'];
			
			$user = $cookie['user'];
			$authID = $cookie['authID'];
			
			if ( !empty ( $cookie ) ) {
				
				$table = 'i_users';
				$sql = "SELECT * FROM $table WHERE user_email = '" . $user . "'";
				$results = $jdb->select($sql);

				if (!$results) {
					die('Sorry, that username does not exist!');
				}

				$results = mysql_fetch_assoc( $results );
		
				$storeg = $results['user_rdate'];

				$stopass = $results['user_pass'];

				$authnonce = md5('cookie-' . $user . $storeg . AUTH_SALT);
				$stopass = $jdb->hash_password($stopass, $authnonce);
				
				if ( $stopass == $authID ) {
					$results = true;
                    header("Location: home.php");    
				} else {
					$results = false;
                    header("Location: index.php");
				}
			} else {
				
                $url = "http" . ((!empty($_SERVER['HTTPS'])) ? "s" : "") . "://".$_SERVER['SERVER_NAME'].$_SERVER['REQUEST_URI'];
				$redirect = str_replace('index.php', 'login.php', $url);
				
				header("Location: $redirect");
               
            	exit;
			}
			}
			if(isset($results))
				return $results;
		}
	}
}

$j = new sanky;
?>