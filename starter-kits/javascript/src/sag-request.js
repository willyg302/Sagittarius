/**
 * Sagittarius - JavaScript Starter Kit
 * Copyright WillyG Productions
 * @Authors: William Gaul
 */
var encryption = require('./encryption');

module.exports = function(password) {
	var that = {}, data = [];
	that.password = password;

	that.setDestination = function(dest) {
		that.dest = dest;
		return that;
	}

	that.addURLPair = function(key, value, encrypt) {
		if (encrypt !== undefined) {
			value = encryption.encrypt(value, that.password);
		}
		data.push({key: key, value: value});
	};
	
	that.setURLPair = function(key, value, encrypt) {
		for (var i = 0; i < data.length; i++) {
			if (data[i].key === key) {
				if (encrypt !== undefined) {
					value = encryption.encrypt(value, that.password);
				}
				data[i].value = value;
				return;
			}
		}
	};

	that.getData = function() {
		var params = {};
		data.forEach(function(param) {
			params[param.key] = param.value;
		});
		return params;
	};

	return that;
};
