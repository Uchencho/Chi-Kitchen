# Chi-Kitchen

:sparkles:Food Service Rest API built with Django Rest Framework. This api comes fully loaded with the following features
- Authentication and Authorization
- Payment System
- Backoffice endpoints

## Project Overview
On a very high level, this is supposed to power up a service (app/web) that provides cooked meals as a product. It allows users do the following
- Create an account with an email address
- Update profile by adding firstname, lastname, phone number etc
- Creates orders for available dishes
- Edit orders
- Delete orders
- Make payment for orders through paystack api
- Verify order status
- View history of Payment
- View history of Orders

As an admin user (owner) of the service, you would be able to
- Create dishes
- Change status of dishes
- See all users who have registered for the service
- Track payment of Orders
- See details of orders that were taken and much more


### Mobile/Front-end Developer 👋
Are you a mobile/frontend developer interested in building an app and consuming this service, please send me a mail aloziekelechi17@gmail.com :grin:

-----------------------------------------------------------------------------------------------------------------------------------------------------
### Employer/Backend Developer 👋
If you are here, you want details about what I built and how I built it. Let us Dive in :collision:

Needless to say, the project is segmented into apps:
- Accounts
- Backoffice
- Food :grin:

No, I didn't upload a documentation because I have not hosted it and I have esperience doing that already. [Sample documentation by me](https://documenter.getpostman.com/view/11324986/SzzhddRx?version=latest#044d99a9-a717-4581-873b-40f18462fd73).
Yes I wrote tests, they can be found in api/tests.py for each app.
I am huge fan of class based views so 99% of my views are CBV :grin:. Yes, I definitely use serializers in my APIs.

#### Accounts
I built a custom user by inheriting the base user class. I did this because of my intention of using google login plugin that allows a user login with his gmail account.
Also the second reason for doing this is because I wanted to add extra fields like phone number, house address and gender to the user table.

Authorization and Authentication is token based where I created a table that stores the token for each user on each login. Yes, I plan to setup a cron job to delete expired tokens.
The essence of storing the token is to prevent a user who has logged out from accessing resources without logging again. 
Security is very important, so although, an access token and a refresh token is returned on each login, they both expire after 90 minutes. This ensures even if a user's access token is compromised,
it would expire in 30 minutes and the refresh token would expire in 90 minutes.:alien:

Five Views were created as endpoints
- Registeration view: as the name implies, registers users
- Profile Detail view: allows users edit their details, it doen't allow users to delete their profile
- Login View : returns details of a user, access and refresh tokens too
- Refreshtoken View : refreshes a token as long as it was not used to logout
- Logout View - Adds tokens to black listed table of tokens
