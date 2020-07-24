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
- Food :poultry_leg:

No, I didn't upload a documentation because I have not hosted it and I have experience doing that already. [Sample documentation by me](https://documenter.getpostman.com/view/11324986/SzzhddRx?version=latest#044d99a9-a717-4581-873b-40f18462fd73).
Yes I wrote tests, they can be found in api/tests.py for each app.
I am huge fan of class based views so 99% of my views are CBV :grin:. Yes, I definitely use serializers in my APIs.

#### Accounts
I built a custom user by inheriting the base user class. I did this because of my intention of using google login plugin that allows a user login with his gmail account.
Also the second reason for doing this is because I wanted to add extra fields like phone number, house address and gender to the user table.

Authorization and Authentication is token based where I created a table that stores the token for each user on each login. Yes, I plan to setup a cron job to delete expired tokens.
The essence of storing the token is to prevent a user who has logged out from accessing resources without logging again. 
Security is very important, so although an access token and a refresh token is returned on each login, they both expire after 90 minutes. This ensures even if a user's access token is compromised,
it would expire in 30 minutes and the refresh token would expire in 90 minutes.:alien:

Five Views were created as endpoints
- __Registeration view__: as the name implies, registers users
- __Profile Detail view__: allows users edit their details, it doesn't allow users to delete their profile
- __Login View__: returns details of a user, access and refresh tokens too
- __Refreshtoken View__: refreshes a token as long as it was not used to logout
- __Logout View__: Adds tokens to black listed table of tokens


#### Food :hamburger: :poultry_leg:
This is where the meat of the service lies, this app is responsible for creating dishes, creating orders, tracking payments and verifying payments. This app consists of ten views that do the following

- __DishView__ : Lists all available dishes for a user to make an order. Available dishes is dependent on if a dish has been created, if it is still active and if it falls on the available date (a get_query method was very useful in achieving this, God bless CBV :nail_care:)

- __UserCartView__ : Lists all the orders a user has created but has not initiated payment for. This is useful especially for analytics and tracking, knowing that customers keep adding beautiful dishes but never pay is a valuable insight. Yes, it is limited to each user's 'cart'. Mr A cannot see Mr B's cart :v:.

- __CreateOrderView__ : This allows a user create a dish and checks that the dish that is being sent from the frontend is actually available :unamused:. It allows the user create multiple dishes at a go, efficiently utilizing bulk_create by hitting the db once:ok_hand:.

- __CartDetailAPIView__ : Details orders that have been added to the list and offers updating and deletion.

- __PaymentCheckoutView__ : This uses the paystack api to initialize a transaction with the user's email and total cost of items in the cart, the response which would contain a redirect url is stored in the db for efficient tracking should the need arise :moneybag:.

- __VerifyPaymentView__: A view to be verify that :dollar: actually entered the account. If Paystack confirms successful payment, status of payment changes to successful and admin user is alerted via mail to provide service.

- __OrderEntryView__ : Returns an overview of the list of orders that payment has been initiated for

- __OrderInfoView__ : Details the content of an order, that is the list of the dishes. Yes, an order can contain more than one dish.

- __PaymentHistoryView__ : For each order entry, I provided a list view for all payment trials.

- __PaymentRetryView__ : Last but not least, a payment retry view. This can only be initaited from the order entry view. This was done where a user sees that his payment failed and would like to try again.


#### Backoffice
Yes, the admin page is up and running but it has some limitations and I wanted to experiment building endpoints that mirror some of the things admin does. All the endpoints in the backoffice app need admin user priviledges to access :guardsman:.

The following endpoints are available:

- __OrderInfoView__ : Lists all order information for all users. Search capability is extended for this view as the admin is allowed to search by delivery date and status of order info.

- __CreateDishView__ : Allows an admin create a dish :fries:

- __DishDetailView__ : Details a dish that has already been created and allows the admin access to delete dishes and deactivate dishes.

- __PaymentHistoryAdminView__ : Endpoint that allows the admin see all payment attempts that have been initiated through the app.

- __UserListView__ :  Allows the admin to see all :woman: and :man:

- __UserDetailView__ : Details of a user, allows admin have the user to all fields apart from PASSWORD :lock:. Admin user also has the priveledge of deleting a particular user profile. By design, deleting a user's profile cascades a lot actions (deletes everything about that user on the system, EVERYTHING).


### Contribution
Any issue or suggestion, please raise an issue or make a PR. Leave a like please :grin:, I like the attention :wink:
