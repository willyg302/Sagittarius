class Module extends Object abstract;

var string ID;

var Sagittarius Parent;

function Initialize(Sagittarius s)
{
	Parent = s;
}

function SubmitAction(string ActionID, Action a)
{
	Parent.SubmitAction(ID, ActionID, a);
}

function OnTextReceived(string ActionID, string Text)
{
	// When any text is received from remote service
}

function OnCallbackReceived(string ActionID)
{
	// When remote transmission is fully completed
}
