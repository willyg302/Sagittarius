var motd;

Sagittarius.prototype.getMOTD = function() {
	return motd;
};

Sagittarius.prototype.queryMOTD = function(callback) {
	var self = this;
	var ga = self.createAction('get')
	             .addFilter(ga.DBTYPE, 'motd')
	             .addFilter(ga.DBNAME, 'motd')
	             .addProjection('message', true)
	             .unique();
	self.submit(ga, function(data, err) {
		if (!err) {
			motd = self.encryption.decrypt(data.dbobjects[0].message, self.pass);
		}
		callback();
	});
};
