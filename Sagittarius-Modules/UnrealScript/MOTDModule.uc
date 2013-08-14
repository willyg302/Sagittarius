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

function OnTextReceived(string ActionID, SagResponse resp)
{
	super.OnTextReceived(ActionID, resp);
	motd = resp.GetValue("message");
}

function OnCallbackReceived(string ActionID)
{
	super.OnCallbackReceived(ActionID);
	OnMOTDReceivedDelegate();
}

DefaultProperties
{
	ID="motd"
}
