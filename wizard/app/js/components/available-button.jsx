/** @jsx React.DOM */

var React = require('react');

var AppActions = require('../app-actions');
var AppStore = require('../app-store');

var Icon = require('./icon.jsx');

var AvailableButton = React.createClass({
	render: function() {
		var desc = AppStore.getButtonDescription(this.props.type);
		return (
			<Icon name={this.props.type} desc={desc} click={this._onClick} />
		);
	},
	_onClick: function() {
		AppActions.addButton(this.props.type);
	}
});

module.exports = AvailableButton;
