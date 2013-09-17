class ServerModule extends Module;

struct Server
{
	var string ServerName, IP, MapName;
};

var array<Server> Servers;

delegate OnServerListReceivedDelegate();
delegate OnServerAddedDelegate();

function RegisterOnServerListReceivedDelegate(delegate<OnServerListReceivedDelegate> del)
{
	OnServerListReceivedDelegate = del;
}

function RegisterOnServerAddedDelegate(delegate<OnServerAddedDelegate> del)
{
	OnServerAddedDelegate = del;
}

function string GetIPOfServer(int index)
{
	return Servers[index].IP;
}

function string GetNameOfServer(int index)
{
	return Servers[index].ServerName;
}

function string GetMapOfServer(int index)
{
	return Servers[index].MapName;
}

function int NumServers()
{
	return Servers.Length;
}

/**
 * Updates the server list from Sagittarius.
 */
function QueryServerList()
{
	local GetAction ga;
	ga = GetAction(Parent.CreateAction("get"));
	ga.AddFilter(ga.DBTYPE, "server");
	ga.AddProjection(ga.DBNAME);
	ga.AddProjection("ip", true); // Encrypt IP to be safe
	ga.AddProjection("map");
	SubmitAction("serverlist", ga);
}

/**
 * Adds a server to Sagittarius.
 */
function AddServer(string ServerName, string MapName)
{
	local AddAction aa;
	aa = AddAction(Parent.CreateAction("add"));
	aa.AddAttribute(aa.DBTYPE, "server"); // Don't forget we need to set this filter!
	aa.AddAttribute(aa.DBNAME, ServerName);
	aa.AddAttribute("ip", "{{IP}}", true);
	aa.AddAttribute("map", MapName);
	SubmitAction("addserver", aa);
}

/**
 * Removes a server with the given IP from Sagittarius.
 */
function RemoveServer(optional string IP = "{{IP}}")
{
	local DelAction da;
	da = DelAction(Parent.CreateAction("del"));
	da.AddFilter(da.DBTYPE, "server");
	da.AddFilter("ip", IP, true);
	da.Unique(); // There should be only one server per IP
	da.SetReturnsResults();
	da.AddProjection("ip", true); // Return the IP for post-remove handling
	SubmitAction("removeserver", da);
}

function ParseServerList(array<JsonObject> JsonServers)
{
	local int i;
	local Server temp;
	for (i = 0; i < JsonServers.Length; i++)
	{
		temp.ServerName = JsonServers[i].GetStringValue("object_name");
		temp.IP = JsonServers[i].GetStringValue("ip");
		temp.MapName = JsonServers[i].GetStringValue("map");
		Servers.AddItem(temp);
	}
}

function OnResponseReceived(string ActionID, SagResponse resp)
{
	super.OnResponseReceived(ActionID, resp);
	if (ActionID == "serverlist")
	{
		Servers.Length = 0; // Make sure to empty server list when we get new ones!
		ParseServerList(resp.GetDBObjects());
		OnServerListReceivedDelegate();
	}
	else if (ActionID == "addserver")
	{
		OnServerAddedDelegate();
	}
	else if (ActionID == "removeserver")
	{
		// Do nothing?
	}
}

DefaultProperties
{
	ID="server"
}