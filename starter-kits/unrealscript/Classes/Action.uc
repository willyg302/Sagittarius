/**
 * Sagittarius - UnrealScript Starter Kit
 * Copyright 2013 WillyG Productions
 * @Authors: William Gaul
 */
class Action extends Object abstract;

const DBTYPE = "object_type";
const DBNAME = "object_name";

var protected string Handler;
var protected SagRequest request;

function Submit(string ModuleID, string QueryID)
{
	FinalizeRequest();
	request.SetModuleInfo(ModuleID, QueryID);
	request.Submit();
}

function InitializeRequest(SagRequest sr)
{
	sr.SetDestination(Handler);
	request = sr;
}

protected function FinalizeRequest()
{
	//
}