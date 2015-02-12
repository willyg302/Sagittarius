var http = require('http');
var express = require('express');
var sock = require('sockjs').createServer();

var app = express();

sock.on('connection', function(conn) {
	conn.on('data', function(message) {
		console.log(JSON.parse(message).endpoint);
	});
});

app.set('port', 8080);
app.use(express.static(__dirname));

var server = http.createServer(app).listen(app.get('port'), function() {
	console.log("Server listening on port " + app.get('port'));
});
sock.installHandlers(server, {prefix: '/sock'});
