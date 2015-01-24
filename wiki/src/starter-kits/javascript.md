---
title: JavaScript
subtitle: The tutorial hub for the JavaScript starter kit
template: tutorial.jade
---

# Basic Integration

Copy `sagittarius.js` into a convenient place in your project's tree, for example the `js/` directory if you have one.

Once you have added the file to your project, creating an instance of Sagittarius is very simple:

```html
<!DOCTYPE html>
<html>
	<head>
		<script src="js/sagittarius.js"></script>
	</head>
	<body>
		<script>
			var sag = new Sagittarius("[APP ID HERE]", "[APP PASSWORD HERE]");
		</script>
	</body>
</html>
```

Make sure to replace `[APP ID HERE]` and `[APP PASSWORD HERE]`with your own application ID and password. At this point Sagittarius will be fully integrated and ready to use, but it can't really do anything just yet. To start leveraging its power you will need to write some *modules*.

# Easy: MOTD Module

## Understanding Modules

Sagittarius is structured around the idea of <span class="label label-danger">MODULES</span> that perform <span class="label label-danger">ACTIONS</span>. The actions that Sagittarius is capable of performing are fixed; that is, you will never have to write an "action" function to do something. You *will*, however, have to create modules that use the actions available to Sagittarius.

Fortunately for us, JavaScript makes it very easy to write and add new modules (and therefore new functionality) to Sagittarius. Another great thing is that you can write as many modules as you'd like: a Server Module, a Login Module, and so on -- one for each of the features you'd like your game to support.

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

## Defining Our Module

What makes JavaScript so great when it comes to writing modules is that it supports code modularity *and* asynchronous functions out of the box. To see these features in action, create a new file -- let's call it `motdmodule.js` -- and add the following code:

```js
var motd;

Sagittarius.prototype.GetMOTD = function () {
	return motd;
};

Sagittarius.prototype.QueryMOTD = function (callback) {
	var ga = this.CreateAction('get'), pass = this.pass;
	this.SubmitAction(
		ga.AddFilter(ga.DBTYPE, 'motd')
			.AddFilter(ga.DBNAME, 'motd')
			.AddProjection('message', true)
			.Unique(),
		function (data) {
			motd = Encryption.Decrypt(data.dbobjects[0].message, pass);
			callback();
		}
	);
};
```

Whoa, that was a lot of code all at once! Let's break it down line-by-line.

### Caching the MOTD

The first line, `var motd;`, defines a **local cache** for our MOTD. The reason for this is that every time you communicate with your App Engine application, you use a tiny bit of its [quota](https://developers.google.com/appengine/docs/quotas). If you go over the quota your application will go down (equivalent to a crash), so it's important to communicate only when absolutely necessary.

In the case of the Message of the Day, we expect the message to change approximately once every 24 hours -- not very often, in other words. Although the MOTD may be updated while the player is playing, we will assume that this scenario is very unlikely. So, we can get away with only querying for the MOTD *once*: upon starting the game.

The typical way to handle data from Sagittarius is to maintain such a cache. When you ask Sagittarius for new information, the local cache is updated. Although we might get the MOTD value often (every time the player exits to the main menu, for example), we are really only getting its cached value.

### Adding New Functionality

As you might expect, the function `GetMOTD()` handles returning the value currently in the cache. In particular, this function shows how to add new functionality to Sagittarius through its **prototype**.

Suppose you wanted to add a function called `MyFunction()` to Sagittarius that you could call as long as you had a Sagittarius instance. All you'd have to do is write something like this:

```js
Sagittarius.prototype.MyFunction = function () {
	// Insert the awesomeness here!
};
```

And to call it, all you'd need to do is:

```js
mySagittariusInstance.MyFunction();
```

Pretty easy, right? Admittedly, this probably isn't the best way to handle modules in JavaScript because of security reasons. If you know a more robust way I'd love to hear about it!

### Querying the MOTD

Our `QueryMOTD()` function handles actually communicating with the server, and showcases the concept of using actions. The most important thing to understand is that while writing functions defined within the `Sagittarius.prototype` scope, any reference to a Sagittarius function must be preceded by `this.`. Also of note is the `callback` parameter, which is a function that users of this module can pass to `QueryMOTD()`. Once the querying is complete, this function will be called.

Sagittarius has a special function called `CreateAction()` that makes it easy to construct an action "object". Here, we want a GetAction, so we call `this.CreateAction('get')`. We could have also called the function with the strings 'add', 'mod', or 'del' to make an Add, Modify, or Delete action, respectively.

Once we have our action, we can add our filters and projections to it. We only want to get the DBObject with `object_type=="motd"` and `object_name=="motd"`, so we add those filters using the special shortcut variables `DBTYPE` and `DBNAME` respectively. We only want to return the actual *message*, so we add a projection for that field. Since we expect there to be only one MOTD, we make the query unique. Because all actions in Sagittarius support chaining, we were able to do this all in one line.

The last step is to submit the action to Sagittarius, which we can do with the function `SubmitAction()`. The second parameter is function that will be called once a response from the server has been received. In our case, we want to set the new value of the `motd` variable and call our *own* callback function.

## Using Our MOTD Module

Since this is a simple tutorial, we'll just create a webpage that prints the MOTD to the screen as soon as it is received:

```html
<!DOCTYPE html>
<html>
	<head>
		<script src="js/sagittarius.js"></script>
		<script src="js/motdmodule.js"></script>
	</head>
	<body>
		<script>
			var sag = new Sagittarius("[APP ID HERE]", "[APP PASSWORD HERE]");
			sag.QueryMOTD(function () {
				document.write(sag.GetMOTD());
			});
		</script>
	</body>
</html>
```

Just remember that you must include `sagittarius.js` *before* any of its modules.

Because of our callback parameter in `QueryMOTD()`, handling an asynchronous call to Sagittarius is very trivial. All we do is pass an anonymous function that writes the value of the local MOTD cache to the HTML document as soon as it is available. To test your module out, just open the page in your favorite browser. You should see the Message of the Day appear on the screen after a few seconds.

Congratulations, you have just written your first module!

# Medium: Server Browser

Coming soon!

# Special Functions

## Sending Mail

You can send an email any time from within your application using the `SendMail()` function:

```js
mySagittariusInstance.SendMail({
	receiver: 'john.doe@gmail.com',
	subject: 'Hello world!',
	message: 'This email was sent from Sagittarius.\n\nHave a nice day!',
	sender: 'sender',
	callback: function (data) {
		document.write("Mail successfully sent!");
	}
});
```

The sender parameter is a string referencing the subdomain of your application that you want the email to be sent from. For example, if your `Application Identifier` is "myapplication" and your sender parameter is set to "donuts", then the recipient will receive an email from **donuts@myapplication.appspotmail.com**. Note that if you pass in an empty string for the sender, it will default to "admin".

# Logging

Coming soon!
