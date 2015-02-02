var React = require('react');

var AppStore = require('../app-store');

var WatchStoreMixin = {
	getInitialState: function() {
		return AppStore.getState();
	},
	componentDidMount: function() {
		AppStore.addChangeListener(this._onChange);
	},
	componentWillUnmount: function() {
		AppStore.removeChangeListener(this._onChange);
	},

	/**
	 * Event handler for change events coming from the AppStore.
	 */
	_onChange: function(actionType) {
		this.setState(AppStore.getState(), function() {
			if (typeof this._onProfileChange === 'function') {
				this._onProfileChange(actionType);
			}
		});
	}
};

module.exports = WatchStoreMixin;
