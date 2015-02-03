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
	changeRecipeName: function(name) {
		AppDispatcher.handleViewAction({
			actionType: Constants.RECIPE_CHANGE_NAME,
			name: name
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
	runRecipe: function() {
		AppDispatcher.handleViewAction({
			actionType: Constants.RECIPE_RUN
		});
	},
	saveRecipe: function() {
		AppDispatcher.handleViewAction({
			actionType: Constants.RECIPE_SAVE
		});
	},
	loadRecipe: function() {
		AppDispatcher.handleViewAction({
			actionType: Constants.RECIPE_LOAD
		});
	},
	clearRecipe: function() {
		AppDispatcher.handleViewAction({
			actionType: Constants.RECIPE_CLEAR
		});
	},
	deleteRecipe: function() {
		AppDispatcher.handleViewAction({
			actionType: Constants.RECIPE_DELETE
		});
	}
};

module.exports = AppActions;
