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

var url_api_register = "http://127.0.0.1:6060/register";

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

if (window.location.pathname.split("/").pop() === "search.html") {

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
}

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

var url_api_research = "http://127.0.0.1:6060/make_research";

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

function add_profile_resume(id_div, index, profile_id, picture, summary) {
	var data = '<div class="result">';
	data += '<button class="div-bt-profile" type="button" onclick="show_results(\'' + profile_id + '\')">';
	data += '<p class="profile-title">Profile ' + index + '</p>';
	data += '<center><img src="' + picture + '"width="200em" height="auto"></center>';
	data += '<p>' + summary + '</p>';
	data += '</button><br>';
	data += '<label class="bt-select">';
	data += '<input type="checkbox" name="checkbox" id="' + profile_id + '"/>SELECT'
	data += '</label></div>'

	document.getElementById(id_div).innerHTML += data;
}

//------------------------------------------------------------

function get_checked() {
	const checkboxIds = Array.from(document.querySelectorAll('input[type="checkbox"]:checked')).map(checkbox => checkbox.id);
	return checkboxIds;
}

var url_api_merge = "http://127.0.0.1:6060/merge";

function mergeSelection() {
	fetch(url_api_merge, {
		method: "POST",

		headers: {
			'Accept': 'application/json',
			'Content-Type': 'application/json'
		},

		body: JSON.stringify({
			uuid: cookie_parse("uuid"),
			research_id: cookie_parse("research_id"),
			profile_id: get_checked()
		})
	})
		.then(res => {
			res.json().then(value => {
				window.location.href = "./choice.html";
			});
		})
		.catch(error => { console.log("Error fetch : " + error) });
}


var url_api_delete = "http://127.0.0.1:6060/remove_profile";

function deleteSelection() {
	fetch(url_api_delete, {
		method: "DELETE",

		headers: {
			'Accept': 'application/json',
			'Content-Type': 'application/json'
		},

		body: JSON.stringify({
			uuid: cookie_parse("uuid"),
			research_id: cookie_parse("research_id"),
			lst_profile: get_checked()
		})
	})
		.then(res => {
			res.json().then(value => {
				window.location.href = "./choice.html";
			});
		})
		.catch(error => { console.log("Error fetch : " + error) });
}

// ############## RESULT ############## //

function show_results(profile_id) {
    cookie_add("profile_id", profile_id);
    window.location.href = "./results.html";
}

var url_api_profile = "http://127.0.0.1:6060/profile";
const NO = [undefined, null, ""]

function getUsertitle(id_div) {
	fetch(url_api_profile, {
		method: "POST",

		headers: {
			'Accept': 'application/json',
			'Content-Type': 'application/json'
		},

		body: JSON.stringify({
			uuid: cookie_parse("uuid"),
			research_id: cookie_parse("research_id"),
			profile_id: cookie_parse("profile_id")
		})
	})
		.then(res => {
			res.json().then(value => {
				
				//firstname
				if (!(value.firstname.str_value.includes(NO))) {
					firstname = value.firstname.str_value;
				}
				//lastname
				if (!(value.lastname.str_value.includes(NO))) {
					lastname = value.lastname.str_value;
				}
				//username
				if (value.lst_usernames.length > 0) {
					username = value.lst_usernames[0];
				}

				// set user title
				if (!(firstname.includes(NO))) {
					userTitle = firstname;
					if (!(lastname.includes(NO))) {
						userTitle += " " + lastname;
					}
				} else if (!(username.includes(NO))) {
					userTitle = username
				} else {
					userTitle = "Unknown"
				}

				var element = document.getElementById(id_div);
				element.innerHTML = userTitle;
			});
		})
		.catch(error => { console.log("Error fetch : " + error) });
}

function activateMenuItem(menuItemId) {
  // Get all menu items
  const menuItems = document.querySelectorAll('.nav li');

  // Remove the active class from all menu items
  menuItems.forEach(menuItem => menuItem.classList.remove('active'));

  // Add the active class to the menu item with the specified ID
  document.getElementById(menuItemId).classList.add('active');
}

// delete profile
var url_api_delete = "http://127.0.0.1:6060/remove_profile";

function deleteProfile() {
	fetch(url_api_delete, {
		method: "DELETE",

		headers: {
			'Accept': 'application/json',
			'Content-Type': 'application/json'
		},

		body: JSON.stringify({
			uuid: cookie_parse("uuid"),
			research_id: cookie_parse("research_id"),
			lst_profile: [cookie_parse("profile_id")]
		})
	})
		.then(res => {
			res.json().then(value => {
				window.location.href = "./choice.html";
			});
		})
		.catch(error => { console.log("Error fetch : " + error) });
}

function clearProfileContent() {
	// CLEAR HTML
	const div = document.getElementById("profile-content");
	div.innerHTML = '';
}

// function generateOverviewHTML() {}

function generateProfileInformationHTML(id_profile_content) {
	fetch(url_api_profile, {
		method: "POST",

		headers: {
			'Accept': 'application/json',
			'Content-Type': 'application/json'
		},

		body: JSON.stringify({
			uuid: cookie_parse("uuid"),
			research_id: cookie_parse("research_id"),
			profile_id: cookie_parse("profile_id")
		})
	})
		.then(res => {
			res.json().then(value => {
				
				var data = "";

				//firstname
				if (!(value.firstname.str_value == undefined || value.firstname.str_value == null || value.firstname.str_value == "")) {
					data += '<p style="margin-top: 30px;">Firstname : ' + value.firstname.str_value + '</p>';
				}

				//lastname
				if (!(value.lastname.str_value == undefined || value.lastname.str_value == null || value.lastname.str_value == "")) {
					data += '<p>Lastname : ' + value.lastname.str_value + '</p>';
				}

				//middlename
				if (value.lst_middlenames.length > 0) {
					data += '<p>Middle name(s):';
					for (var i = 0; i < value.lst_middlenames.length; i++) {
						if (!(value.lst_middlenames[i] == undefined || value.lst_middlenames[i] == null || value.lst_middlenames[i] == "")) {
							data += ' ' + value.lst_middlenames[i];
						}
					}
					data += '</p>';
				}

				//age
				if (!(value.age == undefined || value.age == null || value.age == "")) {
					data += '<p>Age : ' + value.age + '</p>'
				}

				//birthdate
				if (!(value.birth == undefined || value.birth == null || value.birth == "")) {
					if (!(value.birth.date == undefined || value.birth.date == null || value.birth.date == "")) {
						data += '<p>Birthdate : ' + value.birth.date + '</p>'
					}
				}

				//birth address
				if (!(value.birth == undefined || value.birth == null || value.birth == "")) {
					if (!(value.birth.address == undefined || value.birth.address == null || value.birth.address == "")) {
						if (value.birth.address.state_code.length >= 0) {
							data += '<p>Address birth : ' + value.birth.address.city + ', ' + value.birth.address.state_code + ', ' + value.birth.address.country + '</p>';
						}
					}
				}

				//deathdate
				if (!(value.death == undefined || value.death == null || value.death == "")) {
					if (!(value.death.date == undefined || value.death.date == null || value.death.date == "")) {
						data += '<p>Deathdate : ' + value.death.date + '</p>'
					}
				}

				//death address
				if (!(value.death == undefined || value.death == null || value.death == "")) {
					if (!(value.death.address == undefined || value.death.address == null || value.death.address == "")) {
						if (value.death.address.state_code.length >= 0) {
							data += '<p>Address death : ' + value.death.address.city + ', ' + value.death.address.state_code + ', ' + value.death.address.country + '</p>';
						}
					}
				}

				//username
				if (value.lst_usernames.length > 0) {
					data += '<p>Username(s) :';
					for (var i = 0; i < value.lst_usernames.length; i++) {
						if (!(value.lst_usernames[i] == undefined || value.lst_usernames[i] == null || value.lst_usernames[i] == "")) {
							data += ' ' + value.lst_usernames[i];
						}
					}
					data += '</p>';
				}

				//accounts
				if (value.lst_accounts.length > 0) {
					for (var i = 0; i < value.lst_accounts.length; i++) {
						data += '<a href="' + value.lst_accounts[i]['url'] +'">' + value.lst_accounts[i]['type'] + '</a> '
					}
				}

				//emails
				if (value.lst_emails.length > 0) {
					for (var i = 0; i < value.lst_emails.length; i++) {
						if (!(value.lst_emails[i].str_value == undefined || value.lst_emails[i].str_value == null || value.lst_emails[i].str_value == "")) {
							data += '<p>Email ' + i + ' : ' + value.lst_emails[i].str_value + '</p>'
						}
					}
				}

				//--------------------------------------
				//DISPLAY
				document.getElementById("profile-content").innerHTML = data;
			});
		})
		.catch(error => { console.log("Error fetch : " + error) });
}

function generateMarker(map, address) {
	// Geocode the address using Nominatim
	var xhr = new XMLHttpRequest();
	xhr.open('GET', 'https://nominatim.openstreetmap.org/search?q=' + encodeURIComponent(address) + '&format=json');
	xhr.onload = function() {
	if (xhr.status === 200) {
		// Parse the response
		var response = JSON.parse(xhr.responseText);
		if (response.length > 0) {
		// Use the first result
		var lon = response[0].lon;
		var lat = response[0].lat;

		// Create a marker at the geocoded location
		var marker = new ol.Feature({
			geometry: new ol.geom.Point(ol.proj.fromLonLat([lon, lat]))
		});

		// Create a text style
		var textStyle = new ol.style.Text({
			text: address.split(",")[0],
			font: '12px Arial',
			offsetY: -20, // Offset the label from the marker
			fill: new ol.style.Fill({color: 'black'})
		});

		// Create a red marker style
		var markerStyle = new ol.style.Style({
			image: new ol.style.RegularShape({
			  points: 3,
			  radius: 10,
			  angle: Math.PI,
			  fill: new ol.style.Fill({color: 'red'})
			}),
			text: textStyle // Add the text style to the marker style
		});
		
		// Create a layer for the marker
		var vectorSource = new ol.source.Vector({
			features: [marker]
		});

		// Add the marker layer to the map
		var markerLayer = new ol.layer.Vector({
			source: vectorSource,
			style: markerStyle
		});
		map.addLayer(markerLayer);

		// Center the map on the marker
		// map.getView().setCenter(ol.proj.fromLonLat([lon, lat]));
		// map.getView().setZoom(12);
		}
	}
	};
	xhr.send();
}


function generateProfileAddressesMarker(map) {
	fetch(url_api_profile, {
		method: "POST",

		headers: {
			'Accept': 'application/json',
			'Content-Type': 'application/json'
		},

		body: JSON.stringify({
			uuid: cookie_parse("uuid"),
			research_id: cookie_parse("research_id"),
			profile_id: cookie_parse("profile_id")
		})
	})
		.then(res => {
			res.json().then(value => {

				// birth address
				if (!(value.birth == undefined || value.birth == null || value.birth == "")) {
					if (!(value.birth.address == undefined || value.birth.address == null || value.birth.address == "")) {
						if (value.birth.address.state_code.length >= 0) {
							var birth_address = value.birth.address.city + ', ' + value.birth.address.state_code + ', ' + value.birth.address.country;
							generateMarker(map, birth_address)
						}
					}
				}
				// death address
				if (!(value.death == undefined || value.death == null || value.death == "")) {
					if (!(value.death.date == undefined || value.death.date == null || value.death.date == "")) {
						if (value.death.address.state_code.length >= 0) {
							var death_address = value.death.address.city + ', ' + value.death.address.state_code + ', ' + value.death.address.country;
							generateMarker(map, death_address)
						}
					}
				}

				
			});
		})
		.catch(error => { console.log("Error fetch : " + error) });
}

function generateMapsHTML() {

	var data = '<div id="map" style="width: 100%;height: 400px;border: 1px solid white;"></div>';
	document.getElementById("profile-content").innerHTML = data;
	// Create the map object
	var map = new ol.Map({
	target: 'map', // The ID of the map div element
	layers: [
		new ol.layer.Tile({
		source: new ol.source.OSM()
		})
	],
	view: new ol.View({
		center: ol.proj.fromLonLat([1.8, 46]), // Set the center of the map
		zoom: 5 // Set the initial zoom level
	})
	});
	generateProfileAddressesMarker(map)
}

function generateOthersHTML() {
	
}