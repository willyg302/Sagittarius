---
title: UnrealScript
subtitle: The tutorial hub for the UnrealScript starter kit
template: tutorial.jade
---

## Basic Integration

### Copying Files

The easiest way to integrate the starter kit with your game is to simply copy all the .uc files into your source directory (which will be something similar to `\Development\Src\MyGame\Classes\`). They should compile successfully out of the box.

An alternative is to create a new directory just for Sagittarius, such as `\Development\Src\Sagittarius\Classes\`, and place the starter kit there. You will have to modify `DefaultEngine.ini` to let UDK know to compile the new classes:

```ini
[UnrealEd.EditorEngine]
+EditPackages=UTGame
+EditPackages=UTGameContent
+EditPackages=Sagittarius
+EditPackages=MyGame
```

Make sure to place Sagittarius before your game's directory, as the Sagittarius sources must be compiled first. This method is recommended to keep Sagittarius code separate from your projects. You should never have to touch any of the starter kit classes, and updating to a newer starter kit version will simply mean overwriting the contents of the `\Sagittarius\Classes\` folder.

### The GameInfo Class

A class called `SagittariusGame.uc` is included with the starter kit to show the minimum amount of code needed to get Sagittarius up and running. You should copy this code into your own GameInfo class. Make sure to replace `[APP ID HERE]` and `[APP PASSWORD HERE]` in the DefaultProperties block with your own application ID and password.

At this point Sagittarius will be fully integrated and ready to use, but it can't really do anything just yet. To start leveraging its power you will need to write some *modules*.

## Easy: MOTD Module

### Understanding Modules

Sagittarius is structured around the idea of <span class="label label-danger">MODULES</span> that perform <span class="label label-danger">ACTIONS</span>. If you look in the starter kit you will notice two base classes, `Action.uc` and `Module.uc`. The actions that Sagittarius is capable of performing are fixed; that is, you will never have to write a subclass of `Action.uc`. You *will*, however, have to create modules that use the actions available to Sagittarius.

In order to use a module you will have to **register** it to Sagittarius and **retrieve** it when you want to use it. In many ways Sagittarius acts as a "module manager". The great thing is that you can write and register as many modules as you'd like: a Server Module, a Login Module, and so on -- one for each of the features you'd like your game to support.

To better understand how modules work, let's write a simple Message of the Day Module.

### Uploading a MOTD

Before we start coding, we need to define what we want our MOTD to be and actually host one on our App Engine application. Our MOTD will be extremely simple, just a single string that we will call the "message". A full MOTD DBObject might look something like this:

```
object_type="motd"
object_name="motd"
message="Welcome to my game, have fun playing!"
```

The first two attributes are required, so we'll simply set them as `"motd"` to make filtering for the MOTD easier.

Now we need to upload our message. You can use the [Sagittarius Wizard](../../wizard) to do this. If this is your first time uploading a MOTD, set the action button to **Add** and add three **Add Attribute** buttons to set the attributes to the values listed above. If you already have a MOTD, you can set the action button to **Modify** instead to modify the message attribute.

### Defining Our Class

The first thing we'll do code-wise is create a new class extending from `Module.uc` and copy over all the necessary functions:

```
class MOTDModule extends Module;

function OnResponseReceived(string ActionID, SagResponse resp)
{
	super.OnResponseReceived(ActionID, resp);
	// When a response is received from the remote service
}

DefaultProperties
{
	ID="motd"
}
```

Save this file as `MOTDModule.uc` in your project's source directory. Every module you create should have at least this basic skeleton. Although you do not need to override the `OnResponseReceived()` function, you must specify a module ID in the DefaultProperties block. This ID will be used by Sagittarius to identify and retrieve instances of this module, and should be unique (otherwise, modules could be confused for each other).

### The Delegate Pattern

Anything that relies on an Internet connection is **asynchronous**. That is, we cannot predict how long it will take for us to send data to our App Engine application, or when the server will reply. Because of this, we cannot simply wait for a response; we want to be **notified** when a response is received. This is a job for [UnrealScript delegates](http://udn.epicgames.com/Three/UnrealScriptDelegates.html).

Sagittarius masks most of the complexity of delegates and event handling for you, piping all notifications through the `OnResponseReceived()` function we've already declared. However, your game will be interacting with your modules directly, so we need another layer of delegates within each module you make. Thankfully there is a very simple *delegate pattern* to follow:

```
class MOTDModule extends Module;

delegate OnMOTDReceivedDelegate();

function RegisterOnMOTDReceivedDelegate(delegate&lt;OnMOTDReceivedDelegate&gt; del)
{
	OnMOTDReceivedDelegate = del;
}

function OnResponseReceived(string ActionID, SagResponse resp)
{
	super.OnResponseReceived(ActionID, resp);
	OnMOTDReceivedDelegate();
}

DefaultProperties
{
	ID="motd"
}
```

A class (such as your GameInfo class) that wants to know when the Message of the Day has been received simply registers a function to call through `RegisterOnMOTDReceivedDelegate()`. When everything is done, `OnResponseReceived()` is called, and in turn `OnMOTDReceivedDelegate()`, which then in turn calls the function you registered.

We'll see this pattern in action a little later on, but for now you should remember how to set it up:

- Declare a delegate
- Make a function that registers a function to this delegate
- Call the delegate when you want to notify that something has been done

### Caching the MOTD

Every time you communicate with your App Engine application, you use a tiny bit of its [quota](https://developers.google.com/appengine/docs/quotas). If you go over the quota your application will go down (equivalent to a crash), so it's important to communicate only when absolutely necessary.

In the case of the Message of the Day, we expect the message to change approximately once every 24 hours -- not very often, in other words. Although the MOTD may be updated while the player is playing, we will assume that this scenario is very unlikely. So, we can get away with only querying for the MOTD *once*: upon starting the game.

The typical way to handle data from Sagittarius is to maintain a **local cache** of it. When you ask Sagittarius for new information, the local cache is updated. Although we might get the MOTD value often (every time the player exits to the main menu, for example), we are really only getting its cached value. Let's code this now:

```
class MOTDModule extends Module;

var string motd;

delegate OnMOTDReceivedDelegate();

function RegisterOnMOTDReceivedDelegate(delegate&lt;OnMOTDReceivedDelegate&gt; del)
{
	OnMOTDReceivedDelegate = del;
}

/**
 * Gets the cached MOTD value.
 */
function string GetMOTD()
{
	return motd;
}

/**
 * Gets and stores the MOTD from Sagittarius.
 */
function QueryMOTD()
{
	// @TODO
}

function OnResponseReceived(string ActionID, SagResponse resp)
{
	super.OnResponseReceived(ActionID, resp);
	OnMOTDReceivedDelegate();
}

DefaultProperties
{
	ID="motd"
}
```

We have added two new functions. You will call `GetMOTD()` whenever you want to know the MOTD, for example from a Scaleform GFx menu class. When you want to update the MOTD with the value on the server, you can call `QueryMOTD()`. This can be done when the game starts up, for example in a `PostBeginPlay()` function.

### Querying the MOTD</h2>

Since we only really want to *get* the latest MOTD from the server, our `QueryMOTD()` function will only need to implement a single action, appropriately called GetAction:

```
class MOTDModule extends Module;

var string motd;

delegate OnMOTDReceivedDelegate();

function RegisterOnMOTDReceivedDelegate(delegate&lt;OnMOTDReceivedDelegate&gt; del)
{
	OnMOTDReceivedDelegate = del;
}

/**
 * Gets the cached MOTD value.
 */
function string GetMOTD()
{
	return motd;
}

/**
 * Gets and stores the MOTD from Sagittarius.
 */
function QueryMOTD()
{
	local GetAction ga;
	ga = GetAction(Parent.CreateAction("get"));
	ga.AddFilter(ga.DBTYPE, "motd");
	ga.AddFilter(ga.DBNAME, "motd");
	ga.AddProjection("message", true);
	ga.Unique();
	SubmitAction("motdquery", ga);
}

function OnResponseReceived(string ActionID, SagResponse resp)
{
	super.OnResponseReceived(ActionID, resp);
	motd = resp.GetValue("message");
	OnMOTDReceivedDelegate();
}

DefaultProperties
{
	ID="motd"
}
```

Our added code shows how to make use of the actions bundled with the starter kit. First, we create a new instance of GetAction. Then we add our filters and projections to it. We only want to get the DBObject with `object_type=="motd"` and `object_name=="motd"`, so we add those filters using the special shortcut variables `DBTYPE` and `DBNAME` respectively. We only want to return the actual *message*, so we add a projection for that field. Since we expect there to be only one MOTD, we make the query unique. And finally, we submit the GetAction and assign it an ID of `"motdquery"` so that it can be identified later.

Any time that Sagittarius receives a reply from the server, the text will be routed to `OnResponseReceived()`. Therefore it is here that we want to parse the MOTD message and assign it to our local cache. Replies are encoded as a special SagResponse object, which provides a convenient `GetValue()` function to return the first value matching the specified key. Once we do that, our module is complete.

### Using Our MOTD Module

Since this is a simple tutorial, we'll just modify `SagittariusGame.uc` to fetch the MOTD one second after a level has been loaded and broadcast it to all players. In a more realistic scenario you'd probably fetch the MOTD upon startup and integrate the message into a menu or HUD element. Our modifications are as follows:

```
event PreBeginPlay()
{
	super.PreBeginPlay();
	Sag = Spawn(class'Sagittarius');
	Sag.Initialize(SagittariusAppID, SagittariusPass);
	Sag.RegisterModule(new class'MOTDModule');
}

function PostBeginPlay()
{
	super.PostBeginPlay();
	SetTimer(1.0, false, 'GrabMOTD');
}

function GrabMOTD()
{
	local MOTDModule motd;
	motd = MOTDModule(Sag.GetModule("motd"));
	motd.RegisterOnMOTDReceivedDelegate(PrintMOTD);
	motd.QueryMOTD();
}

function PrintMOTD()
{
	Broadcast(self, MOTDModule(Sag.GetModule("motd")).GetMOTD());
}
```

The first thing we do is **register** an instance of our MOTDModule to Sagittarius in `PreBeginPlay()`. In `PostBeginPlay()` we set a timer to call the function `GrabMOTD()`. In this function, we **retrieve** our module instance, register the function `PrintMOTD()` to its delegate, and ask it to query the server. Notice the use of delegates: when the module *does* receive a response from the server, we know our function `PrintMOTD()` will be called.

All `PrintMOTD()` really does is broadcast what is in our module's local cache. However, remember that this separation of functionality is necessary because web connections are asynchronous.

Now let's fire up a SagittariusGame. If all goes well, you should see something like this when the match starts up:

![unrealscript-1](../../img/unrealscript-1.jpg)

Congratulations, you have just written your first module!

## Medium: Server Browser

Coming soon!

## Special Functions</h1>

### Sending Mail

You can send an email any time from within UDK using the `SendMail()` function in `Sagittarius.uc`:

```
function SendMail(string Receiver, string Subject, string Message, optional string Sender = "")
```

The Sender parameter is a string referencing the subdomain of your application that you want the email to be sent from. For example, if your `Application Identifier` is "myapplication" and your Sender parameter is set to "donuts", then the recipient will receive an email from **donuts@myapplication.appspotmail.com**. Note that you do not have to specify a Sender; if you don't, it will default to "admin".

## Logging

Sagittarius has a built-in log system that is slightly more robust than the UDK ``log()` macro. It supports conditional logging via an enum defined in `Sagittarius.uc`:

```
var const enum ELogLevel
{
	LOG_None,
	LOG_Error,
	LOG_Warn,
	LOG_Info,
	LOG_Debug
} LogLevel;
```

You can set the logging level in the DefaultProperties block of `Sagittarius.uc`. The levels are defined roughly as follows:

- **LOG_None**: Log nothing at all
- **LOG_Error**: Log only errors, which are unrecoverable faults that should be handled
- **LOG_Warn**: Warnings are recoverable errors; there is a problem but the game can continue running
- **LOG_Info**: General important information about connections is logged by default
- **LOG_Debug**: Log everything, including debug information (which is typically verbose)

To use the logging system, you can call the following functions defined in `Sagittarius.uc`:

```
static function LogError(string msg, optional name cat = LOG_TAG)
static function LogWarn(string msg, optional name cat = LOG_TAG)
static function LogInfo(string msg, optional name cat = LOG_TAG)
static function LogDebug(string msg, optional name cat = LOG_TAG)
```

The optional `LOG_TAG` is a tag that will be enclosed in brackets preceding the message in the log. If you decide to specify it, you would typically use the name of the class that you are logging from. Remember that logging is filtered by the `LogLevel`, so if your logging level is `LOG_Warn` but you call `LogInfo()`, that message will not be logged.

Also, because all the logging functions are **static** you can use this system from any class:

```
class'Sagittarius'.static.LogError("The Servers are Busy at this time. Please try again later.");
MySagittariusInstance.LogInfo("I can also do this using an instance of Sagittarius!");
```
