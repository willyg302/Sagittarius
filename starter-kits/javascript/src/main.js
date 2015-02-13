/**
 * Sagittarius - JavaScript Starter Kit
 * Copyright WillyG Productions
 * @Authors: William Gaul
 */
var actions = require('./actions');
var encryption = require('./encryption');
var request = require('superagent');
var SagRequest = require('./sag-request');

function Sagittarius(appid, pass) {
	this.appid = appid;
	this.pass = pass;
	this.encryption = encryption;
}

Sagittarius.prototype.createAction = function(type) {
	return {
		get: actions.GetAction,
		add: actions.AddAction,
		mod: actions.ModAction,
		del: actions.DelAction
	}[type](this.pass);
};

Sagittarius.prototype.sendMail = function(mail) {
	var req = SagRequest(this.pass);
	req.setDestination('/mail');
	req.addURLPair('recv', mail.receiver);
	req.addURLPair('subj', mail.subject);
	req.addURLPair('mesg', mail.message);
	if (mail.hasOwnProperty('sender')) {
		req.addURLPair('send', mail.sender);
	}
	this.transmit(req, mail.callback);
};

Sagittarius.prototype.transmit = function(req, callback) {
	request.post("http://" + this.appid + ".appspot.com" + req.dest)
		.type('form')
		.send(req.getData())
		.end(function(res) {
			if (!res.ok) {
				callback(res.error.message, true);
			}
			// @TODO: Decryption
			callback(res.body, false);
		});
};

Sagittarius.prototype.submit = function(action, callback) {
	this.transmit(action.request, callback);
};

module.exports = Sagittarius;
