/** @jsx React.DOM */

var React = require('react');

var Button = require('react-bootstrap/Button');
var ButtonToolbar = require('react-bootstrap/ButtonToolbar');
var Input = require('react-bootstrap/Input');
var OverlayTrigger = require('react-bootstrap/OverlayTrigger');
var Panel = require('react-bootstrap/Panel');
var Tooltip = require('react-bootstrap/Tooltip');


var buttons = [
	{
		name: 'filter',
		desc: 'Add Filter'
	},
	{
		name: 'project',
		desc: 'Add Projection'
	},
	{
		name: 'attribute',
		desc: 'Add Attribute'
	},
	{
		name: 'modification',
		desc: 'Modify Attribute'
	},
	{
		name: 'limit',
		desc: 'Set Limit'
	},
	{
		name: 'offset',
		desc: 'Set Offset'
	},
	{
		name: 'returns',
		desc: 'Returns Results'
	},
	{
		name: 'generic',
		desc: 'Generic Parameter'
	}
];


var Icon = React.createClass({
	getDefaultProps: function() {
		return {
			position: 'top'
		};
	},
	render: function() {
		var tooltip = <Tooltip>{this.props.desc}</Tooltip>;
		return (
			<OverlayTrigger placement={this.props.position} overlay={tooltip}>
				<a className={"icon " + this.props.name} onClick={this._onClick}>
					<img src={"static/img/" + this.props.name + ".png"} />
				</a>
			</OverlayTrigger>
		);
	},
	_onClick: function(e) {
		e.preventDefault();
		this.props.click();
	}
});


var Wizard = React.createClass({
	getInitialState: function() {
		return {
			id: '',
			pass: ''
		};
	},
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
					{buttons.map(function(button, i) {
						return <Icon key={i} name={button.name} desc={button.desc} click={this._onSubmit} />;
					}, this)}
				</Panel>
				<Panel header={<h3>Recipe</h3>}>
					<Icon name='dbadd' desc='Add' />
					<ButtonToolbar className="recipe-menu">
						<Button bsStyle="primary">Run</Button>
						<Button>Save</Button>
						<Button>Load</Button>
						<Button>Clear</Button>
						<Button>Delete</Button>
					</ButtonToolbar>
				</Panel>
				<Panel header={<h3>Output</h3>}>
					<div id="output" />
				</Panel>
			</div>
		);
	},
	_onSetId: function() {
		this.setState({
			id: this.refs.id.getValue()
		});
	},
	_onSetPass: function() {
		this.setState({
			pass: this.refs.pass.getValue()
		});
	},
	_onSubmit: function() {
		//
	}
});

module.exports = Wizard;
