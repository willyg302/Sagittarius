class Sagittarius extends Actor;

var SagittariusLinkClient Link;

struct ModuleStruct
{
	var string ID;
	var Module m;
};

var array<ModuleStruct> Modules;

const LOG_TAG = 'Sagittarius';

var const enum ELogLevel
{
	LOG_None,
	LOG_Error,
	LOG_Warn,
	LOG_Info,
	LOG_Debug
} LogLevel;


function Initialize(string THost, int TPort)
{
	Link = Spawn(class'SagittariusLinkClient');
	Link.Initialize(self, THost, TPort);
}

function RegisterModule(Module m)
{
	local ModuleStruct ms;
	ms.ID = m.ID;
	ms.m = m;
	Modules.AddItem(ms);
	m.Initialize(self);
}

function Module GetModule(string ID)
{
	local int index;
	index = Modules.Find('ID', ID);
	if (index == INDEX_NONE)
	{
		LogWarn("GetModule() - module with ID " $ ID $ " does not exist");
		return None;
	}
	else
	{
		return Modules[index].m;
	}
}



function SubmitAction(string ModuleID, string ActionID, Action a)
{
	Link.Transmit(true, a.GetHandler(), ModuleID, ActionID, a.GetURLString());
}



/** CALLBACK FUNCTIONS **/

function OnTextReceived(string ModuleID, string ActionID, string Text)
{
	if (ModuleID == "builtin")
	{
		BuiltInOnTextReceived(ActionID, Text);
		return;
	}
	GetModule(ModuleID).OnTextReceived(ActionID, Text);
}

function OnCallbackReceived(string ModuleID, string ActionID)
{
	if (ModuleID == "builtin")
	{
		BuiltInOnCallbackReceived(ActionID);
		return;
	}
	GetModule(ModuleID).OnCallbackReceived(ActionID);
}

function BuiltInOnTextReceived(string ActionID, string Text)
{
	//
}

function BuiltInOnCallbackReceived(string ActionID)
{
	// @TODO: Test
	if (ActionID == "mail")
	{
		class'WorldInfo'.static.GetWorldInfo().Game.Broadcast(self, "Mail successfully sent!");
	}
}



/** MAIL **/

function SendMail(string Receiver, string Subject, string Message, optional string Sender = "")
{
	local string Contents;
	Contents = "recv=" $ Receiver $ "&subj=" $ Subject $ "&mesg=" $ Message;
	if (Sender != "")
	{
		Contents $= ("&send=" $ Sender);
	}
	Link.Transmit(true, "/mail", "builtin", "mail", Contents);
}


/** LOG FUNCTIONS **/

static function LogError(string msg, optional name cat = LOG_TAG)
{
	if (default.LogLevel > 0)
	{
		`LogError(cat, msg);
	}
}

static function LogWarn(string msg, optional name cat = LOG_TAG)
{
	if (default.LogLevel > 1)
	{
		`LogWarn(cat, msg);
	}
}

static function LogInfo(string msg, optional name cat = LOG_TAG)
{
	if (default.LogLevel > 2)
	{
		`LogInfo(cat, msg);
	}
}

static function LogDebug(string msg, optional name cat = LOG_TAG)
{
	if (default.LogLevel > 3)
	{
		`LogDebug(cat, msg);
	}
}


static function string GetXMLValue(string XMLTag, string Text)
{
	local int XMLTagStart, XMLTagEnd;
	XMLTagStart = InStr(Text, "<" $ XMLTag $ ">");
	if (XMLTagStart < 0)
	{
		return "";
	}
	XMLTagStart += (Len(XMLTag) + 2);
	XMLTagEnd = InStr(Text, "</" $ XMLTag $ ">");
	if (XMLTagEnd < XMLTagStart)
	{
		return "";
	}
	return Mid(Text, XMLTagStart, XMLTagEnd - XMLTagStart);
}


DefaultProperties
{
	LogLevel=LOG_Debug
}
