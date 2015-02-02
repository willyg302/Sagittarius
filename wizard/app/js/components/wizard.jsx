/** @jsx React.DOM */

var React = require('react');

var Button = require('react-bootstrap/Button');
var ButtonToolbar = require('react-bootstrap/ButtonToolbar');
var Input = require('react-bootstrap/Input');
var Panel = require('react-bootstrap/Panel');

var AppActions = require('../app-actions');
var AppStore = require('../app-store');

var Action = require('./action.jsx');
var AvailableButton = require('./available-button.jsx');
var Icon = require('./icon.jsx');
var WatchStoreMixin = require('./watch-store-mixin');

var Wizard = React.createClass({
	mixins: [WatchStoreMixin],

	render: function() {
		var available = AppStore.getAvailableButtons();
		return (
			<div>
				<Panel header={<h3>Global Options</h3>}>
					<form className="form-inline">
						<Input type="text" ref="id" value={this.state.id} label="App ID" onChange={this._onSetId} />
						<Input type="password" ref="pass" value={this.state.pass} label="Password" onChange={this._onSetPass} />
					</form>
				</Panel>
				<Panel header={<h3>Available Buttons</h3>}>
					{Object.keys(available).map(function(button) {
						return <AvailableButton key={button} type={button} />;
					})}
				</Panel>
				<Panel header={<h3>Recipe</h3>}>
					<Action action={this.state.action} />
					{this.state.recipe.map(function(button, i) {
						return <Icon key={i} name={button.type} desc='TODO' />;
					})}
					<ButtonToolbar className="recipe-menu">
						<Button bsStyle="primary">Run</Button>
						<Button>Save</Button>
						<Button>Load</Button>
						<Button onClick={this._onClear}>Clear</Button>
						<Button>Delete</Button>
					</ButtonToolbar>
				</Panel>
				<Panel header={<h3>Output</h3>}>
					<div id="output">{JSON.stringify(this.state)}</div>
				</Panel>
			</div>
		);
	},
	_onSetId: function() {
		AppActions.changeId(this.refs.id.getValue());
	},
	_onSetPass: function() {
		AppActions.changePass(this.refs.pass.getValue());
	},
	_onSubmit: function() {
		//
	},
	_onClear: function() {
		AppActions.clearRecipe();
	}
});

module.exports = Wizard;
