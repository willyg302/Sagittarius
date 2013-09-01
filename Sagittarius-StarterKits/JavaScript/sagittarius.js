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

var Action = function (type, password) {
    var that = {}, urlstring = [];
    that.DBTYPE = 'object_type';
    that.DBNAME = 'object_name';
    that.handler = type;
    that.password = password;
    
    that.add = function (key, value) {
        urlstring.push({key: key, value: value});
    };
    
    that.set = function (key, value) {
        for (var i = 0; i < urlstring.length; i++) {
            if (urlstring[i].key === key) {
                urlstring[i].value = value;
                return;
            }
        }
    };
    
    that.Encrypt = function (text, encrypt) {
        if (encrypt !== undefined) {
            text = Encryption.Encrypt(text, that.password);
        }
        return text;
    };
    
    that.GetURLString = function () {
        var segments = [], pair;
        for (var i = 0; i < urlstring.length; i++) {
            pair = urlstring[i];
            segments[i] = pair.key + "=" + pair.value;
        }
        return segments.join('&');
    };
    
    return that;
};

var GetAction = function (password) {
    var that = Action('/dbget', password);
    that.add('rlim', 20);
    that.add('roff', 0);
    
    that.AddFilter = function (field, value, encrypt) {
        that.add('f', that.Encrypt(field + '::' + value, encrypt));
        return that;
    };
    
    that.AddProjection = function (field, encrypt) {
        that.add('p', (encrypt !== undefined ? '~' : '') + field);
        return that;
    };
    
    that.SetLimit = function (rl) {
        that.set('rlim', rl);
        return that;
    };
    
    that.SetOffset = function (ro) {
        that.set('roff', ro);
        return that;
    };
    
    that.Unique = function () {
        that.set('rlim', 1);
        return that;
    };
    
    return that;
};

var AddAction = function (password) {
    var that = Action('/dbadd', password);
    
    that.AddAttribute = function (field, value, encrypt) {
        that.add('a', that.Encrypt(field + '::' + value, encrypt));
        return that;
    };
    
    return that;
};

var ModAction = function (password) {
    var that = GetAction(password);
    that.handler = '/dbmod';
    
    that.AddModification = function (field, value, encrypt) {
        that.add('m', that.Encrypt(field + '::' + value, encrypt));
        return that;
    };
    
    that.SetReturnsResults = function () {
        that.add('rres', 'true');
        return that;
    };
    
    return that;
};

var DelAction = function (password) {
    var that = GetAction(password);
    that.handler = '/dbdel';
    
    that.SetReturnsResults = function () {
        that.add('rres', 'true');
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
    this.post(action.handler, action.GetURLString(), callback);
};

Sagittarius.prototype.post = function (dest, data, callback) {
    var request = createCORSRequest();
	if (!request) {
		return;
	}
    request.open('POST', "http://" + this.appid + ".appspot.com" + dest, true);
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
	request.send(encodeURI(data));
};

Sagittarius.prototype.SendMail = function (sendObj) {
    var data = "recv=" + sendObj.receiver + "&subj=" + sendObj.subject + "&mesg=" + sendObj.message;
    if (sendObj.hasOwnProperty('sender')) {
        data += ('&send=' + sendObj.sender);
    }
    this.post('/mail', data, sendObj.callback);
};