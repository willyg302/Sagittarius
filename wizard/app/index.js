var http = require('http');
var express = require('express');
var jf = require('jsonfile');
var request = require('request');
var sock = require('sockjs').createServer();


var encryption = {};

encryption.padString = function(text, key, pad) {
	var ret = '', seed = 0, i;
	for (i = 0; i < key.length; i++) {
		seed += ((key.charCodeAt(i) & 0xff) * (1 << i));
	}
	seed *= pad;
	for (i = 0; i < text.length; i++) {
		seed = ((seed * 214013 + 2531011) >>> 16) & 0x7fff;
		ret += String.fromCharCode((text.charCodeAt(i) & 0xff) ^ (seed & 0xff));
	}
	return ret;
};

encryption.byteToHex = function(b) {
	var hex = '0123456789ABCDEF', hi = (b >>> 4) & 0x0f, lo = b & 0x0f;
	return hex.charAt(hi) + hex.charAt(lo);
};

encryption.hexToByte = function(s) {
	var hex = '0123456789ABCDEF', hi = hex.indexOf(s.charAt(0)), lo = hex.indexOf(s.charAt(1));
	return ((hi << 4) + lo) & 0xff;
};

encryption.encrypt = function(pt, key) {
	var ct = '', pad = Math.floor(Math.random() * 256), temp = this.padString(pt, key, pad), i;
	for (i = 0; i < temp.length; i++) {
		ct += this.byteToHex(temp.charCodeAt(i) & 0xff);
	}
	return "~" + this.byteToHex(pad & 0xff) + ct;
};

encryption.decrypt = function(ct, key) {
	var temp = '', i;
	for (i = 3; i < ct.length; i += 2) {
		temp += String.fromCharCode(this.hexToByte(ct.substring(i, i + 2)));
	}
	return this.padString(temp, key, this.hexToByte(ct.substring(1, 3)));
};


var DATA_FILE = 'recipes.dat';

var runRecipe = function(conn, recipe, id, password) {
	var handle = "/" + recipe.action;
	var params = {};
	recipe.buttons.forEach(function(button) {
		if (button.type === 'returns') {
			params.rres = true;
		} else {
			var val = button.val;
			if (button.enc) {
				val = encryption.encrypt(val, password);
			}
			params[button.key] = val;
		}
	});

	conn.out("Submitting to " + id + handle + " with params " + JSON.stringify(params));

	// Initialize connection!
	request.post({
		url: "http://" + id + ".appspot.com" + handle,
		form: params
	}, function(err, resp, body) {
		if (err) {
			conn.err("Error running recipe:\n" + err);
			return;
		}
		// @TODO: Decryption
		conn.out("Received data:\n" + body);
	});
};

var saveRecipe = function(conn, recipe) {
	recipes = jf.readFileSync(DATA_FILE);
	recipes[recipe.name] = recipe
	jf.writeFileSync(DATA_FILE, recipes);
	conn.out("Successfully saved recipe \"" + recipe.name + "\"");
};

var deleteRecipe = function(conn, recipe) {
	recipes = jf.readFileSync(DATA_FILE);
	if (recipes.hasOwnProperty(recipe.name)) {
		delete recipes[recipe.name];
		jf.writeFileSync(DATA_FILE, recipes);
		conn.out("Successfully deleted recipe \"" + recipe.name + "\"");
	} else {
		conn.err("No recipe named \"" + recipe.name + "\" has been saved");
	}
};


var app = express();

sock.on('connection', function(conn) {
	conn.on('data', function(message) {
		payload = JSON.parse(message);

		conn.out = function(message) {
			this.write(JSON.stringify({
				message: message,
				error: false
			}));
		};

		conn.err = function(message) {
			this.write(JSON.stringify({
				message: message,
				error: true
			}));
		};

		switch (payload.endpoint) {
			case 'run':
				runRecipe(conn, payload.recipe, payload.id, payload.password);
				break;
			case 'save':
				saveRecipe(conn, payload.recipe);
				break;
			case 'delete':
				deleteRecipe(conn, payload.recipe);
				break;
			default: break;
		}
	});
});

app.set('port', 8080);
app.use(express.static(__dirname));

var server = http.createServer(app).listen(app.get('port'), function() {
	console.log("Server listening on port " + app.get('port'));
});
sock.installHandlers(server, {prefix: '/sock'});
