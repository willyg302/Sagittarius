/**
 * Sagittarius - JavaScript Starter Kit
 * Copyright 2013 WillyG Productions
 * @Authors: William Gaul
 */
function Encryption() {
	// Just to declare the Encrypt namespace
}

Encryption.PadString = function (text, key, pad) {
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

Encryption.GetHexForByte = function (b) {
	var hex = '0123456789ABCDEF', hi = (b >>> 4) & 0x0f, lo = b & 0x0f;
	return hex.charAt(hi) + hex.charAt(lo);
};

Encryption.GetByteForHex = function (s) {
	var hex = '0123456789ABCDEF', hi = hex.indexOf(s.charAt(0)), lo = hex.indexOf(s.charAt(1));
	return ((hi << 4) + lo) & 0xff;
};

Encryption.Encrypt = function (pt, key) {
	var ct = '', pad = Math.floor(Math.random() * 256), temp = Encryption.PadString(pt, key, pad), i;
	for (i = 0; i < temp.length; i++) {
		ct += Encryption.GetHexForByte(temp.charCodeAt(i) & 0xff);
	}
	return "~" + Encryption.GetHexForByte(pad & 0xff) + ct;
};

Encryption.Decrypt = function (ct, key) {
	var temp = '', i;
	for (i = 3; i < ct.length; i += 2) {
		temp += String.fromCharCode(Encryption.GetByteForHex(ct.substring(i, i + 2)));
	}
	return Encryption.PadString(temp, key, Encryption.GetByteForHex(ct.substring(1, 3)));
};

var SagRequest = function (password) {
	var that = {}, data = [];
	that.password = password;

	that.setDestination = function (dest) {
		that.dest = dest;
		return that;
	}

	that.addURLPair = function (key, value, encrypt) {
		if (encrypt !== undefined) {
			value = Encryption.Encrypt(value, that.password);
		}
		data.push({key: key, value: value});
	};
	
	that.setURLPair = function (key, value, encrypt) {
		for (var i = 0; i < urlstring.length; i++) {
			if (urlstring[i].key === key) {
				if (encrypt !== undefined) {
					value = Encryption.Encrypt(value, that.password);
				}
				urlstring[i].value = value;
				return;
			}
		}
	};

	that.GetData = function () {
		var segments = [];
		for (var i = 0; i < urlstring.length; i++) {
			segments[i] = urlstring[i].key + "=" + urlstring[i].value;
		}
		return segments.join('&');
	};

	return that;
}

var Action = function (handler, password) {
	var that = {};
	that.DBTYPE = 'object_type';
	that.DBNAME = 'object_name';
	that.request = SagRequest(password);
	that.request.setDestination(handler);
	return that;
};

var GetAction = function (password) {
	var that = Action('/dbget', password);
	that.request.addURLPair('rlim', 20);
	that.request.addURLPair('roff', 0);
	
	that.AddFilter = function (field, value, encrypt) {
		that.request.addURLPair('f', field + '::' + value, encrypt);
		return that;
	};
	
	that.AddProjection = function (field, encrypt) {
		that.request.addURLPair('p', field + (encrypt !== undefined ? '~' : ''));
		return that;
	};
	
	that.SetLimit = function (rl) {
		that.request.setURLPair('rlim', rl);
		return that;
	};
	
	that.SetOffset = function (ro) {
		that.request.setURLPair('roff', ro);
		return that;
	};
	
	that.Unique = function () {
		that.request.setURLPair('rlim', 1);
		return that;
	};
	
	return that;
};

var AddAction = function (password) {
	var that = Action('/dbadd', password);
	
	that.AddAttribute = function (field, value, encrypt) {
		that.request.addURLPair('a', field + '::' + value, encrypt);
		return that;
	};
	
	return that;
};

var DelAction = function (password) {
	var that = GetAction(password);
	that.handler = '/dbdel';
	that.request.addURLPair('rres', 'false');
	
	that.SetReturnsResults = function () {
		that.request.setURLPair('rres', 'true');
		return that;
	};
	
	return that;
};

var ModAction = function (password) {
	var that = DelAction(password);
	that.handler = '/dbmod';
	
	that.AddModification = function (field, value, encrypt) {
		that.request.addURLPair('m', field + '::' + value, encrypt);
		return that;
	};
	
	return that;
};

function createCORSRequest() {
	var xhr = new XMLHttpRequest();
	if (xhr.hasOwnProperty('withCredentials')) {
		// We're good!
	} else if (typeof XDomainRequest !== 'undefined') {
		xhr = new XDomainRequest();
	} else {
		xhr = null;
	}
	return xhr;
}

function Sagittarius(appid, pass) {
	this.appid = appid;
	this.pass = pass;
}

Sagittarius.prototype.CreateAction = function (type) {
	switch (type) {
		case 'get': return GetAction(this.pass);
		case 'add': return AddAction(this.pass);
		case 'mod': return ModAction(this.pass);
		case 'del': return DelAction(this.pass);
		default: break;
	}
};

Sagittarius.prototype.SubmitAction = function (action, callback) {
	this.TransmitRequest(action.request, callback);
};

Sagittarius.prototype.TransmitRequest = function (sagRequest, callback) {
	var request = createCORSRequest();
	if (!request) {
		return;
	}
	request.open('POST', "http://" + this.appid + ".appspot.com" + sagRequest.dest, true);
	if (window.XDomainRequest) {
		request.onload = function () {
			callback(JSON.parse(request.responseText.replace("<resp>", "").replace("</resp>", "")));
		};
	} else {
		request.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
		request.onreadystatechange = function (response) {
			if (request.readyState === 4) {
				callback(JSON.parse(request.responseText.replace("<resp>", "").replace("</resp>", "")));
			}
		};
	}
	// Use encodeURI() to encode entire data!!!
	request.send(encodeURI(sagRequest.GetData()));
};

Sagittarius.prototype.SendMail = function (sendObj) {
	var mail = SagRequest(this.pass);
	mail.setDestination('/mail');
	mail.addURLPair('recv', sendObj.receiver);
	mail.addURLPair('subj', sendObj.subject);
	mail.addURLPair('mesg', sendObj.message);
	if (sendObj.hasOwnProperty('sender')) {
		mail.addURLPair('send', sendObj.sender);
	}
	this.TransmitRequest(mail, sendObj.callback);
};