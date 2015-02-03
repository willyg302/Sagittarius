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
var RecipeButton = require('./recipe-button.jsx');
var WatchStoreMixin = require('./watch-store-mixin');

var Wizard = React.createClass({
	mixins: [WatchStoreMixin],

	render: function() {
		return (
			<div>
				<Panel header={<h3>Global Options</h3>}>
					<form className="form-inline">
						<Input type="text" ref="id" value={this.state.id} label="App ID" onChange={this._onSetId} />
						<Input type="password" ref="pass" value={this.state.pass} label="Password" onChange={this._onSetPass} />
					</form>
				</Panel>
				<Panel header={<h3>Available Buttons</h3>}>
					{AppStore.getAvailableButtons().map(function(button) {
						return <AvailableButton key={button} type={button} />;
					})}
				</Panel>
				<Panel header={<h3>Recipe: <input className="recipe-name" type="text" ref="recipe"
				                                  value={this.state.recipe.name} onChange={this._onSetRecipeName} /></h3>}>
					<Action action={this.state.recipe.action} />
					{this.state.recipe.buttons.map(function(button, i) {
						return <RecipeButton key={i} type={button.type} index={i} />;
					})}
					<ButtonToolbar className="recipe-menu">
						<Button bsStyle="primary" onClick={this._onRun}>Run</Button>
						<Button onClick={this._onSave}>Save</Button>
						<Button onClick={this._onLoad}>Load</Button>
						<Button onClick={this._onClear}>Clear</Button>
						<Button onClick={this._onDelete}>Delete</Button>
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
	_onSetRecipeName: function() {
		AppActions.changeRecipeName(this.refs.recipe.getDOMNode().value);
	},
	_onRun: function() {
		AppActions.runRecipe();
	},
	_onSave: function() {
		AppActions.saveRecipe();
	},
	_onLoad: function() {
		AppActions.loadRecipe();
	},
	_onClear: function() {
		AppActions.clearRecipe();
	},
	_onDelete: function() {
		AppActions.deleteRecipe();
	}
});

module.exports = Wizard;
