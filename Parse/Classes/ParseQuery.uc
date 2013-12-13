/**
 * Parse - UnrealScript SDK
 * Copyright 2014 WillyG Productions
 * @Authors: William Gaul
 */
class ParseQuery extends Object;

delegate CountDelegate(int count, ParseException e);
delegate FindDelegate(array<ParseObject> objs, ParseException e);
delegate GetDelegate(ParseObject obj, ParseException e);

function RegisterCountDelegate(delegate<CountDelegate> del)
{
     CountDelegate = del;
}

function RegisterFindDelegate(delegate<FindDelegate> del)
{
     FindDelegate = del;
}

function RegisterGetDelegate(delegate<GetDelegate> del)
{
     GetDelegate = del;
}



function ParseQuery AddAscendingOrder(string key)
{
     // Also sorts the results in ascending order by the given key
}

function ParseQuery AddDescendingOrder(string key)
{
     // Also sorts the results in descending order by the given key
}



function Cancel()
{
     // Cancels the current network request, if one is running
}

static function ClearAllCachedResults()
{
     // Clears the cached results for all queries
}

function ClearCachedResult()
{
     // Removes the previously cached result for this query, forcing the next Find() to hit the network
}

function void Count()
{
     // Counts the number of objects that match this query, if CountDelegate is set it will call that at the end
}

function void Find()
{
     // Retrieves a list of ParseObjects that satisfy this query from the server, if FindDelegate is set it will call that at the end
}

function void Get(string ObjectID)
{
     // Constructs a ParseObject whose ID is [ObjectID] by fetching data from the server, if GetDelegate is set it will call that at the end
}

function void GetFirst()
{
     // Retrieves at most one ParseObject that satisfies this query from the server, if GetDelegate is set it will call that at the end
}


function int GetLimit()
{
     // Accessor for the query limit
}

function int GetSkip()
{
     // Accessor for the query skip
}


function SetLimit(int newLimit)
{
     // Controls the maximum number of results returned
}

function SetSkip(int newSkip)
{
     // Controls the number of results to skip before returning any results
}



/* 


 
 void     setMaxCacheAge(long maxAgeInMilliseconds) 
          Sets the maximum age of cached data that will be considered in this query.
 
 void     setTrace(boolean shouldTrace) 
          Turn on performance tracing of finds.

 ParseQuery.CachePolicy  getCachePolicy() 
          Accessor for the caching policy.
 String   getClassName() 
          Accessor for the class name.


 
 long     getMaxCacheAge() 
          Gets the maximum age of cached data that will be considered in this query.
static
<T extends ParseObject> 
ParseQuery<T>
getQuery(Class<T> subclass) 
          Creates a new query for the given ParseObject subclass type.
static
<T extends ParseObject> 
ParseQuery<T>
getQuery(String className) 
          Creates a new query for the given class name.




static ParseQuery<ParseUser>  getUserQuery() 
          Deprecated. Please use ParseUser.getQuery() instead.




 boolean  hasCachedResult() 
          Returns whether or not this query has a cached result.
 void     include(String key) 
          Include nested ParseObjects for the provided key.
static
<T extends ParseObject> 
ParseQuery<T>
or(List<ParseQuery<T>> queries) 
          Constructs a query that is the or of the given queries.
 ParseQuery<T> orderByAscending(String key) 
          Sorts the results in ascending order by the given key.
 ParseQuery<T> orderByDescending(String key) 
          Sorts the results in descending order by the given key.
 void     selectKeys(Collection<String> keys) 
          Restrict the fields of returned ParseObjects to only include the provided keys.
 void     setCachePolicy(ParseQuery.CachePolicy newCachePolicy) 
          Change the caching policy of this query.



*/


function ParseQuery WhereContainedIn(string key, array<Object> values)
{
     // Add a constraint to the query that requires a particular key's value to be contained in the provided list of values
}

function ParseQuery WhereContains(string key, string substring)
{
     // Add a constraint for finding string values that contain a provided string
}

function WhereContainsAll(string key, array<Object> values)
{
     // Add a constraint to the query that requires a particular key's value match another ParseQuery
}

function ParseQuery WhereDoesNotExist(string key)
{
     // Add a constraint for finding objects that do not contain a given key
}

function ParseQuery WhereDoesNotMatchKeyInQuery(string key, string keyInQuery, ParseQuery query)
{
     // Add a constraint to the query that requires a particular key's value does not match any value for a key in the results of another ParseQuery
}

function ParseQuery WhereDoesNotMatchQuery(string key, ParseQuery query)
{
     // Add a constraint to the query that requires a particular key's value does not match another ParseQuery
}

function ParseQuery WhereEndsWith(string key, string suffix)
{
     // Add a constraint for finding string values that end with a provided string
}

function ParseQuery WhereEqualTo(string key, Object value)
{
     // Add a constraint to the query that requires a particular key's value to be equal to the provided value
}

function ParseQuery WhereExists(string key)
{
     // Add a constraint for finding objects that contain the given key
}

function ParseQuery WhereGreaterThan(string key, Object value)
{
     // Add a constraint to the query that requires a particular key's value to be greater than the provided value
}




/*




 ParseQuery<T> whereGreaterThanOrEqualTo(String key, Object value) 
          Add a constraint to the query that requires a particular key's value to be greater than or equal to the provided value.
 ParseQuery<T> whereLessThan(String key, Object value) 
          Add a constraint to the query that requires a particular key's value to be less than the provided value.
 ParseQuery<T> whereLessThanOrEqualTo(String key, Object value) 
          Add a constraint to the query that requires a particular key's value to be less than or equal to the provided value.
 ParseQuery<T> whereMatches(String key, String regex) 
          Add a regular expression constraint for finding string values that match the provided regular expression.
 ParseQuery<T> whereMatches(String key, String regex, String modifiers) 
          Add a regular expression constraint for finding string values that match the provided regular expression.
 ParseQuery<T> whereMatchesKeyInQuery(String key, String keyInQuery, ParseQuery<?> query) 
          Add a constraint to the query that requires a particular key's value matches a value for a key in the results of another ParseQuery
 ParseQuery<T> whereMatchesQuery(String key, ParseQuery<?> query) 
          Add a constraint to the query that requires a particular key's value match another ParseQuery.
 ParseQuery<T> whereNear(String key, ParseGeoPoint point) 
          Add a proximity based constraint for finding objects with key point values near the point given.
 ParseQuery<T> whereNotContainedIn(String key, Collection<? extends Object> values) 
          Add a constraint to the query that requires a particular key's value not be contained in the provided list of values.
 ParseQuery<T> whereNotEqualTo(String key, Object value) 
          Add a constraint to the query that requires a particular key's value to be not equal to the provided value.
 ParseQuery<T> whereStartsWith(String key, String prefix) 
          Add a constraint for finding string values that start with a provided string.
 ParseQuery<T> whereWithinGeoBox(String key, ParseGeoPoint southwest, ParseGeoPoint northeast) 
          Add a constraint to the query that requires a particular key's coordinates be contained within a given rectangular geographic bounding box.
 ParseQuery<T> whereWithinKilometers(String key, ParseGeoPoint point, double maxDistance) 
          Add a proximity based constraint for finding objects with key point values near the point given and within the maximum distance given.
 ParseQuery<T> whereWithinMiles(String key, ParseGeoPoint point, double maxDistance) 
          Add a proximity based constraint for finding objects with key point values near the point given and within the maximum distance given.
 ParseQuery<T> whereWithinRadians(String key, ParseGeoPoint point, double maxDistance) 
          Add a proximity based constraint for finding objects with key point values near the point given and within the maximum distance given.*/