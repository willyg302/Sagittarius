/**
 * Sagittarius - UnrealScript Starter Kit
 * Copyright 2013 WillyG Productions
 * @Authors: William Gaul
 */
class Module extends Object abstract;

var string ID;

var Sagittarius Parent;

function Initialize(Sagittarius s)
{
	Parent = s;
}

function SubmitAction(string QueryID, Action a)
{
	a.Submit(ID, QueryID);
}

function OnResponseReceived(string ActionID, SagResponse resp)
{
	// When a response is received from the remote service
}