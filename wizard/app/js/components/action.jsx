/** @jsx React.DOM */

var React = require('react');

var Input = require('react-bootstrap/Input');

var AppActions = require('../app-actions');
var AppStore = require('../app-store');

var ModalIcon = require('./modal-icon.jsx');

var Action = React.createClass({
	getInitialState: function() {
		return {
			action: this.props.action
		};
	},
	render: function() {
		var actions = AppStore.getActions();
		var modalBody = (
			<div>
				<Input type="select" ref="action" value={this.state.action} label="Choose Action" onChange={this._onChange}
				       help="Choose the action you want your recipe to carry out.">
					{Object.keys(actions).map(function(action) {
						return <option key={action} value={action}>{actions[action]}</option>;
					})}
				</Input>
			</div>
		);
		return (
			<ModalIcon name={this.props.action} desc={actions[this.props.action]} modalBody={modalBody} cancel="Cancel"
			           primary="Select" onClickPrimary={this._onClickSave} onOpen={this._onOpen} />
		);
	},
	_onChange: function() {
		this.setState({
			action: this.refs.action.getValue()
		});
	},
	_onClickSave: function() {
		AppActions.setAction(this.state.action);
	},
	_onOpen: function() {
		this.setState(this.getInitialState());
	}
});

module.exports = Action;
