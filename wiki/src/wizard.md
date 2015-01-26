---
title: Sagittarius Wizard
subtitle: Learn how to use the wizard to manage your application
template: tutorial.jade
---

# Running the Wizard

<div class="alert alert-block">
	<h4>Warning!</h4>
	Currently the Sagittarius Wizard is available only in Python source form, not as an executable or application. To run it you will need either the <a href="http://www.pythonware.com/products/pil/">Python Imaging Library</a> (PIL) or its 64-bit alternative <a href="http://www.lfd.uci.edu/~gohlke/pythonlibs/#pillow">Pillow</a>.
</div>

Navigate to the `Sagittarius-Wizard/` directory of your Sagittarius distribution and run the command `python SagittariusWizard.py` in your favorite command line.

# Recipes

## What Are Recipes?

Using the wizard revolves around the idea of <span class="label label-danger">RECIPES</span>. A recipe is a collection of buttons (you can think of them as "ingredients"), each with certain attributes, that does something when submitted to your application. The following buttons are available:
					
<div class="media">
	<img class="media-object pull-left" src="../img/wizard/filter.png" width="70">
	<div class="media-body">
		<h4 class="media-heading">Add Filter <span class="label label-default">GET</span> <span class="label label-default">MODIFY</span> <span class="label label-default">DELETE</span></h4>
		Filters restrict which objects to return based on equality. For example, an <code>object_type=="motd"</code> filter would only return objects whose type is "motd".
	</div>
</div>
<div class="media">
	<img class="media-object pull-left" src="../img/wizard/project.png" width="70">
	<div class="media-body">
		<h4 class="media-heading">Add Projection <span class="label label-default">GET</span> <span class="label label-default">MODIFY</span> <span class="label label-default">DELETE</span></h4>
		Projections tell the database to return only the attributes of the object that are specified. If no projections are specified, the entire object is returned (at higher cost).
	</div>
</div>
<div class="media">
	<img class="media-object pull-left" src="../img/wizard/attribute.png" width="70">
	<div class="media-body">
		<h4 class="media-heading">Add Attribute <span class="label label-default">ADD</span></h4>
		Specifies the value of an attribute for the object to be added to the database.
	</div>
</div>
<div class="media">
	<img class="media-object pull-left" src="../img/wizard/modification.png" width="70">
	<div class="media-body">
		<h4 class="media-heading">Modify Attribute <span class="label label-default">MODIFY</span></h4>
		Specifies the new value of an attribute to be modified. If more than one object is being modified, all objects will take on this new value.
	</div>
</div>
<div class="media">
	<img class="media-object pull-left" src="../img/wizard/limit.png" width="70">
	<div class="media-body">
		<h4 class="media-heading">Set Limit <span class="label label-default">GET</span> <span class="label label-default">MODIFY</span> <span class="label label-default">DELETE</span></h4>
		Sets the maximum number of objects to operate on. If more objects exist that satisfy your query, they will be ignored.
	</div>
</div>
<div class="media">
	<img class="media-object pull-left" src="../img/wizard/offset.png" width="70">
	<div class="media-body">
		<h4 class="media-heading">Set Offset <span class="label label-default">GET</span> <span class="label label-default">MODIFY</span> <span class="label label-default">DELETE</span></h4>
		Sets the offset in the database to return results. This allows for pagination across multiple queries: query 1 can get objects 0-19, query 2 can get objects 20-39, and so on.
	</div>
</div>
<div class="media">
	<img class="media-object pull-left" src="../img/wizard/returns.png" width="70">
	<div class="media-body">
		<h4 class="media-heading">Returns Results <span class="label label-default">MODIFY</span> <span class="label label-default">DELETE</span></h4>
		By default, the MODIFY and DELETE actions do not return objects. This button tells the actions to return results, optionally with projections and limits as in a GET action.
	</div>
</div>
<div class="media">
	<img class="media-object pull-left" src="../img/wizard/generic.png" width="70">
	<div class="media-body">
		<h4 class="media-heading">Generic Parameter <span class="label label-default">LEADERBOARDS</span> <span class="label label-default">SEND MAIL</span></h4>
		Represents a generic URL parameter, and is used for more low-level interactions with the Sagittarius API. For example, a generic parameter with field "f" and value "v" will be encoded as <code>&amp;f=v</code>.
	</div>
</div>

In addition, there is a special **action button** automatically added to each recipe. To select the action you want your recipe to carry out, simply left-click the action button (it should be the first button in the **Recipe** row) and select the action from the drop-down list. The following actions are available:

<div class="media">
	<img class="media-object pull-left" src="../img/wizard/dbget.png" width="70">
	<div class="media-body">
		<h4 class="media-heading">Get Action</h4>
		Get objects or parts of objects from the database. Which objects are returned, and how many to return, are based on the filters and limits you apply to this action.
	</div>
</div>
<div class="media">
	<img class="media-object pull-left" src="../img/wizard/dbadd.png" width="70">
	<div class="media-body">
		<h4 class="media-heading">Add Action</h4>
		Add an object with the specified attributes to the database.
	</div>
</div>
<div class="media">
	<img class="media-object pull-left" src="../img/wizard/dbmod.png" width="70">
	<div class="media-body">
		<h4 class="media-heading">Modify Action</h4>
		Modify certain attributes of objects from the database, optionally returning the modified objects. The objects to modify are determined by applied filters and limits.
	</div>
</div>
<div class="media">
	<img class="media-object pull-left" src="../img/wizard/dbdel.png" width="70">
	<div class="media-body">
		<h4 class="media-heading">Delete Action</h4>
		Delete all objects that satisfy the applied filters and limits from the database, optionally returning them.
	</div>
</div>
<div class="media">
	<img class="media-object pull-left" src="../img/wizard/ldbds.png" width="70">
	<div class="media-body">
		<h4 class="media-heading">Leaderboards Action</h4>
		Interact with the leaderboards system built into Sagittarius. Offers full support for adding/purging/removing leaderboards, posting to an existing leaderboard, and getting leaderboard data.
	</div>
</div>
<div class="media">
	<img class="media-object pull-left" src="../img/wizard/mail.png" width="70">
	<div class="media-body">
		<h4 class="media-heading">Send Mail Action</h4>
		Send an email to the provided address through Sagittarius.
	</div>
</div>

## An Example Recipe

Consider the recipe below:

<div>
	<div style="float:left; margin-right:10px; margin-bottom:10px;"><img class="media-object" src="../img/wizard/dbget.png" width="70"></div>
	<div style="float:left; margin-right:10px; margin-bottom:10px;"><img class="media-object" src="../img/wizard/filter.png" width="70"></div>
	<div style="float:left; margin-right:10px; margin-bottom:10px;"><img class="media-object" src="../img/wizard/filter.png" width="70"></div>
	<div style="float:left; margin-right:10px; margin-bottom:10px;"><img class="media-object" src="../img/wizard/project.png" width="70"></div>
	<div style="float:left; margin-right:10px; margin-bottom:10px;"><img class="media-object" src="../img/wizard/limit.png" width="70"></div>
	<div style="clear:both;"></div>
</div>

This is a simple recipe that queries for the current Message of the Day. The first button tells Sagittarius that it wants to GET data. The two filters make sure that all returned objects have `object_type==motd` and `object_name==motd`. Since we only want the actual message, we add a projection on the `message` attribute of our MOTD object. Finally, we only want one MOTD returned, so we set a limit of 1.

## Adding and Deleting Buttons

Add a button to your recipe by clicking on it in the **Available Buttons** row. Not all buttons in the row will be clickable; whether or not you can add a button depends on the action you have selected. Once you have added a button, you can click on it in the **Recipe** row to modify its attributes. Doing so will bring up a dialogue of available options for that button type.

If you want to delete a button from your recipe, just right-click it. For a quick way to clear an entire recipe, go to **File &rarr; Clear Recipe** or press **Ctrl+N**. Note that you can never delete the action button.

## Managing Recipes

The best part about recipes is that you can save and load them at any time. To save a new recipe, go to **File &rarr; Save Recipe As...** or press **Alt+S** and enter the name you would like to give the recipe. You can also use the quicker **File &rarr; Save Recipe** or **Ctrl+S** (if the recipe has not already been saved, you will be prompted to name it).

You can load a recipe by going to **File &rarr; Load Recipe** or pressing **Ctrl+O**. Choose the recipe you want to load from the dropdown list and press **Load** to load it.

A saved recipe can be deleted by going to **File &rarr; Delete Recipe** (for safety reasons there is no shortcut command). This will NOT clear the recipe from the **Recipe** row, but it *will* remove it from the save file. Similarly, if you clear a loaded recipe you can still save it to file; the saved recipe will be empty.

<div class="alert alert-block alert-info">
	<h4>A Note on Saving</h4>
	The save file for the Sagittarius Wizard is a file called <code>recipes.dat</code> in the same directory as <code>SagittariusWizard.py</code>. Avoid modifying this file. Also, this file is not written to until the wizard is <i>closed</i>, meaning that if the wizard should crash or be process-interrupted, you will lose any changes you have made in the current session.
</div>

# Global Options

Before submitting a recipe, you must fill out the App ID and Password fields in the **Global Options** row. These values are the same as the values of `[APP ID HERE]` and `[APP PASSWORD HERE]` from your application's `app.yaml` file. For more information, see [here](http://localhost:8080/getting-started/#modifying-app-yaml).

For convenience, these fields are saved every time you exit and will have their previous values the next time you run the wizard.

# Understanding the Output

Coming soon!
