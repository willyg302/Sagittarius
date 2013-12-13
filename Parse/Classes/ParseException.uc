/**
 * Parse - UnrealScript SDK
 * Copyright 2014 WillyG Productions
 * @Authors: William Gaul
 */
class ParseException extends Object;

var int code;
var string message;

function Create(int theCode, string theMessage)
{
    self.code = theCode;
    self.message = theMessage;
}

function int GetCode()
{
    return code;
}

function string GetMessage()
{
	return message;
}


var const int OTHER_CAUSE = -1;                     // Some error other than those enumerated here
var const int INTERNAL_SERVER_ERROR = 1             // Something has gone wrong with the server (it is Parse's fault)

var const int CONNECTION_FAILED = 100               // Connection to Parse servers has failed
var const int OBJECT_NOT_FOUND = 101                // Specified object does not exist
var const int INVALID_QUERY = 102                   // You tried to query with a datatype that doesn't support it (e.g. exact matching an array)
var const int INVALID_CLASS_NAME = 103              // Missing or invalid class name (case-sensitive, must start with a letter, and a-zA-Z0-9_ are only valid characters)
var const int MISSING_OBJECT_ID = 104               // Unspecified object ID
var const int INVALID_KEY_NAME = 105                // Invalid key name (case-sensitive, must start with a letter, and a-zA-Z0-9_ are only valid characters)
var const int INVALID_POINTER = 106                 // Malformed pointer -- you should never see this
var const int INVALID_JSON = 107                    // Malformed JSON received upstream: either you have encoded something unusual, or the network is failing
var const int COMMAND_UNAVAILABLE = 108             // The feature you tried to access is only available internally or for testing
var const int NOT_INITIALIZED = 109                 // You must call Parse.Initialize() before using Parse
var const int INCORRECT_TYPE = 111                  // A field was set to an inconsistent type
var const int INVALID_CHANNEL_NAME = 112            // Invalid channel name (empty string -- broadcast channel, must start with a letter, and a-zA-Z0-9_ are only valid characters)
var const int PUSH_MISCONFIGURED = 115
var const int OBJECT_TOO_LARGE = 116
var const int OPERATION_FORBIDDEN = 119             // Operation is not allowed for clients
var const int CACHE_MISS = 120                      // Result was not found in the cache
var const int INVALID_NESTED_KEY = 121              // An invalid key was used in a nested JSONObject
var const int INVALID_FILE_NAME = 122               // An invalid filename was used for ParseFile (contains only a-zA-Z0-9_. characters and is between 1-128 characters long)
var const int INVALID_ACL = 123
var const int TIMEOUT = 124                         // Request timed out on the server, typically because it was too expensive to run
var const int INVALID_EMAIL_ADDRESS = 125
var const int MISSING_CONTENT_TYPE = 126
var const int MISSING_CONTENT_LENGTH = 127
var const int INVALID_CONTENT_LENGTH = 128
var const int FILE_TOO_LARGE = 129
var const int FILE_SAVE_ERROR = 130
var const int FILE_DELETE_ERROR = 153
var const int DUPLICATE_VALUE = 137                 // A unique field was given a value that is already taken
var const int INVALID_ROLE_NAME = 139
var const int EXCEEDED_QUOTA = 140                  // Application quota was exceeded -- upgrade to resolve
var const int SCRIPT_FAILED = 141                   // A Cloud Code script failed
var const int VALIDATION_ERROR = 142                // A Cloud Code validation failed
var const int INVALID_IMAGE_DATA = 150
var const int UNSAVED_FILE_ERROR = 151
var const int INVALID_PUSH_TIME_ERROR = 152

var const int USERNAME_MISSING = 200                // Username is missing or empty
var const int PASSWORD_MISSING = 201                // Password is missing or empty
var const int USERNAME_TAKEN = 202
var const int EMAIL_TAKEN = 203
var const int EMAIL_MISSING = 204                   // Email is missing, but must be specified
var const int EMAIL_NOT_FOUND = 205                 // User with the specified email was not found
var const int SESSION_MISSING = 206                 // User object without a valid session could not be altered
var const int MUST_CREATE_USER_THROUGH_SIGNUP = 207 // You shouldn't be directly creating a ParseUser as if it were a ParseObject
var const int ACCOUNT_ALREADY_LINKED = 208          // An account being linked is already linked to another user
var const int LINKED_ID_MISSING = 250               // A user cannot be linked to an account because that account's ID could not be found
var const int INVALID_LINKED_SESSION = 251          // A user with a linked (e.g. Facebook) account has an invalid session
var const int UNSUPPORTED_SERVICE = 252             // A service being linked (e.g. Facebook) is unsupported

var const int AGGREGATE_ERROR = 600                 // There were multiple errors (individual errors can be accessed through the "errors" array)