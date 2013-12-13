/**
 * Parse - UnrealScript SDK
 * Copyright 2014 WillyG Productions
 * @Authors: William Gaul
 */

/**
 * The ParseObject is a local representation of data that can be saved and retrieved from the Parse cloud.
 * To write data, you'd usually construct a new ParseObject, use Put() to fill it, and then use Save() to persist it.function
 * To read data, you'd usually use a ParseQuery.
 */
class ParseObject extends Object;

var private JsonObject response;
var bool bWasSuccessful;
var string ErrorMsg;
var Sagittarius Parent;


/** DELEGATES **/

delegate DeleteDelegate(ParseException e);
delegate RefreshDelegate(ParseObject obj, ParseException e);
delegate SaveDelegate(ParseException e);

function RegisterDeleteDelegate(delegate<DeleteDelegate> del)
{
	DeleteDelegate = del;
}

function RegisterRefreshDelegate(delegate<RefreshDelegate> del)
{
	RefreshDelegate = del;
}

function RegisterSaveDelegate(delegate<SaveDelegate> del)
{
	SaveDelegate = del;
}





function Add(string key, Object value)
{
	// Atomically adds [value] to the end of the array associated with [key]
}

function AddAll(string key, array<Object> values)
{
	// Same as Add(), except for all objects in [values]
}

function AddUnique(string key, Object value)
{
	// Same as Add(), except only adds objects not already in the array
}

function AddAllUnique(string key, array<Object> values)
{
	// Same as AddAll(), except only adds objects not already in the array
}


function bool ContainsKey(string key)
{
	// Returns whether this object has [key]
}


function Delete()
{
	// Deletes this object on the server, if DeleteDelegate is set it will call that at the end
}

static function DeleteAll(array<ParseObject> objects)
{
	// Same as Delete(), except for all ParseObjects in [objects]
}

function DeleteEventually()
{
	// Same as Delete(), except this works even if Parse is currently inaccessible
}


function Object Get(string key)
{
	// Access the value associated with [key]
}

function int GetInt(string key)
{
	//
}

function string GetString(string key)
{
	//
}


function Increment(string key)
{
	// Atomically increments the value associated with [key] by 1
}

function Increment(string key, int amount)
{
	// Atomically increments the value associated with [key] by [amount]
}


function Put(string key, Object value)
{
	// Adds the [key]-[value] pair to this object
}

function Refresh()
{
	// Refreshes this object with data from the server, if RefreshDelegate is set it will call that at the end
}


function Remove(string key)
{
	// Removes [key] from this object if it exists
}

function RemoveAll(string key, array<Object> values)
{
	// Atomically removes all instances of objects in [values] from the array associated with [key]
}


function Save()
{
	// Saves this object to the server, if SaveDelegate is set it will call that at the end
}

static function SaveAll(array<ParseObject> objects)
{
	// Same as Save(), except for all ParseObjects in [objects]
}

function SaveEventually()
{
	// Same as Save(), except this works even if Parse is currently inaccessible
}




function ParseACL GetACL()
{
	// Returns the ParseACL governing this object
}





/* 
 
 boolean	getBoolean(String key) 
          Access a boolean value.
 byte[]	getBytes(String key) 
          Access a byte array value.
 String	getClassName() 
          Accessor to the class name.
 Date	getCreatedAt() 
          This reports time as the server sees it, so that if you create a ParseObject, then wait a while, and then call save(), the creation time will be the time of the first save() call rather than the time the object was created locally.
 Date	getDate(String key) 
          Access a Date value.
 double	getDouble(String key) 
          Access a double value.

 JSONArray	getJSONArray(String key) 
          Access a JSONArray value.
 JSONObject	getJSONObject(String key) 
          Access a JSONObject value.
<T> List<T>
getList(String key) 
          Access a List value.
 long	getLong(String key) 
          Access a long value.
<V> Map<String,V>
getMap(String key) 
          Access a Map value
 Number	getNumber(String key) 
          Access a numerical value.
 String	getObjectId() 
          Accessor to the object id.
 ParseFile	getParseFile(String key) 
          Access a ParseFile value.
 ParseGeoPoint	getParseGeoPoint(String key) 
          Access a ParseGeoPoint value.
 ParseObject	getParseObject(String key) 
          Access a ParseObject value.
 ParseUser	getParseUser(String key) 
          Access a ParseUser value.
<T extends ParseObject> 
ParseRelation<T>
getRelation(String key) 
          Access or create a Relation value for a key

 Date	getUpdatedAt() 
          This reports time as the server sees it, so that if you make changes to a ParseObject, then wait a while, and then call save(), the updated time will be the time of the save() call rather than the time the object was changed locally.
*/


/*



static
<T extends ParseObject> 
T
create(Class<T> subclass) 
          Creates a new ParseObject based upon a subclass type.
static ParseObject	create(String className) 
          Creates a new ParseObject based upon a class name.
static
<T extends ParseObject> 
T
createWithoutData(Class<T> subclass, String objectId) 
          Creates a reference to an existing ParseObject for use in creating associations between ParseObjects.
static ParseObject	createWithoutData(String className, String objectId) 
          Creates a reference to an existing ParseObject for use in creating associations between ParseObjects.

<T extends ParseObject> 
T
fetch() 
          Fetches this object with the data from the server.
static List<ParseObject>	fetchAll(List<ParseObject> objects) 
          Fetches all the objects in the provided list.
static
<T extends ParseObject> 
List<T>
fetchAllIfNeeded(List<T> objects) 
          Fetches all the objects that don't have data in the provided list.
static
<T extends ParseObject> 
void
fetchAllIfNeededInBackground(List<T> objects, FindCallback<T> callback) 
          Fetches all the objects that don't have data in the provided list in the background
static
<T extends ParseObject> 
void
fetchAllInBackground(List<T> objects, FindCallback<T> callback) 
          Fetches all the objects in the provided list in the background
<T extends ParseObject> 
T
fetchIfNeeded() 
          If this ParseObject has not been fetched (i.e.
<T extends ParseObject> 
void
fetchIfNeededInBackground(GetCallback<T> callback) 
          If this ParseObject has not been fetched (i.e.
<T extends ParseObject> 
void
fetchInBackground(GetCallback<T> callback) 
          Fetches this object with the data from the server in a background thread.




 boolean	has(String key) 
          Whether this object has a particular key.
 boolean	hasSameId(ParseObject other) 
           

 boolean	isDataAvailable() 
          Gets whether the ParseObject has been fetched.
 boolean	isDirty() 
          Whether any key-value pair in this object (or its children) has been added/updated/removed and not saved yet.
 boolean	isDirty(String key) 
          Whether a value associated with a key has been added/updated/removed and not saved yet.
 Set<String>	keySet() 
          Returns a set view of the keys contained in this object.

static void	registerSubclass(Class<? extends ParseObject> subclass) 
          Registers a custom subclass type with the Parse SDK, enabling strong-typing of those ParseObjects whenever they appear.


 void	setACL(ParseACL acl) 
          Set the ParseACL governing this object.
 void	setObjectId(String newObjectId) 
          Setter for the object id.*/