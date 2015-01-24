class MOTDModule extends Module;

var string motd;

delegate OnMOTDReceivedDelegate();

function RegisterOnMOTDReceivedDelegate(delegate<OnMOTDReceivedDelegate> del)
{
	OnMOTDReceivedDelegate = del;
}

/**
 * Gets the cached MOTD value.
 */
function string GetMOTD()
{
	return motd;
}

/**
 * Gets and stores the MOTD from Sagittarius.
 */
function QueryMOTD()
{
	local GetAction ga;
	ga = GetAction(Parent.CreateAction("get"));
	ga.AddFilter(ga.DBTYPE, "motd");
	ga.AddFilter(ga.DBNAME, "motd");
	ga.AddProjection("message", true);
	ga.Unique();
	SubmitAction("motdquery", ga);
}

function OnResponseReceived(string ActionID, SagResponse resp)
{
	super.OnResponseReceived(ActionID, resp);
	motd = resp.GetValue("message");
	OnMOTDReceivedDelegate();
}

DefaultProperties
{
	ID="motd"
}
