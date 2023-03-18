# studentflaskAPI

About Student Management API
Student Management API does the main function of a school and explains how it works. It enables the school to create an admin account. It allows the registration of students and lecturers. Also, the API allows the school admin to create courses and handling the grading system for the student.

CRUD operations can be carried out on the student data and the courses data, with an easy-to-use Swagger UI setup for testing and integration with the front end.

A Student account have limited access to the app, as a student can only change their profile details and view their profile, courses, grades and GPA.

This Student Management API was built with Python's Flask-RESTX by Ajayi Oluwaseyi during Backend Engineering live classes at AltSchool Africa. This was built as my third semester final capstone project in AltSchool Africa.

back to top

Built With:
Python Flask SQLite


##Project Scope
The Student Management API handles the following:

Admin Registration
Lecturer Registration
Student Registration
Getting Student Information and applying the CRUD operation
Course Creation
Getting a Course details and using the CRUD operation
Multiple Course Registration for Students
Assigning a Lecturer to a course
Adding a Student Score
Calculating a Student GPA using the 4.0 Grading System.
The future Versions will cover more aspects and features as needed soon.


##Lessons
Creating this API helped me learn and practice:

API Development with Python
App Deployment with PythonAnywhere
Testing with pytest and Insomnia
Documentation
Debugging
Routing
Database Management
Internet Security
User Authentication
User Authorization





To explore and use this API, follow these steps:

Open the web app on your browser: https://student-flask-api.herokuapp.com/

Create an admin or student or lecturer account:

Click 'auth' to reveal a dropdown menu of the authentication routes, then register an admin account via the '/auth/signup' route. Input your details and input 'admin' in the 'user-type' to create an admin account.
Click 'auth' to reveal a dropdown menu of the authentication routes, then register a student account via the '/auth/signup' route. Input your details and input 'student' in the 'user-type' to create an admin account.
Click 'auth' to reveal a dropdown menu of the authentication routes, then register a lecturer account via the '/auth/signup/lecturer' route. Input your details to create a lecturer account.
Login via the '/auth/login' route to generate a JWT token. Copy the access token only without the quotation marks

Scroll back up to click Authorize at top right. Enter the JWT token in the given format, for example:

Bearer eyJhbtestXVCJ9.eyJbmMzd9.this_rQh8_tl2V1iDlsl_wAOMHcing5334
Click Authorize and then Close.

Now authorized, you can create, view, update and delete students, courses and grades via the routes in 'students' and 'courses'. You can also see the information about:

All students taking a course
All courses taken by a student
A student's grades in percentage (example: 84.0) and letters (eg: B+)
A student's GPA, calculated using the 4.0 grading system based on all grades from all courses they are taking (example: 3.3)
Go to the Course Namespace and create a new course before adding a student to the course

Then go on ahead to perform other operations and test all the routes. Enjoy!

When you're done, click 'Authorize' at top right again to then 'Logout'. Also, head on to the '/auth/logout' route to log the user out and revoke the access token.

Note: Any registered user can request to reset their password through the '/auth/password-reset-request' route and the link to reset their password will be sent to the user's mail. Copy the token from the link that was sent to your mail and paste it in the token field in the '/auth/password-reset/' route. Then you can go on to change your password.
