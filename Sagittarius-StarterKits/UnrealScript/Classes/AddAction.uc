/**
 * Sagittarius - UnrealScript Starter Kit
 * Copyright 2013 WillyG Productions
 * @Authors: William Gaul
 */
class AddAction extends Action;

var private array<string> Attributes;

function AddAttribute(string field, string value, optional bool bEncrypt = false)
{
	Attributes.AddItem(Encrypt(field $ "::" $ value, bEncrypt));
}

function string GetURLString()
{
	local string str, delim;
	local int i;
	str = "";
	delim = "";
	for (i = 0; i < Attributes.Length; i++)
	{
		str $= (delim $ "a=" $ Attributes[i]);
		delim = "&";
	}
	return str;
}

DefaultProperties
{
	Handler="/dbadd"
}