/**
 * Sagittarius - JavaScript Starter Kit
 * Copyright WillyG Productions
 * @Authors: William Gaul
 */
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

module.exports = encryption;
