# Appsembler API

## Authentication
The API requires OAuth authentication to grant access to the endpoints and actions.

All endpoints can return the following response errors if there is a problem with the authentication process:

### Credentials not provided
* Code: 401 UNAUTHORIZED
* Content: `{ detail : "Authentication credentials were not provided." }`
* Reason: Authentication credentials were not provided.

### Invalid Token
* Code: 401 UNAUTHORIZED
* Content: `{ detail : "Invalid Token." }`
* Reason: Invalid OAuth Token.

## User endpoints

### Create User Account

This endpoint creates a new edX user. It's possible to avoid the activation email sending using the `send_activation_email` set to "False"

* URL: `/appsembler_api/v0/accounts/create`
* Method: `POST`
* Data Params
	* Required:
		* 'username'
		* 'password'
		* 'email'
		* 'name'
		* 'send_activation_email' (True or False)

* Success Response
	* Code: 200
	* Content:
```
{
	"user_id ": 65, # the id of the new user
}
```
* Error Responses:
	* Code: 400
	* Content: `{"user_message": "Wrong parameters on user creation"}`
	* Reason: Wrong parameters on user creation

	* Code: 409
	* Content: `{"user_message": "User already exists"}`
	* Reason: User already exists

* Example call:
```
POST /appsembler_api/v0/accounts/create
Host: example.com
Content-Type: application/json
Authorization: Bearer cbf6a5de322cf6a4323c957a882xy1s321c954b86
Cache-Control: no-cache
{
    "username": "staff55",
    "password": "edx",
    "email": "staff55@example.com",
    "name": "stafftest"
}
```

### Create User Account Without Username And Password
This endpoint has a different set of parameters and more complex workflow than `Create User Account`.
This endpoint creates a user account with minimal parameters, the endpoint is capable to create an user account only with the email address and a person Name (not username).
#### Workflow description:
1. The endpoint is called with an email and a person name.
2. The endpoint autogenerates a password and an username.
3. After created the user in a non active state, an email is sent to the user, with a set password link.
4. After the user follows the link and set a new password, the account becomes active, and the new password is save.

* URL: `/appsembler_api/v0/accounts/user_without_password`
* Method: `POST`
* Data Params
	* Required:
		* 'email'
		* 'name'
	* Optional:
	    * 'country'
	    * 'city'
	    * 'gender'
	    * 'goals'
	    * 'level_of_education'
	    * 'year_of_birth'

* Success Response
	* Code: 200
	* Content:
```
{
    "username": "honor906", # the generated username
    "user_id ": 65 # the id of the new user
}
```

* Error Responses:
	* Code: 400
	* Content: `{"user_message": "Wrong parameters on user creation"}`
	* Reason: Wrong parameters on user creation

	* Code: 409
	* Content: `{"user_message": "User already exists"}`
	* Reason: User already exists

* Example call:
```
POST /appsembler_api/v0/accounts/create
Host: example.com
Content-Type: application/json
Authorization: Bearer cbf6a5de322cf6a4323c957a882xy1s321c954b86
Cache-Control: no-cache
{
    "email": "staff58@example.com",
    "name": "stafftest"
}
```



### Connect User Account
This endpoint connects an existing Open edX user account to one in an external system. Given a username, the endpoint has the ability to change the user email, password and name.

* URL: `/appsembler_api/v0/accounts/connect`
* Method: `POST`
* Data Params
    * Required:
        * `username`
    * Optional:
        * `email`
        * `password`
        * `name`

* Success Response
    * Code: 200
    * Content:
```
{
    "user_id ": 65, # the id of the existing user
}
```


* Error Responses:
    * Code: 400
    * Content: `{"user_message": "Wrong parameters on user connection"}`
    * Reason: Wrong parameters on user connection

    * Code: 404
    * Content: {"user_message": "User not found"}
    * Reason: No user exists with the provided email address.

    * Code: 409
    * Content: ["user_message": "The email test@example.com is in use by another user"}
    * Reason: The email that you're trying to set is in use by another user.

    * Code: 409
    * Content: ["user_message": "Invalid email format"}
    * Reason: Error in the email format.

* Example call:
```
POST /appsembler_api/v0/accounts/connect
Host: example.com
Content-Type: application/json
Authorization: Bearer cbf6a5de322cf6a4323c957a882xy1s321c954b86
Cache-Control: no-cache
{
    "username": "test_user",
	"name": "Test User",
	"email": "test_user@example.com",
	"password": "new@pass"
}
```

### Update user account

This endpoint allows to update a user account. Receives a lookup parameter and N optional parameters which are all the attributes that needs to be updated.
The endpoint can update email, all available profile fields and also has support for [registration extension form fields](https://github.com/open-craft/custom-form-app).

* URL: `/appsembler_api/v0/accounts/update_user
* Method: `POST`
* Data Params
    * Required:
        * `user_lookup` # can be username or email
    * Optional:
        * `email` # user's email
        * `name` # user full name
        * `country` # country iso code, ex: `ES`, `UY`, `US`
        * `gender` # user gender, accepted values `m`, `f` or `o`
        * `level_of_education` # user education, accepted values `p`, `m`, `b`, `a`, `hs`, `jhs`, `el`, `none` or `other`, 
        * `year_of_birth` # four digit year as string
        * `city` # text
        * `mailing_address` # long text 
        * `language` # language iso code, ex 'ES', 'EN'
        * `goals` # long text
        * `bio` # text

You also can send extended profile form fiels, but that depends on every installation, you'll need to find the [registration extension form app fork](https://github.com/open-craft/custom-form-app) that is installed on the instance, and check the field names, and accepted values. 
        
* Success Response
	* Code: 200
	* Content: Success message and list of updated fields and values
```
{
    "success": "The following fields has been updated: name=Doe, John, country=ES"
}
```
* Error Responses:
	* Code: 404 NOT FOUND
	* Reason: User not exists

* Error Responses:
	* Code: 400 NOT FOUND
	* Reason: No user lookup parameter sent

* Example call:
```
POST /appsembler_api/v0/accounts/update_user
Host: example.com
Content-Type: application/json
Authorization: Bearer cbf6a5de322cf6a4323c957a882xy1s321c954b86
Cache-Control: no-cache
{
	"user_lookup": "staff@example.com",
	"emai": "new_staff@example.com",
	"name": "Staff New Name",
	"country": "US",
	"gender": "f",
	"level_of_education": "m",
	"year_of_birth": "2000",
	"city": "Montevideo",
	"mailing_address": "A streen and a number 2345 FL, USA",
	"language": "es",
	"goals": "To be famous",
	"bio": "I'm not famous yet"
	"district": "101815" # a custom form field
}
```

### Check Existing Username

This endpoint is a tool to check if an user exists given the username.

* URL: `/appsembler_api/v0/accounts/get-user/(?P<username>[\w.+-]+)`
* Method: `GET`

* Success Response
	* Code: 200
	* Content:
```
{
	"user_id ": "username",
}
```
* Error Responses:
	* Code: 404 NOT FOUND
	* Reason: User not exists

## Enrollment Codes endpoints

### Generate Enrollment Codes
This endpoint generates enrollment codes for a course. You can later enroll users in the course using the endpoint below and the generated codes. This endpoint takes as parameters a course ID and the amount of desired codes to be generated.
More info about Enrollment Codes [edX Docs](http://edx.readthedocs.io/projects/open-edx-building-and-running-a-course/en/latest/manage_live_course/manage_course_fees.html#create-and-manage-enrollment-codes)

* URL: `/appsembler_api/v0/enrollment-codes/generate`
* Method: `POST`
* Data Params
	* Required:
		* `course_id` (the course id `course-v1:Org+Code+Run`)
		* `total_registration_codes` (the amount of codes to generate and save)

* Success Response
	* Code: 200
	* Content:
```
{
  "course_id": "course-v1:edX+DemoX+Demo_Course",
  "codes": [
    "VQSG0xsg",
    "dWvbNXBT",
    "2z0rcZZs",
    "0Q6NvXFW",
    "xMc7SDJF"
  ],
  "course_url": "/courses/course-v1:edX+DemoX+Demo_Course/about"
}
```
* Example call:
```
POST /appsembler_api/v0/enrollment-codes/generate
Host: example.com
Content-Type: application/json
Authorization: Bearer cbf6a5de322cf6a4323c957a882xy1s321c954b86
Cache-Control: no-cache
{
    "course_id": "course-v1:edX+DemoX+Demo_Course",
    "total_registration_codes": "20"
}
```

### Enroll User With Code
This endpoint allows you to enroll a user into a course using previously-generated Enrollment Codes. The endpoint takes as parameters the user email and the enrollment code.

* URL: `/appsembler_api/v0/enrollment-codes/enroll-user`
* Method: `POST`
* Data Params:
	* Required:
`email` (the user email)
`enrollment_code`: (the enrollment code obtained in the previous endpoint `/appsembler_api/v0/enrollment-codes/generate`)
* Success Response:
	* Code: 200
	* Content:
```
{
    "success": "true",
}
```
* Error Responses:
	* Code: 400
	* Content: `{ "success": "false", "reason" : "Enrollment code error." }`
	* Reason: Enrollment code error.
**OR**
	* Code: 400
	* Content: `{ "success": "false", "reason" : "Enrollment code error." }`
	* Reason: Enrollment closed.
**OR**
	* Code: 400
	* Content: `{ "success": "false", "reason" : "Course full." }`
	* Reason: Course full.
**OR**
	* Code: 400
	* Content: `{ "success": "false", "reason" : "Already enrolled." }`
	* Reason: Already enrolled.

* Example call
```
POST /appsembler_api/v0/enrollment-codes/enroll-user
Host: example.com
Content-Type: application/json
Authorization: Bearer cbf6a5de322cf6a4323c957a882xy1s321c954b86
Cache-Control: no-cache
{
    "email": "staff@example.com",
    "enrollment_code": "V5QBQMN6"
}
```


### Enrollment Code Status
Via this endpoint the status of the Enrollment Codes can be changed. The endpoint takes as parameters the enrollment Code and the action (cancel or restore)

**cancel** When you can cancel an enrollment code, the code becomes unavailable. If a user was enrolled using this code, the user will be unenrolled from the related course.

**restore** If the code was previously "cancelled", it will become available again. If the code was active and a user was enrolled in a course using it, the user will be unenrolled from the course, and the code will be available again for enrolling another user.

* URL: `/appsembler_api/v0/enrollment-codes/status`
* Method: `POST`
* Data Params:
	* Required:
`enrollment_code` (the enrollment code obtained in the previous endpoint `/appsembler_api/v0/enrollment-codes/generate`)
`action`: ('cancel' or 'restore')
* Success Response:
	* Code: 200
	* Content: `{"success": "true"}`
* Error Responses:
	* Code: 400
	* Reason: `{ "success": "false", "reason" : "The enrollment code ({code}) was not found"}`
* Example call:
```
POST /appsembler_api/v0/enrollment-codes/status
Host: example.com
Content-Type: application/json
Authorization: Bearer cbf6a5de322cf6a4323c957a882xy1s321c954b86
Cache-Control: no-cache
{
    "enrollment_code": "V5QBQMN6",
    "action": "restore"
}
```
**OR**
```
POST /appsembler_api/v0/enrollment-codes/status
Host: example.com
Content-Type: application/json
Authorization: Bearer cbf6a5de322cf6a4323c957a882xy1s321c954b86
Cache-Control: no-cache
{
    "enrollment_code": "1Ls34dQa",
    "action": "cancel"
}
```

## Bulk Enrollment Endpoints

### Bulk Enrollment

Endpoint that allows you to enroll or unenroll multiple students into/out of multiple courses with
optional email notification.

* URL: `/appsembler_api/v0/bulk-enrollment/bulk-enroll`
* Method: `POST`
* Data Params
	* Required:
		* action ( 'enroll' or 'unenroll' )
		* identifiers (comma separated list of student emails, example: `test_user@appsembler.com,another_user@appsembler.com` )
		* courses (comma separated list of student emails, example:
`course-v1:edX+DemoX+Demo_Course,course-v1:Appsembler+APP101+1Q2016` )
	* Optional:
		* auto_enroll (boolean, defaults to false )
		* email_students (boolean, defaults to false )

* Success Response:
	* Code: 200
	* Content:
	```
	{
	"action": "unenroll",
	"courses": {
		"course-v1:edX+DemoX+Demo_Course": {
			"action": "unenroll",
			"results": [{
				"identifier": "test@appsembler.com",
				"after": {
					"enrollment": false,
					"allowed": false,
					"user": true,
					"auto_enroll": false
				},
				"before": {
					"enrollment": false,
					"allowed": false,
					"user": true,
					"auto_enroll": false
				}
			}],
			"auto_enroll": true
		}
	},
	"email_students": false,
	"auto_enroll": true
}
	```

* Error Response: I
	* Code: 401 UNAUTHORIZED
	* Content: { detail : "Authentication credentials were not provided." }
	* Reason: Missing or incorrect auth credentials
**OR**
	* Code: 404 NOT FOUND
	* Content: { detail : "Not found" }
	* Reason: Wrong course ID
**OR**
	* Code: 400 BAD REQUEST
	* Content: {"identifiers": ["This field is required."]}
	* Reason: Missing a required field

* Sample Call:
```
POST /appsembler_api/v0/bulk-enrollment/bulk-enroll
Host: example.com
Content-Type: application/json
Authorization: Bearer cbf6a5da152cf6a4833c957d882ee1624c954b86
Cache-Control: no-cache
{
	"action": "enroll",
	"auto_enroll": true,
	"identifiers": "test@appsembler.com,test1@appsembler.com,test2@appsembler.
	com ",
	"email_students": true,
	"courses": "course-v1:edX+DemoX+Demo_Course,course-v1:Appsembler+APP101+1Q
	2016 "
}
```

## Analytics Endpoints

### Accounts

This endpoint provides information about user accounts. Can be called with filters for start date and end date, or can be called without parameters in order to get information for all registered accounts.

* URL: `/appsembler_api/v0/analytics/accounts/batch`
* Method: `GET`
* Optional URL Params:
	* `updated_min` (YYYY-MM-DD) Start date
	* `updated_max` (YYYY-MM-DD) End date

* Success Response
	* Code: 200
	* Content:
	```
    {
    "username": "anewuser",
    "date_joined": "2016-12-17T23:45:47Z",
    "is_active": true,
    "id": 29,
    "email": "anewuser@example.com"
  },
  {
    "username": "newtest",
    "date_joined": "2016-12-17T23:55:27.765Z",
    "is_active": true,
    "id": 30,
    "email": "newtest@example.com"
  },
  ...
 	```
* 	Example calls:
	* `/appsembler_api/v0/analytics/accounts/batch` All data of all users
	* `/appsembler_api/v0/analytics/accounts/batch?updated_min=2015-12-09T00:00:00Z` Get data on users created after Dec 9th 2015
	* `/appsembler_api/v0/analytics/accounts/batch?updated_min=2015-12-09T00:00:00Z&updated_max=2015-12-19` Get data on users created between Dec 9th and 19th 2015

### Enrollments

This endpoint provides information about course enrollment. Can be called with filters for course, start date and end date (the user enrollment date), username or can be called without parameters to get information for all enrollments. If the student has finished the course and requested a certificate in a certain course, the information will be included.

* URL: `/appsembler_api/v0/analytics/enrollment/batch`
* Method: `GET`
* Optional URL Params:
	* `course_id` (course-v1:Org+Course+Run)
	* `updated_min` (YYYY-MM-DD) User enrollment start date
	* `updated_max` (YYYY-MM-DD) User enrollment end date
	* `username` (staff)

* Success Response
	* Code: 200
	* Content:
	```
	[
  {
    "username": "honor",
    "course_id": "course-v1:edX+DemoX+Demo_Course",
    "user_id": 2,
    "enrollment_id": 1,
    "date_enrolled": "2016-05-23T16:17:07.585Z"
  },
  {
    "username": "audit",
    "course_id": "course-v1:edX+DemoX+Demo_Course",
    "user_id": 3,
    "enrollment_id": 2,
    "date_enrolled": "2016-05-23T16:17:11.068Z",
    "cerificate": {
        "grade": "1.0",
        "url": "",
        "completion_date": "2017-01-24 14:32:21+00:00"

    }
  },
  ...
  ]
	```

* 	Example calls:
	* `/appsembler_api/v0/analytics/enrollment/batch` Get all course enrollments
	* `/appsembler_api/v0/analytics/enrollment/batch?course_id=course-v1%3Aedx%2BDemoX101%2B2017` Get all course enrollments for edX DemoX Course
	* `/appsembler_api/v0/analytics/enrollment/batch?course_id=course-v1%3Aedx%2BDemoX101%2B2017&update_min=2016-01-07` Get all course enrollments for Food Safety 101 enrolled after Jan 7th 2016: