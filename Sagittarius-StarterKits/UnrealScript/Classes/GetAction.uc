/**
 * Sagittarius - UnrealScript Starter Kit
 * Copyright 2013 WillyG Productions
 * @Authors: William Gaul
 */
class GetAction extends Action;

var protected int ResultLimit, ResultOffset;
var protected array<string> Filters, Projections;

function AddFilter(string field, string value, optional bool bEncrypt = false)
{
	Filters.AddItem(Encrypt(field $ "::" $ value, bEncrypt));
}

function AddProjection(string field, optional bool bEncrypt = false)
{
	Projections.AddItem((bEncrypt ? "~" : "") $ field);
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

function string GetURLString()
{
	local string str;
	local int i;
	str = "rlim=" $ ResultLimit $ "&roff=" $ ResultOffset;
	if (Filters.Length > 0)
	{
		for (i = 0; i < Filters.Length; i++)
		{
			str $= ("&f=" $ Filters[i]);
		}
	}
	if (Projections.Length > 0)
	{
		for (i = 0; i < Projections.Length; i++)
		{
			str $= ("&p=" $ Projections[i]);
		}
	}
	return str;
}

DefaultProperties
{
	Handler="/dbget"
	ResultLimit=20
	ResultOffset=0
}