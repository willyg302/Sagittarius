var EventEmitter = require('events').EventEmitter;
var SockJS = require('sockjs-client');
var merge = require('react/lib/merge');

var AppDispatcher = require('./app-dispatcher');
var Constants = require('./constants');

// This is horrible, but avoids having duplicate code or symlinks
var Sagittarius = require('../../../starter-kits/javascript/src/main');


var CHANGE_EVENT = 'change';

var sock = new SockJS('http://localhost:8080/sock');

sock.onmessage = function(e) {
	var payload = JSON.parse(e.data);
	var message = payload.message.replace(new RegExp('\n', 'g'), '<br>');
	var output = document.getElementById('output');
	output.innerHTML = "<p" + (payload.error ? ' class="error"' : '') + ">" + message + "</p>" + output.innerHTML;
};

var send = function(message) {
	sock.send(JSON.stringify(message));
};


var buttons = {
	'filter': 'Add Filter',
	'project': 'Add Projection',
	'attribute': 'Add Attribute',
	'modification': 'Modify Attribute',
	'limit': 'Set Limit',
	'offset': 'Set Offset',
	'returns': 'Returns Results',
	'generic': 'Generic Parameter'
};

var actions =  {
	'dbget': 'Get',
	'dbadd': 'Add',
	'dbmod': 'Modify',
	'dbdel': 'Delete',
	'mail': 'Send Mail',
	'ldbds': 'Leaderboards'
};


var _state = {
	id: '',
	pass: '',
	recipe: {
		name: 'Untitled',
		action: 'dbget',
		buttons: []
	}
};


function changeId(id) {
	_state.id = id;
}

function changePass(pass) {
	_state.pass = pass;
}

function changeRecipeName(name) {
	_state.recipe.name = name;
}

function setAction(action) {
	_state.recipe.action = action;
}

function addButton(type) {
	_state.recipe.buttons.push({
		type: type,
		enc: false,
		key: '',
		val: ''
	});
}

function removeButton(index) {
	_state.recipe.buttons.splice(index, 1);
}

function updateButton(index, data) {
	//
}

function runRecipe() {
	if (!_state.id || !_state.pass || _state.recipe.buttons.length === 0) {
		return;
	}
	send({
		endpoint: 'run',
		recipe: _state.recipe,
		id: _state.id,
		password: _state.pass
	});
}

function saveRecipe() {
	send({
		endpoint: 'save',
		recipe: _state.recipe
	});
}

function clearRecipe() {
	_state.recipe.buttons = [];
}

function deleteRecipe() {
	send({
		endpoint: 'delete',
		recipe: _state.recipe
	});
}


var AppStore = merge(EventEmitter.prototype, {
	getState: function() {
		return _state;
	},
	getActions: function() {
		return actions;
	},
	getAvailableButtons: function() {
		var l, o, r;
		for (var i = 0; i < _state.recipe.buttons.length; i++) {
			var e = _state.recipe.buttons[i].type;
			l = l || (e === 'limit');
			o = o || (e === 'offset');
			r = r || (e === 'returns');
		}
		return Object.keys(buttons).filter(function(button) {
			switch(button) {
				case 'filter':
				case 'project':
					return ['dbget', 'dbmod', 'dbdel'].indexOf(_state.recipe.action) !== -1;
				case 'attribute':
					return _state.recipe.action === 'dbadd';
				case 'modification':
					return _state.recipe.action === 'dbmod';
				case 'limit':
					return !l && ['dbget', 'dbmod', 'dbdel'].indexOf(_state.recipe.action) !== -1;
				case 'offset':
					return !o && ['dbget', 'dbmod', 'dbdel'].indexOf(_state.recipe.action) !== -1;
				case 'returns':
					return !r && ['dbmod', 'dbdel'].indexOf(_state.recipe.action) !== -1;
				case 'generic':
					return ['dbget', 'dbadd', 'dbmod', 'dbdel'].indexOf(_state.recipe.action) === -1;
				default:
					return false;
			}
		});
	},
	getButtonDescription: function(type) {
		return buttons[type];
	},
	emitChange: function(actionType) {
		this.emit(CHANGE_EVENT, actionType);
	},
	addChangeListener: function(callback) {
		this.on(CHANGE_EVENT, callback);
	},
	removeChangeListener: function(callback) {
		this.removeListener(CHANGE_EVENT, callback);
	}
});

// Register to handle all updates from the dispatcher
AppDispatcher.register(function(payload) {
	var action = payload.action;

	switch(action.actionType) {
		case Constants.OPTIONS_CHANGE_ID:
			changeId(action.id);
			break;
		case Constants.OPTIONS_CHANGE_PASS:
			changePass(action.pass);
			break;
		case Constants.RECIPE_CHANGE_NAME:
			changeRecipeName(action.name);
			break;
		case Constants.RECIPE_SET_ACTION:
			setAction(action.action);
			break;
		case Constants.RECIPE_ADD_BUTTON:
			addButton(action.type);
			break;
		case Constants.RECIPE_REMOVE_BUTTON:
			removeButton(action.index);
			break;
		case Constants.RECIPE_UPDATE_BUTTON:
			updateButton(action.index, action.data);
			break;
		case Constants.RECIPE_RUN:
			runRecipe();
			break;
		case Constants.RECIPE_SAVE:
			saveRecipe();
			break;
		case Constants.RECIPE_LOAD:
			// @TODO
			break;
		case Constants.RECIPE_CLEAR:
			clearRecipe();
			break;
		case Constants.RECIPE_DELETE:
			deleteRecipe();
			break;
		default:
			return true;
	}

	// Trigger a UI change after handling the action
	AppStore.emitChange(action.actionType);

	return true;
});

module.exports = AppStore;
