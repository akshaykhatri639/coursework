function validatelogin(){

  var email = document.form1.email.value;
  var password = document.form1.password.value;
  var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/ ;
  if (re.test(email)==0){
    alert("Enter a valid email id");
    document.form1.email.focus();
    return false;
  }
  if(password.length < 6){
    alert("Please Enter a valid Password");
    document.form1.password.focus();
    return false;
  }
  return true;

}

function validate(){
var first_name = document.form2.first_name.value;
var last_name = document.form2.last_name.value;
var email = document.form2.email_1.value;
var password = document.form2.password.value;
var password2 = document.form2.password_2.value;
if( first_name == "" )
{
 window.alert( "Please provide your First name!" );
 document.form2.first_name.focus() ;
 return false;
}
if( last_name == "" )
{
 alert( "Please provide your Last name!" );
 document.form2.last_name.focus() ;
 return false;
}

var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
if (re.test(email)== 0)
{
    alert("Enter a  valid email");
    document.form2.email_1.focus() ;
    return false;
}

if(password.length<8)
{
  alert("Password should be greater than 8 characters");
  document.form2.password.focus() ;
  return false;
}  
if (password2 != password){
  alert("Passwords do not match");
  document.form2.password_2.focus() ;
  return false;
}
alert("Signup successfull");
return true;
}

