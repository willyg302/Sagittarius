# Communication Protocol

## Client to Server

- URL-encoded list of parameters through an HTTP POST with the `application/x-www-form-urlencoded` enctype
	- Ex: `param1=value1&param2=value2&...`
- Parameter names may be repeated
	- Ex: `repeated=value1&repeated=value2&other=value3`
- Values may have several "parts", separated by double-colons (`::`)
	- Ex: `param1=value1part1::value1part2::value1part3`
	- How `::` are treated is mostly action-specific
		- Ex: `f=key::value` is used by action handlers to tell the server to filter for DBObjects whose `key == value`
	- It isn't a good idea to have `::` in a value unless you know they will be handled properly

### Value Encryption Using Tildes

- If a value **starts** with a tilde (`~`), then it has been encrypted by the client and must be decrypted by the server before use
	- Ex: `&param1=~AB127C8E...`
- If a value **ends** with a tilde (`~`), then the information returned by the server corresponding to this value must be encrypted
	- Ex: `&param1=IP~`
- A decrypted value may not start or end with a tilde (in general, avoid having tildes in a value)
- A value cannot have both a start and an end tilde
	- If a value is encrypted and its return value must also be encrypted, apply the end tilde *first*, then encrypt the result
	- The value received by the server will have a start tilde, which when decrypted will have an end tilde

### Mustaches

- Values may include template markets in mustache syntax (`{{template}}`) that will be replaced by the preprocessor **after** decryption has been done
	- Ex: `&param1=ip::{{IP}}` instructs the preprocessor to replace `{{IP}}` with the client's remote IP string
- A table of available mustaches:

Mustache | Description
-------- | -----------
`{{IP}}` | Client's remote IP (string)

## Server to Client

- JSON object
- Always has a single "success" value, which is "y" when the operation has been successful and an error message otherwise
	- Note: if the "success" value is anything other than "y" (even something like "yes"), it will be treated as an error client-side
- Response otherwise depends on context

## Server Execution Order

- Encompasses all operations from the time the server receives a POST request to the time it sends a response
- During that time it will do the following:
	1. Retrieve all necessary values from the URL-encoded request
	2. For each value,
		a. If the value starts with a tilde, decrypt it
		b. Replace any mustaches with their substitutes
	3. Perform any requested actions (query, send mail, etc.), which may include further parsing parts of a value or the value itself
	4. If any value ends with a tilde, encrypt its corresponding part of the response
- It should be noted that decrypting and preprocessing are handled transparently by the custom `Request.get()` and `Request.get_all()` methods

# SagittariusLinkClient

Handles HTTP requests and responses (SagRequest/SagResponse). Should be **sandboxed**, in that other classes do not care about how the Internet works, or even that there are asynchronous events happening.

## What Other Classes "Know"

- I can submit a SagRequest to the SagittariusLinkClient
- If I submit a SagRequest, I am guaranteed to get a SagResponse back
	- I do not know when this will happen (e.g. I cannot expect a response in 5 seconds)
	- A response does not necessarily mean the SagRequest has been handled
- If I submit two requests, A first followed by B, I am guaranteed to get a response for A before I get a response for B

## What SagittariusLinkClient "Knows"

- When I receive a SagRequest, I put it in a queue
- If I am not servicing a request, I'll take the next request in the queue and start servicing it
- I **must** generate a SagResponse for each SagRequest I service
	- Even if a connection cannot be made (no Internet?)
	- If the HTTP response code is not 200
	- Any other error (syntax, etc.)
- When I am done servicing a request, I let Sagittarius know about it
