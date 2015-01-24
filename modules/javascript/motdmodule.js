var motd;

Sagittarius.prototype.GetMOTD = function() {
	return motd;
};

Sagittarius.prototype.QueryMOTD = function(callback) {
	var ga = this.CreateAction('get')
	             .AddFilter(ga.DBTYPE, 'motd')
	             .AddFilter(ga.DBNAME, 'motd')
	             .AddProjection('message', true)
	             .Unique();
	var pass = this.pass;
	this.SubmitAction(ga, function(data) {
		motd = Encryption.Decrypt(data.dbobjects[0].message, pass);
		callback();
	});
};
