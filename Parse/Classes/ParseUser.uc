/**
 * Parse - UnrealScript SDK
 * Copyright 2014 WillyG Productions
 * @Authors: William Gaul
 */
class ParseUser extends ParseObject;

delegate RequestPasswordResetDelegate(ParseException e);
delegate SignUpDelegate(ParseException e);

function RegisterRequestPasswordResetDelegate(delegate<RequestPasswordResetDelegate> del)
{
	RequestPasswordResetDelegate = del;
}

function RegisterSignUpDelegate(delegate<SignUpDelegate> del)
{
	SignUpDelegate = del;
}


static function RequestPasswordReset(string email)
{
	// Requests a password reset email to be sent to the specified email address associated with the user account
	// If RequestPasswordResetDelegate is set, it will be called
}



function SetEmail(string email)
{
	//
}

function SetPassword(string password)
{
	//
}

function SetUsername(string username)
{
	//
}





/**
 * Signs up a new user. If SignUpDelegate is set, it will be called once this is done.function
 * This should be called instead of ParseObject.save(), as it will also persist the session in memory so that
 * the user can be accessed via GetCurrentUser().
 *
 * Fails if: server is inaccessible, or username has already been taken
 */
function SignUp()
{
	//
}



/*static ParseUser	become(String sessionToken) 
          Authorize a user with a session token.
static void	becomeInBackground(String sessionToken, LogInCallback callback) 
          Authorize a user with a session token.
static void	enableAutomaticUser() 
          Enables automatic creation of anonymous users.
 ParseUser	fetch() 
          Fetches this object with the data from the server.
 ParseUser	fetchIfNeeded() 
          If this ParseObject has not been fetched (i.e.
static ParseUser	getCurrentUser() 
          This retrieves the currently logged in ParseUser with a valid session, either from memory or disk if necessary.
 String	getEmail() 
          Retrieves the email address.
static ParseQuery<ParseUser>	getQuery() 
          Constructs a query for ParseUsers.
 String	getSessionToken() 
          Retrieves the session token for a user, if they are logged in.
 String	getUsername() 
          Retrieves the username.
 boolean	isAuthenticated() 
          Whether the ParseUser has been authenticated on this device.
 boolean	isNew() 
          Indicates whether this ParseUser was created during this session through a call to ParseUser.signUp() or by logging in with a linked service such as Facebook.
static ParseUser	logIn(String username, String password) 
          Logs in a user with a username and password.
static void	logInInBackground(String username, String password, LogInCallback callback) 
          Logs in a user with a username and password.
static void	logOut() 
          Logs out the currently logged in user session.
 void	put(String key, Object value) 
          Add a key-value pair to this object.
 void	remove(String key) 
          Removes a key from this object's data if it exists.


*/