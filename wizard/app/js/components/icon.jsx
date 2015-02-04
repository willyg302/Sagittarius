/** @jsx React.DOM */

var React = require('react');

var OverlayTrigger = require('react-bootstrap/OverlayTrigger');
var Tooltip = require('react-bootstrap/Tooltip');

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
					<img src={"/static/img/" + this.props.name + ".png"} />
				</a>
			</OverlayTrigger>
		);
	},
	_onClick: function(e) {
		e.preventDefault();
		this.props.click();
	}
});

module.exports = Icon;
