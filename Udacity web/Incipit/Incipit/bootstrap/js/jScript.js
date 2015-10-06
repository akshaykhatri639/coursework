function validateForm() {
    var name = document.forms["form1"]["name"].value;
    var pass = document.forms["form1"]["pwd"].value;
    if (name == null || name == "") {
        alert("Name must be filled out");
        document.form1.action = "#";
    }
    if (pass == null || pass == "" ) {
        alert("Password must be filled out");
        document.form1.action = "#";

    }
}
function validateForm2() {
    var fname = document.forms["form2"]["fname"].value;
    var lname = document.forms["form2"]["lname"].value;
    var passval = /\w{7,20}/; 
    var pass = document.forms["form2"]["pass"].value;
    var pass1 = document.forms["form2"]["pass1"].value;
    var date = document.forms["form2"]["date"].value;
    if (fname == null || fname == "") {
        alert("First name must be filled out");
        document.form2.action = "#";
    }
    if (lname == null || lname == "") {
        alert("First name must be filled out");
        document.form2.action = "#";
    }
    if (!pass.match(passval)) {
        alert("Password too short");
        document.form2.action = "#";
    }
    if (pass1 == null || pass1 == ""|| pass != pass1) {
        alert("Passwords not same");
        document.form2.action = "#";
    } 
    if (date == null || date == "") {
        alert("Address must be filled out");
        document.form2.action = "#";

    }
}

function check(x){
    $('#content').load(x);  // here 'test.html' is a page and 'target' id a id of 'test.html'
}
