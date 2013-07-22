class DelAction extends GetAction;

var private bool bReturnsResults;

function SetReturnsResults()
{
	bReturnsResults = true;
}

function string GetURLString()
{
	local string str;
	str = super.GetURLString();
	if (bReturnsResults)
	{
		str $= "&rres=true";
	}
	return str;
}

DefaultProperties
{
	Handler="/dbdel"
	bReturnsResults=false
}