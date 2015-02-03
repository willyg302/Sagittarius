/** @jsx React.DOM */

var React = require('react');

var AppActions = require('../app-actions');
var AppStore = require('../app-store');

var ModalIcon = require('./modal-icon.jsx');

var RecipeButton = React.createClass({
	render: function() {
		var desc = AppStore.getButtonDescription(this.props.type);
		var modalBody = (
			<div />
		);
		return (
			<span onContextMenu={this._onRemove}>
				<ModalIcon name={this.props.type} desc={desc} modalBody={modalBody}
				           cancel="Cancel" primary="OK" />
			</span>
		);
	},
	_onRemove: function(e) {
		e.preventDefault();  // Must be done with lower-level events
		AppActions.removeButton(this.props.index);
	}
});

module.exports = RecipeButton;
