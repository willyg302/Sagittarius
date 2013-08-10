/**
 * Sagittarius - UnrealScript Starter Kit
 * Copyright 2013 WillyG Productions
 * @Authors: William Gaul
 */
class SagResponse extends Object;

var bool bWasSuccessful;
var private JsonObject DBObjects;
var Sagittarius Parent;

function Decode(string Text, Sagittarius s)
{
	local JsonObject temp;
	temp = class'JsonObject'.static.DecodeJson(Text);
	bWasSuccessful = (temp.GetStringValue("success") == "y");
	DBObjects = temp.GetObject("dbobjects");
	Parent = s;
}

function string GetValue(string key)
{
	local string ret;
	if (DBObjects == none)
	{
		return "";
	}
	if (DBObjects.ObjectArray.Length == 0)
	{
		return "";
	}
	ret = DBObjects.ObjectArray[0].GetStringValue(key);
	if (InStr(ret, "~") == 0)
    {
        ret = Parent.Decrypt(ret);
    }
	return ret;
}

function array<string> GetValues(string key)
{
	local array<string> ret;
	local string temp;
	local int i;
	if (DBObjects == none)
	{
		return ret;
	}
	for (i = 0; i < DBObjects.ObjectArray.Length; i++)
	{
		temp = DBObjects.ObjectArray[i].GetStringValue(key);
		if (InStr(temp, "~") == 0)
		{
			temp = Parent.Decrypt(temp);
		}
		ret.AddItem(temp);
	}
	return ret;
}

function array<JsonObject> GetDBObjects()
{
	return DBObjects.ObjectArray;
}