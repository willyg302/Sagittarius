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

	that.addFilter = function(field, value, encrypt) {
		that.request.addURLPair('f', field + '::' + value, encrypt);
		return that;
	};

	that.addProjection = function(field, encrypt) {
		that.request.addURLPair('p', field + (encrypt !== undefined ? '~' : ''));
		return that;
	};

	that.setLimit = function(rl) {
		that.request.setURLPair('rlim', rl);
		return that;
	};

	that.setOffset = function(ro) {
		that.request.setURLPair('roff', ro);
		return that;
	};

	that.unique = function() {
		that.request.setURLPair('rlim', 1);
		return that;
	};

	return that;
};

actions.AddAction = function(password) {
	var that = this.Action('/dbadd', password);

	that.addAttribute = function(field, value, encrypt) {
		that.request.addURLPair('a', field + '::' + value, encrypt);
		return that;
	};

	return that;
};

actions.DelAction = function(password) {
	var that = this.GetAction(password);
	that.request.setDestination('/dbdel');
	that.request.addURLPair('rres', false);

	that.setReturnsResults = function() {
		that.request.setURLPair('rres', true);
		return that;
	};

	return that;
};

actions.ModAction = function(password) {
	var that = this.DelAction(password);
	that.request.setDestination('/dbmod');

	that.addModification = function(field, value, encrypt) {
		that.request.addURLPair('m', field + '::' + value, encrypt);
		return that;
	};

	return that;
};

modules.exports = actions;
