var Dispatcher = require('flux').Dispatcher;
var copyProperties = require('react/lib/copyProperties');

var AppDispatcher = copyProperties(new Dispatcher(), {

	/**
	 * These actions come from a view element (user input, UI, etc.).
	 */
	handleViewAction: function(action) {
		this.dispatch({
			source: 'VIEW_ACTION',
			action: action
		});
	}
});

module.exports = AppDispatcher;
