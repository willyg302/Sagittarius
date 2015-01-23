/**
 * Sagittarius - UnrealScript Starter Kit
 * Copyright 2013 WillyG Productions
 * @Authors: William Gaul
 */
class AddAction extends Action;

var private array<string> Attributes;

function AddAttribute(string field, string value, optional bool bEncrypt = false)
{
	request.AddURLPair("a", field $ "::" $ value, bEncrypt);
}

DefaultProperties
{
	Handler="/dbadd"
}