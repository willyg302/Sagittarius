---
title: Java
subtitle: The tutorial hub for the Java starter kit
template: tutorial.jade
---

# Basic Integration

Copy the `sagittarius` package into the `src/` directory of your project and the `LIB` folder into a convenient place in your project's tree. Make sure to add the JARs inside the `LIB` folder as dependencies for your project.

Once you have added all files without errors, creating an instance of Sagittarius is very simple:

```java
public static final String APP_ID = [APP ID HERE];
public static final String APP_PASS = [APP PASSWORD HERE];

public static void main(String[] args) {
	Sagittarius sag = new Sagittarius(APP_ID, APP_PASS);
}
```

Make sure to replace `[APP ID HERE]` and `[APP PASSWORD HERE]` with your own application ID and password. At this point Sagittarius will be fully integrated and ready to use, but it can't really do anything just yet. To start leveraging its power you will need to write some *modules*.

# Easy: MOTD Module

## Understanding Modules

Sagittarius is structured around the idea of <span class="label label-danger">MODULES</span> that perform <span class="label label-danger">ACTIONS</span>. If you look in the starter kit you will notice two base classes, `Action.java` and `Module.java`. The actions that Sagittarius is capable of performing are fixed; that is, you will never have to write a subclass of `Action.java`. You *will*, however, have to create modules that use the actions available to Sagittarius.

In order to use a module you will have to **register** it to Sagittarius and **retrieve** it when you want to use it. In many ways Sagittarius acts as a "module manager". The great thing is that you can write and register as many modules as you'd like: a Server Module, a Login Module, and so on -- one for each of the features you'd like your game to support.

To better understand how modules work, let's write a simple Message of the Day Module.

## Uploading a MOTD

Before we start coding, we need to define what we want our MOTD to be and actually host one on our App Engine application. Our MOTD will be extremely simple, just a single string that we will call the "message". A full MOTD DBObject might look something like this:

```
object_type="motd"
object_name="motd"
message="Welcome to my game, have fun playing!"
```

The first two attributes are required, so we'll simply set them as `"motd"` to make filtering for the MOTD easier.

Now we need to upload our message. You can use the [Sagittarius Wizard](../../wizard) to do this. If this is your first time uploading a MOTD, set the action button to **Add** and add three **Add Attribute** buttons to set the attributes to the values listed above. If you already have a MOTD, you can set the action button to **Modify** instead to modify the message attribute.

## Defining Our Class

The first thing we'll do code-wise is create a new class extending from `Module.java` and copy over all the necessary functions:

```java
import sagittarius.Module;
import sagittarius.Sagittarius;
import sagittarius.SagResponse;

public class MOTDModule extends Module {

	public MOTDModule(Sagittarius s) {
		super(s);
		this.ID = "motd";
	}

	@Override
	public void OnResponseReceived(String ActionID, SagResponse resp) {
		// When a response is received from the remote service
	}
}
```

Save this file as `MOTDModule.java` in your project's source directory. Every module you create should have at least this basic skeleton. Although you do not need to have anything in the `OnResponseReceived()` function, you must override the constructor to specify a module ID. This ID will be used by Sagittarius to identify and retrieve instances of this module, and should be unique (otherwise, modules could be confused for each other).

## The Handler Pattern

Anything that relies on an Internet connection is **asynchronous**. That is, we cannot predict how long it will take for us to send data to our App Engine application, or when the server will reply. Because of this, we cannot simply wait for a response; we want to be **notified** when a response is received.

Sagittarius masks most of the complexity of such event handling for you, piping all notifications through the `OnResponseReceived()` function we've already declared. However, your project will be interacting with your modules directly, so we need another layer of event handlers within each module you make. Thankfully there is a very simple *handler pattern* to follow:

```java
import sagittarius.Handler;
import sagittarius.Module;
import sagittarius.Sagittarius;
import sagittarius.SagResponse;

public class MOTDModule extends Module {

	private Handler handler;

	public MOTDModule(Sagittarius s) {
		super(s);
		this.ID = "motd";
	}

	public void RegisterOnMOTDReceivedHandler(Handler h) {
		this.handler = h;
	}

	@Override
	public void OnResponseReceived(String ActionID, SagResponse resp) {
		handler.invoke();
	}
}
```

A class that wants to know when the Message of the Day has been received simply registers a handler through `RegisterOnMOTDReceivedHandler()`. When everything is done, `OnResponseReceived()` is called, and in turn the custom handler. `Handler.java` is a very simple abstract class that defines one method, `invoke()`, that can be overridden in an [anonymous inner class](http://docs.oracle.com/javase/tutorial/java/javaOO/innerclasses.html) to do what you want.

We'll see this pattern in action a little later on, but for now you should remember how to set it up:

- Declare a handler
- Make a function that registers an anonymous instance to this handler
- Call the handler when you want to notify that something has been done

## Caching the MOTD

Every time you communicate with your App Engine application, you use a tiny bit of its [quota](https://developers.google.com/appengine/docs/quotas). If you go over the quota your application will go down (equivalent to a crash), so it's important to communicate only when absolutely necessary.

In the case of the Message of the Day, we expect the message to change approximately once every 24 hours -- not very often, in other words. Although the MOTD may be updated while the player is playing, we will assume that this scenario is very unlikely. So, we can get away with only querying for the MOTD *once*: upon starting the game.

The typical way to handle data from Sagittarius is to maintain a **local cache** of it. When you ask Sagittarius for new information, the local cache is updated. Although we might get the MOTD value often (every time the player exits to the main menu, for example), we are really only getting its cached value. Let's code this now:

```java
import sagittarius.Handler;
import sagittarius.Module;
import sagittarius.Sagittarius;
import sagittarius.SagResponse;

public class MOTDModule extends Module {

	private String motd;

	private Handler handler;

	public MOTDModule(Sagittarius s) {
		super(s);
		this.ID = "motd";
	}

	public void RegisterOnMOTDReceivedHandler(Handler h) {
		this.handler = h;
	}

	public String GetMOTD() {
		return motd;
	}

	public void QueryMOTD() {
		// @TODO
	}

	@Override
	public void OnResponseReceived(String ActionID, SagResponse resp) {
		handler.invoke();
	}
}
```

We have added two new functions. You will call `GetMOTD()` whenever you want to know the MOTD. When you want to update the MOTD with the value on the server, you can call `QueryMOTD()`.

## Querying the MOTD

Since we only really want to *get* the latest MOTD from the server, our `QueryMOTD()` function will only need to implement a single action, appropriately called GetAction:

```java
import sagittarius.GetAction;
import sagittarius.Handler;
import sagittarius.Module;
import sagittarius.Sagittarius;
import sagittarius.SagResponse;

public class MOTDModule extends Module {

	private String motd;

	private Handler handler;

	public MOTDModule(Sagittarius s) {
		super(s);
		this.ID = "motd";
	}

	public void RegisterOnMOTDReceivedHandler(Handler h) {
		this.handler = h;
	}

	public String GetMOTD() {
		return motd;
	}

	public void QueryMOTD() {
		GetAction ga = (GetAction)parent.CreateAction("get");
		ga.AddFilter(GetAction.DBTYPE, "motd");
		ga.AddFilter(GetAction.DBNAME, "motd");
		ga.AddProjection("message", true);
		ga.Unique();
		SubmitAction("motdquery", ga);
	}

	@Override
	public void OnResponseReceived(String ActionID, SagResponse resp) {
		motd = resp.getDBValue("message");
		handler.invoke();
	}
}
```

Our added code shows how to make use of the actions bundled with the starter kit. First, we create a new instance of GetAction. Then we add our filters and projections to it. We only want to get the DBObject with `object_type=="motd"` and `object_name=="motd"`, so we add those filters using the special shortcut variables `DBTYPE` and `DBNAME` respectively. We only want to return the actual *message*, so we add a projection for that field. Since we expect there to be only one MOTD, we make the query unique. And finally, we submit the GetAction and assign it an ID of `"motdquery"` so that it can be identified later.

Any time that Sagittarius receives a reply from the server, the text will be routed to `OnResponseReceived()`. Therefore it is here that we want to parse the MOTD message and assign it to our local cache. Replies are encoded as a special SagResponse object, which provides a convenient `getDBValue()` function to return the first value matching the specified key. Once we do that, our module is complete.

## Using Our MOTD Module

Since this is a simple tutorial, we'll just create a class that prints the MOTD to the screen as soon as it is received. To demonstrate the asynchronous capabilities of Sagittarius, we will also print a bunch of "o" characters to the screen, one every 40 milliseconds:

```java
import sagittarius.Handler;
import sagittarius.Sagittarius;

public class SagittariusTest {

	public static final String APP_ID = [APP ID HERE];
	public static final String APP_PASS = [APP PASSWORD HERE];

	public static void GrabMOTD(Sagittarius sag) {
		System.out.println("OUR MOTD IS: " + ((MOTDModule) sag.GetModule("motd")).GetMOTD());
	}

	public static void main(String[] args) throws InterruptedException {
		final Sagittarius sag = new Sagittarius(APP_ID, APP_PASS);
		sag.RegisterModule(new MOTDModule(sag));

		MOTDModule m = (MOTDModule) sag.GetModule("motd");
		m.RegisterOnMOTDReceivedHandler(new Handler() {
			@Override
			public void invoke() {
				GrabMOTD(sag);
			}
		});
		m.QueryMOTD();

		for (int i = 0; i < 100; i++) {
			Thread.sleep(40);
			System.out.println("o");
		}
	}
}
```

The first thing we do is **register** an instance of our MOTDModule to Sagittarius, then **retrieve** our module instance. In a practical application these two actions would not happen one after the other, but they do here for demonstration purposes.

Notice the use of the anonymous inner Handler class: our `invoke()` function simply calls `GrabMOTD()`, which in turn prints the value of our module's cached MOTD to `System.out`. Since our handler is only called once our module has received a response from the server, we know there will be an updated value in the cache. Remember that this layer of indirection is necessary because web connections are asynchronous.

Running the test class should produce something like this:

```
[Sagittarius] DEBUG: Resolving: http://your-app-id-here.appspot.com
[Sagittarius] INFO: TCP connection opened for module motd and query motdquery
o
o
o
o
o
o
o
o
[Sagittarius] DEBUG: End TCP connection
[Sagittarius] DEBUG: Received Text: <message>Welcome to my game, have fun playing!</message>

[Sagittarius] INFO: TCP connection closed for module motd and query motdquery
OUR MOTD IS: Welcome to my game, have fun playing!
o
o
o
o
o
...
```

Notice how the o's continue to print even as Sagittarius is retrieving our MOTD. It took 8 o's, or about 320 milliseconds, for the round-trip to complete, but during that time the application was free to continue working.

Congratulations, you have just written your first module!

# Medium: Server Browser

Coming soon!

# Special Functions

## Sending Mail

You can send an email any time from within your application using the `SendMail()` function in `Sagittarius.java`:

```java
public void SendMail(String receiver, String subject, String message, String sender)
```

The sender parameter is a string referencing the subdomain of your application that you want the email to be sent from. For example, if your `Application Identifier` is "myapplication" and your sender parameter is set to "donuts", then the recipient will receive an email from **donuts@myapplication.appspotmail.com**. Note that if you pass in an empty string for the sender, it will default to "admin".

# Logging

Sagittarius has a built-in log system that supports conditional logging via an enum defined in `Sagittarius.java`:

```java
public enum ELogLevel {
	LOG_None, LOG_Error, LOG_Warn, LOG_Info, LOG_Debug;
}
```

You can set the logging level using the static function `Sagittarius.SetLogLevel()`. The levels are defined roughly as follows:

- **LOG_None**: Log nothing at all
- **LOG_Error**: Log only errors, which are unrecoverable faults that should be handled
- **LOG_Warn**: Warnings are recoverable errors; there is a problem but the game can continue running
- **LOG_Info**: General important information about connections is logged by default
- **LOG_Debug**: Log everything, including debug information (which is typically verbose)

To use the logging system, you can call the following functions defined in `Sagittarius.java`:

```java
public static void LogError(String msg, String cat)
public static void LogWarn(String msg, String cat)
public static void LogInfo(String msg, String cat)
public static void LogDebug(String msg, String cat)
```

There are also versions of all four functions without the second `cat` parameter. This parameter is a tag that will be enclosed in brackets preceding the message in the log. If you decide to specify it, you would typically use the name of the class that you are logging from. Remember that logging is filtered by the `logLevel`, so if your logging level is `LOG_Warn` but you call `LogInfo()`, that message will not be logged.

By default, Sagittarius outputs the log to `System.out`. You can change the PrintStream that Sagittarius logs to by using the static function `Sagittarius.SetLogStream()`:

```java
PrintStream myLog = new PrintStream(new FileOutputStream("MyAwesomeGame-Log.txt", true));
Sagittarius.SetLogStream(myLog);
```
