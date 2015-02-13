/**
 * Sagittarius - JavaScript Starter Kit
 * Copyright WillyG Productions
 * @Authors: William Gaul
 */
var SagRequest = require('./sag-request');

var actions = {};

actions.Action = function(handler, password) {
	return {
		DBTYPE: 'object_type',
		DBNAME: 'object_name',
		request: SagRequest(password).setDestination(handler)
	};
};

actions.GetAction = function(password) {
	var that = this.Action('/dbget', password);
	that.request.addURLPair('rlim', 20);
	that.request.addURLPair('roff', 0);

	that.AddFilter = function(field, value, encrypt) {
		that.request.addURLPair('f', field + '::' + value, encrypt);
		return that;
	};

	that.AddProjection = function(field, encrypt) {
		that.request.addURLPair('p', field + (encrypt !== undefined ? '~' : ''));
		return that;
	};

	that.SetLimit = function(rl) {
		that.request.setURLPair('rlim', rl);
		return that;
	};

	that.SetOffset = function(ro) {
		that.request.setURLPair('roff', ro);
		return that;
	};

	that.Unique = function() {
		that.request.setURLPair('rlim', 1);
		return that;
	};

	return that;
};

actions.AddAction = function(password) {
	var that = this.Action('/dbadd', password);

	that.AddAttribute = function(field, value, encrypt) {
		that.request.addURLPair('a', field + '::' + value, encrypt);
		return that;
	};

	return that;
};

actions.DelAction = function(password) {
	var that = this.GetAction(password);
	that.request.setDestination('/dbdel');
	that.request.addURLPair('rres', false);

	that.SetReturnsResults = function() {
		that.request.setURLPair('rres', true);
		return that;
	};

	return that;
};

actions.ModAction = function(password) {
	var that = this.DelAction(password);
	that.request.setDestination('/dbmod');

	that.AddModification = function(field, value, encrypt) {
		that.request.addURLPair('m', field + '::' + value, encrypt);
		return that;
	};

	return that;
};

modules.exports = actions;
