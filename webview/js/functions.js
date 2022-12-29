const UI_IP = "127.0.0.1"

function cookie_add(key, value) {
	document.cookie = key + "=" + value + ";path=/";
}

function cookie_parse(key) {
	cookieTab = document.cookie.split(";");
	for (var i = 0; i < cookieTab.length; i++) {
		cookieTab[i] = cookieTab[i].replace(" ", "");
		if (cookieTab[i].indexOf(key) == 0) {
			return cookieTab[i].substring(key.length + 1);
		}
	}
	return "no value";
}

// ############## REGISTER CLIENT ############## //

var url_api_register = "http://" + UI_IP + ":6060/register";

function register_client() {
	fetch(url_api_register)
		.then(res => {
			res.json().then(
				value => {
					cookie_add("uuid", value.uuid);
					window.location.href = "./search.html";
				}
			);
		})
		.catch(error => {
			console.log("Error fetch : " + error)
		});
}

// ############## ADD INPUTS FORM ############## //

document.addEventListener("DOMContentLoaded", function() {
    const addInputButton = document.getElementById("add-middlename");
    const inputContainer = document.getElementById("input-middlename");
    
    addInputButton.addEventListener("click", function() {
        const newInput = document.createElement("input");
        newInput.type = "text";
        newInput.name = "middlename";
        newInput.placeholder = "Middlename"
        inputContainer.appendChild(document.createElement("br")); // add a line break
        inputContainer.appendChild(newInput); // add the new input below the first input
    });
});

document.addEventListener("DOMContentLoaded", function() {
    const addInputButton = document.getElementById("add-username");
    const inputContainer = document.getElementById("input-username");
    
    addInputButton.addEventListener("click", function() {
        const newInput = document.createElement("input");
        newInput.type = "text";
        newInput.name = "username";
        newInput.placeholder = "Username"
        inputContainer.appendChild(document.createElement("br")); // add a line break
        inputContainer.appendChild(newInput); // add the new input below the first input
    });
});

document.addEventListener("DOMContentLoaded", function() {
    const addInputButton = document.getElementById("add-phone");
    const inputContainer = document.getElementById("input-phone");
    
    addInputButton.addEventListener("click", function() {
        const newInput = document.createElement("input");
        newInput.type = "tel";
        newInput.name = "phone";
        newInput.placeholder = "Phone number"
        newInput.pattern =  "^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$"
        inputContainer.appendChild(document.createElement("br")); // add a line break
        inputContainer.appendChild(newInput); // add the new input below the first input
    });
});

document.addEventListener("DOMContentLoaded", function() {
    const addInputButton = document.getElementById("add-email");
    const inputContainer = document.getElementById("input-email");
    
    addInputButton.addEventListener("click", function() {
        const newInput = document.createElement("input");
        newInput.type = "email";
        newInput.name = "email";
        newInput.placeholder = "Email"
        inputContainer.appendChild(document.createElement("br")); // add a line break
        inputContainer.appendChild(newInput); // add the new input below the first input
    });
});

// ############## STORE INPUT ############## //

/* Function use to group input that allow multiple entry */
function group_input(name) {
	var inputs = document.getElementsByName(name);
	var lst_inputs = new Array();
	for (var i = 0; i < inputs.length; i++) {
		lst_inputs.push(inputs[i].value);
	}
	return lst_inputs;
}

function get_address() {
	var addr = new Array();
	var dict_address = {
		country: document.getElementById("select_countries").value,
		state_code: document.getElementById("input_statecode").value,
		city: document.getElementById("input_city").value,
		street: document.getElementById("input_street").value,
		streetnumber: document.getElementById("input_streetnumber").value
	}

	if (!(dict_address.country == ""
		|| dict_address.state_code == ""
        || dict_address.city == ""
        || dict_address.street == ""
		|| dict_address.streetnumber == "" )) {
		addr.push(dict_address);
	}

	return addr;

}

function get_gender(gender) {
	if (document.getElementById(gender).value == "Male") {
		return "M";
	}
	else if (document.getElementById(gender).value == "Female") {
		return "F";
	}
	else {
		return "";
	}
}

function get_birthday(birthday) {
	var mydate = document.getElementById(birthday).value;

	if (mydate.length == 10) {
		var year = mydate.slice(0, 4);
		var month = mydate.slice(5, 7);
		var day = mydate.slice(8, 10);
		mydate = day + "/" + month + "/" + year;
	}
	else {
		mydate = "";
	}

	return mydate;
}

function load() {
	sessionStorage.setItem("firstname", document.getElementById("input_firstname").value);
	sessionStorage.setItem("lastname", document.getElementById("input_lastname").value);
	sessionStorage.setItem("middlename", group_input("middlename"));
	sessionStorage.setItem("gender", get_gender("select_gender"));
	sessionStorage.setItem("birthdate", get_birthday("input_birthdate"));
	sessionStorage.setItem("age", document.getElementById("input_age").value);
	sessionStorage.setItem("address", get_address());
	sessionStorage.setItem("phone", group_input("phone"));
	sessionStorage.setItem("email", group_input("email"));
	sessionStorage.setItem("username", group_input("username"));
	window.location.href = "./loading.html";
}

// ############## START RESEARCH ############## //

var url_api_research = "http://" + UI_IP + ":6060/make_research";
function make_research(data) {

	fetch(url_api_research, {
		method: "POST",

		headers: {
			'Accept': 'application/json',
			'Content-Type': 'application/json'
		},

		body: JSON.stringify({
			uuid: cookie_parse("uuid"),
			firstname: sessionStorage.getItem("firstname"),
			lastname: sessionStorage.getItem("lastname"),
			middlename: sessionStorage.getItem("middlename"),
			gender: sessionStorage.getItem("gender"),
			birthday: sessionStorage.getItem("birthday"),
			age: sessionStorage.getItem("age"),
			address: sessionStorage.getItem("address"),
			phone: sessionStorage.getItem("phone"),
			email: sessionStorage.getItem("email"),
			username: sessionStorage.getItem("username")
		})
	})
		.then(res => {
			res.json().then(
				value => {
					cookie_add("research_id", value.research_id);
					window.location.href = "./options.html";
				}
			);
		})
		.catch(error => {
			console.log("Error fetch : " + error);
		});
}

// ############## CHOOSE VISIBILITY ############## //

function get_checkbox() {
	dict_check = {
		firstname: document.getElementById("check_firstname").checked,
		lastname: document.getElementById("check_lastname").checked,
		lst_middlenames: document.getElementById("check_middlename").checked,
		lst_usernames: document.getElementById("check_username").checked,
		gender: document.getElementById("check_gender").checked,
		birth: document.getElementById("check_birthdate").checked,
		death: document.getElementById("check_deathdate").checked,
		age: document.getElementById("check_age").checked,
		lst_phone_numbers: document.getElementById("check_phone").checked,
		lst_accounts: document.getElementById("check_accounts").checked,
		lst_pictures: document.getElementById("check_pictures").checked,
		lst_ips: document.getElementById("check_ip").checked,
		lst_addresses: document.getElementById("check_address").checked,
		lst_locations: document.getElementById("check_location").checked,
		lst_organizations: document.getElementById("check_organization").checked,
		political_orientation: document.getElementById("check_political_orientations").checked
	}
	return dict_check;
}

var url_api_visibility = "http://127.0.0.1:6060/set_visibility";
function send_options() {
	fetch(url_api_visibility, {
		method: "PUT",

		headers: {
			'Accept': 'application/json',
			'Content-Type': 'application/json'
		},

		body: JSON.stringify({
			uuid: cookie_parse("uuid"),
			research_id: cookie_parse("research_id"),
			firstname: get_checkbox().firstname,
			lastname: get_checkbox().lastname,
			lst_middlenames: get_checkbox().lst_middlenames,
			lst_usernames: get_checkbox().lst_usernames,
			gender: get_checkbox().gender,
			birth: get_checkbox().birth,
			death: get_checkbox().death,
			age: get_checkbox().age,
			lst_phone_numbers: get_checkbox().lst_phone_numbers,
			lst_accounts: get_checkbox().lst_accounts,
			lst_pictures: get_checkbox().lst_pictures,
			lst_ips: get_checkbox().lst_ips,
			lst_addresses: get_checkbox().lst_addresses,
			lst_locations: get_checkbox().lst_locations,
			lst_organizations: get_checkbox().lst_organizations,
			political_orientation: get_checkbox().political_orientation
		})
	})
		.then(res => { res.json().then(value => { window.location.href = "./choice.html" }) })
		.catch(error => { console.log("Error fetch : " + error) });

}

// ############## CHOICE ############## //

var url_api_profiles = "http://127.0.0.1:6060/profiles";
function display_profiles(id_div) {
	fetch(url_api_profiles, {
		method: "POST",

		headers: {
			'Accept': 'application/json',
			'Content-Type': 'application/json'
		},

		body: JSON.stringify({
			uuid: cookie_parse("uuid"),
			research_id: cookie_parse("research_id")
		})
	})
		.then(res => {
			res.json().then(value => {
				for (var i = 0; i < value.lst_profile.length; i++) {
					add_profile_resume(id_div, i, value.lst_profile[i].profile_id, value.lst_profile[i].picture, value.lst_profile[i].summary);
				}
			});
		})
		.catch(error => { console.log("Error fetch : " + error) });
}

function add_profile_resume(id_div, index, profile_id, picture, sumary) {
	var data = '<div class="result">';
	data += '<button class="div-bt-profile" type="button" onclick="show_results(\'' + profile_id + '\')">';
	data += '<p class="profile-title">Profile ' + index + '</p>';
	data += '<center><img src="' + picture + '"width="200em" height="auto"></center>';
	data += '<p>' + sumary + '</p>';
	data += '</button><br>';
	data += '<button class="bt-delete" onclick="delete_profile(\'' + profile_id + '\')">DELETE</button><br>';
	data += '</div>'

	document.getElementById(id_div).innerHTML += data;
}

// Function use to delete unwanted profiles
var url_api_delete = "http://127.0.0.1:6060/remove_profile";
function delete_profile(pid) {
	fetch(url_api_delete, {
		method: "DELETE",

		headers: {
			'Accept': 'application/json',
			'Content-Type': 'application/json'
		},

		body: JSON.stringify({
			uuid: cookie_parse("uuid"),
			research_id: cookie_parse("research_id"),
			profile_id: pid
		})
	})
		.then(res => {
			res.json().then(value => {
				window.location.href = "./choice.html";
			});
		})
		.catch(error => { console.log("Error fetch : " + error) });
}