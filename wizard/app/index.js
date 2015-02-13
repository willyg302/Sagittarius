var http = require('http');
var express = require('express');
var jf = require('jsonfile');
var sock = require('sockjs').createServer();


var DATA_FILE = 'recipes.dat';

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
