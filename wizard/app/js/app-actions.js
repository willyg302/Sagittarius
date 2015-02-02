var AppDispatcher = require('./app-dispatcher');
var AppStore = require('./app-store');
var Constants = require('./constants');

var AppActions = {
	changeId: function(id) {
		AppDispatcher.handleViewAction({
			actionType: Constants.OPTIONS_CHANGE_ID,
			id: id
		});
	},
	changePass: function(pass) {
		AppDispatcher.handleViewAction({
			actionType: Constants.OPTIONS_CHANGE_PASS,
			pass: pass
		});
	},
	setAction: function(action) {
		AppDispatcher.handleViewAction({
			actionType: Constants.RECIPE_SET_ACTION,
			action: action
		});
	},
	addButton: function(type) {
		AppDispatcher.handleViewAction({
			actionType: Constants.RECIPE_ADD_BUTTON,
			type: type
		});
	},
	removeButton: function(index) {
		AppDispatcher.handleViewAction({
			actionType: Constants.RECIPE_REMOVE_BUTTON,
			index: index
		});
	},
	updateButton: function(index, data) {
		AppDispatcher.handleViewAction({
			actionType: Constants.RECIPE_UPDATE_BUTTON,
			index: index,
			data: data
		});
	},
	clearRecipe: function() {
		AppDispatcher.handleViewAction({
			actionType: Constants.RECIPE_CLEAR
		});
	}
	/*
	: function() {
		AppDispatcher.handleViewAction({
			actionType: Constants.RECIPE_RUN
		});
	},
	: function() {
		AppDispatcher.handleViewAction({
			actionType: Constants.RECIPE_SAVE
		});
	},
	: function() {
		AppDispatcher.handleViewAction({
			actionType: Constants.RECIPE_LOAD
		});
	},
	: function() {
		AppDispatcher.handleViewAction({
			actionType: Constants.RECIPE_CLEAR
		});
	},
	: function() {
		AppDispatcher.handleViewAction({
			actionType: Constants.RECIPE_DELETE
		});
	}
	*/
};

module.exports = AppActions;
