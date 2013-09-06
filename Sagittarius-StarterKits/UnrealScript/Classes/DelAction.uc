/**
 * Sagittarius - UnrealScript Starter Kit
 * Copyright 2013 WillyG Productions
 * @Authors: William Gaul
 */
class DelAction extends GetAction;

var protected bool bReturnsResults;

function SetReturnsResults()
{
	bReturnsResults = true;
}

protected function FinalizeRequest()
{
	super.FinalizeRequest();
	if (bReturnsResults)
	{
		request.AddURLPair("rres", "true", false);
	}
}

DefaultProperties
{
	Handler="/dbdel"
	bReturnsResults=false
}