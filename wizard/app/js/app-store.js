var EventEmitter = require('events').EventEmitter;
var merge = require('react/lib/merge');

var AppDispatcher = require('./app-dispatcher');
var Constants = require('./constants');


var CHANGE_EVENT = 'change';

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
	action: 'dbget',
	recipe: []
};


function changeId(id) {
	_state.id = id;
}

function changePass(pass) {
	_state.pass = pass;
}

function setAction(action) {
	_state.action = action;
}

function addButton(type) {
	_state.recipe.push({
		type: type
	});
}

function clearRecipe() {
	_state.recipe = [];
}


var AppStore = merge(EventEmitter.prototype, {
	getState: function() {
		return _state;
	},
	getActions: function() {
		return actions;
	},
	getAvailableButtons: function() {
		return buttons;  // @TODO
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
			break;
		case Constants.RECIPE_SAVE:
			break;
		case Constants.RECIPE_LOAD:
			break;
		case Constants.RECIPE_CLEAR:
			clearRecipe();
			break;
		case Constants.RECIPE_DELETE:
			break;
		default:
			return true;
	}

	// Trigger a UI change after handling the action
	AppStore.emitChange(action.actionType);

	return true;
});

module.exports = AppStore;
