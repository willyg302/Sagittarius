/**
 * Sagittarius - UnrealScript Starter Kit
 * Copyright WillyG Productions
 * @Authors: William Gaul
 */
class GetAction extends Action;

var protected int ResultLimit, ResultOffset;

function AddFilter(string field, string value, optional bool bEncrypt = false)
{
	request.AddURLPair("f", field $ "::" $ value, bEncrypt);
}

function AddProjection(string field, optional bool bEncrypt = false)
{
	request.AddURLPair("p", field $ (bEncrypt ? "~" : ""), false);
}

function SetLimit(int rl)
{
	ResultLimit = rl;
}

function SetOffset(int ro)
{
	ResultOffset = ro;
}

function Unique()
{
	ResultLimit = 1;
}

protected function FinalizeRequest()
{
	super.FinalizeRequest();
	request.AddURLPair("rlim", string(ResultLimit), false);
	request.AddURLPair("roff", string(ResultOffset), false);
}

DefaultProperties
{
	Handler="/dbget"
	ResultLimit=20
	ResultOffset=0
}