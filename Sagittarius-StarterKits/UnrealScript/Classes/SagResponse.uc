/**
 * Sagittarius - UnrealScript Starter Kit
 * Copyright 2013 WillyG Productions
 * @Authors: William Gaul
 */
class SagResponse extends Object;

var private JsonObject response;
var bool bWasSuccessful;
var string ErrorMsg;
var Sagittarius Parent;

function Decode(string Text, Sagittarius s)
{
	response = class'JsonObject'.static.DecodeJson(Text);
	bWasSuccessful = (response.GetStringValue("success") == "y");
	ErrorMsg = response.GetStringValue("success");
	Parent = s;
}

function string GetValue(string key)
{
	local string ret;
	local JsonObject DBObjects;
	DBObjects = response.GetObject("dbobjects");
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
	local JsonObject DBObjects;
	DBObjects = response.GetObject("dbobjects");
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
	return response.GetObject("dbobjects").ObjectArray;
}