/**
 * Sagittarius - UnrealScript Starter Kit
 * Copyright 2013 WillyG Productions
 * @Authors: William Gaul
 */
class SagittariusLinkClient extends TcpLink;

var string TargetHost;
var int TargetPort;

/* The only class that this link client actually communicates with. In this way
 * Sagittarius.uc serves as a middleman and "masks" this class.
 */
var Sagittarius Parent;

struct Connection
{
	var bool bPost;
	var string dest, data, mID, qID;
};

// To avoid multiple TCP connections from overriding each other.
var bool bIsBusy;

/* Queue of connections to handle multiple requests and prevent them from overriding
 * each other. They are in FIFO order, so ConnectionQueue[0] is always executed next.
 */
var array<Connection> ConnectionQueue;

var Connection CurrentConnection;

function Initialize(Sagittarius s, string THost, int TPort)
{
	Parent = s;
	TargetHost = THost;
	TargetPort = TPort;
}

/**
 * Begins the transmission process by storing a connection in the ConnectionQueue. If
 * the client is currently serving another connection, this connection waits in the queue
 * until it can be taken.
 *
 * @param bPost - true if this is a POST request (false if it's a GET)
 * @param  dest - the destination webpage on the TargetHost
 * @param   mID - ID of the module that generated this transmission
 * @param   qID - ID of the query/message (for callback handling)
 * @param  data - the data to transmit, or the null string "" if no data is specified
 */
function Transmit(bool bPost, string dest, string mID, string qID, optional string data)
{
	local Connection c;
	c.bPost = bPost;
	c.dest = dest;
	c.mID = mID;
	c.qID = qID;
	c.data = data;
	ConnectionQueue.AddItem(c);
	if (!bIsBusy)
	{
		StartTransmission();
	}
}

function StartTransmission()
{
	if (ConnectionQueue.Length == 0)
	{
		return;
	}
	bIsBusy = true;
	CurrentConnection = ConnectionQueue[0];
	ConnectionQueue.Remove(0, 1);
	Parent.LogDebug("Resolving: " $ TargetHost);
	Resolve(TargetHost);
}

event Resolved(IpAddr Addr)
{
	Parent.LogInfo(TargetHost $ " resolved to "$ IpAddrToString(Addr));
	Addr.Port = TargetPort;
	Parent.LogDebug("Bound to port: " $ BindPort());
	if (!Open(Addr))
	{
		Parent.LogError("Failed to open port");
	}
}

event ResolveFailed()
{
	Parent.LogError("Unable to resolve " $ TargetHost);
	// You could retry resolving here if you have an alternative remote host.
}

event Opened()
{
	local string newline;
	newline = chr(13) $ chr(10);

	Parent.LogInfo("TCP connection opened for module " $ CurrentConnection.mID $ " and query " $ CurrentConnection.qID);

	if (CurrentConnection.bPost)
	{
		SendText("POST " $ CurrentConnection.dest $ " HTTP/1.0" $ newline);
		SendText("Host: " $ TargetHost $ newline);
		SendText("User-Agent: SagittariusLinkClient/1.0" $ newline);
		SendText("Content-Type: application/x-www-form-urlencoded" $ newline);
		SendText("Content-Length: " $ Len(CurrentConnection.data) $ newline);
		SendText(newline);
		SendText(CurrentConnection.data $ newline);
	}
	else
	{
		SendText("GET " $ CurrentConnection.dest $ CurrentConnection.data $ " HTTP/1.0" $ newline);
		SendText("Host: " $ TargetHost $ newline);
		SendText(newline);
	}
	SendText(newline);
	SendText(newline);

	Parent.LogDebug("End TCP connection");
}

event Closed()
{
	Parent.LogInfo("TCP connection closed for module " $ CurrentConnection.mID $ " and query " $ CurrentConnection.qID);
	Parent.OnCallbackReceived(CurrentConnection.mID, CurrentConnection.qID);
	bIsBusy = false;

	// Retry transmission in case there are any queued messages (if not, nothing happens)
	StartTransmission();
}

event ReceivedText(string Text)
{
	// We store the response between <resp></resp> XML tags, so we grab it here
	Text = Parent.GetXMLValue("resp", Text);
	Parent.LogDebug("Received Text: " $ Text);
	Parent.OnTextReceived(CurrentConnection.mID, CurrentConnection.qID, Text);
}


DefaultProperties
{
	bIsBusy=false
}