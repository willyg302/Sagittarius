class ModAction extends GetAction;

var private array<string> Modifications;
var private bool bReturnsResults;

function AddModification(string field, string value)
{
	Modifications.AddItem(field $ "::" $ value);
}

function SetReturnsResults()
{
	bReturnsResults = true;
}

function string GetURLString()
{
	local string str;
	local int i;
	str = super.GetURLString();
	if (bReturnsResults)
	{
		str $= "&rres=true";
	}
	if (Modifications.Length > 0)
	{
		for (i = 0; i < Modifications.Length; i++)
		{
			str $= ("&m=" $ Modifications[i]);
		}
	}
	return str;
}

DefaultProperties
{
	Handler="/dbmod"
	bReturnsResults=false
}