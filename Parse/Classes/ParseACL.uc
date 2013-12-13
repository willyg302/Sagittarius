/**
 * Parse - UnrealScript SDK
 * Copyright 2014 WillyG Productions
 * @Authors: William Gaul
 */

/**
 * A ParseACL is used to control which users can access or modify a particular object.
 * Each ParseObject can have its own ParseACL.
 * You can grant read and write permissions separately to specific users, to groups of users that belong to roles,
 * or you can grant permissions to "the public" so that, for example, any user could read a particular object but
 * only a particular set of users could write to that object.
 *
 * By default, an ACL has no permissions granted.
 */
class ParseACL extends Object;

function Initialize(ParseUser owner)
{
	// Set this ACL to only allowed [owner] access
}


function bool GetPublicReadAccess()
{
	// Whether the public is allowed to read this object
}

function bool GetPublicWriteAccess()
{
	// Whether the public is allowed to write to this object
}

function bool GetReadAccess(ParseUser user)
{
	// Whether [user] is *explicitly* allowed to read this object
}

function bool GetReadAccess(String userID)
{
	// Whether user with [userID] is *explicitly* allowed to read this object
}



function bool GetWriteAccess(ParseUser user)
{
	// Whether [user] is *explicitly* allowed to write to this object
}

function bool GetWriteAccess(String userID)
{
	// Whether user with [userID] is *explicitly* allowed to write to this object
}


function SetPublicReadAccess(bool allowed)
{
	// Set whether the public is allowed to read this object
}

function SetPublicWriteAccess(bool allowed)
{
	// Set whether the public is allowed to write to this object
}


function SetReadAccess(ParseUser user, bool allowed)
{
	// Set whether [user] is allowed to read this object
}

function SetReadAccess(string userID, bool allowed)
{
	// Set whether user with [userID] is allowed to read this object
}


function SetWriteAccess(ParseUser user, bool allowed)
{
	// Set whether [user] is allowed to write to this object
}

function SetWriteAccess(string userID, bool allowed)
{
	// Set whether user with [userID] is allowed to write to this object
}


/*


 
 boolean	getRoleReadAccess(ParseRole role) 
          Get whether users belonging to the given role are allowed to read this object.
 boolean	getRoleReadAccess(String roleName) 
          Get whether users belonging to the role with the given roleName are allowed to read this object.
 boolean	getRoleWriteAccess(ParseRole role) 
          Get whether users belonging to the given role are allowed to write this object.
 boolean	getRoleWriteAccess(String roleName) 
          Get whether users belonging to the role with the given roleName are allowed to write this object.





 
static void	setDefaultACL(ParseACL acl, boolean withAccessForCurrentUser) 
          Sets a default ACL that will be applied to all ParseObjects when they are created.



 void	setRoleReadAccess(ParseRole role, boolean allowed) 
          Set whether users belonging to the given role are allowed to read this object.
 void	setRoleReadAccess(String roleName, boolean allowed) 
          Set whether users belonging to the role with the given roleName are allowed to read this object.
 void	setRoleWriteAccess(ParseRole role, boolean allowed) 
          Set whether users belonging to the given role are allowed to write this object.
 void	setRoleWriteAccess(String roleName, boolean allowed) 
          Set whether users belonging to the role with the given roleName are allowed to write this object.

*/