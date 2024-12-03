# Household-Services-Application

Household Services Application is a multi-user web based app (requires one admin and other service professionals/ customers) which acts as platform for providing comprehensive home servicing and solutions.

![Home](https://github.com/user-attachments/assets/c4b6c1a0-66d9-4326-8449-fdb14d231d0e)

## Index
-   [Roles](#Features)
-   [File Structure](#File-Structure)
-   [Database Structure](#Database-Structure)
    -   [Course Table Schema](#Course-Table-Schema)
    -   [Student Table Schema](#Student-Table-Schema)
    -   [Enrollment Table Schema](#Enrollment-Table-Schema)
-   [Getting Started](#Getting-Started)
	-   [Prerequisites](#Prerequisites)
	-   [Installation](#Installation)
-   [Screenshots](#Screenshots)
-   [Further Api Implementation](#Further-Api-Implementation)       	

## Roles

This platform is having three roles:

### 1. Admin - root access: it is a superuser of the app and requires no registration.

- Admin login redirects to the admin dashboard
- Admin can monitor all the users (customers/service professionals)
- Admin can create a new service with a base price
- Admin can approve/ reject a service professional after verification of profile docs
- Admin can block customer/service professionals based on fraudulent activity/poor reviews

### 2. Service Professional - An individual that provides the service

- Professional can Login/Register
- professionals can accept/reject a request
- One professional is good at one of the services only
- He/she can accept/reject an assigned service request in respective service
- Professional will exit the location after the service is closed by the customer

## File Structure

```bash
.
Code
    ├── Application
    │   ├── config.py 
    │   ├── controller.py      //Routes
    │   ├── database.py
    │   └── models.py    
    ├── Project_Report.pdf
    ├── Setup_and_Run.sh
    ├── db_directory
    │   └── sql.db
    ├── main.py                //Entrypoint of Application
    ├── requirements.txt
    ├── static
    │   ├── Images
    │   │   ├── A_Summary_1.jpg
    │   │   ├── A_Summary_2.jpg
    │   │   ├── C_Summary_1.jpg
    │   │   ├── Favicon.png
    │   │   ├── Logo.jpg
    │   │   ├── P_Summary_1.jpg
    │   │   └── P_Summary_2.jpg
    │   ├── style.css
    │   └── style1.css
    └── templates              //View
        ├── Admin_Customer.html
        ├── Admin_Search.html
        ├── Admin_Services.html
        ├── Admin_Summary.html
        ├── Admin_edit_service.html
        ├── Admin_header.html
        ├── Admin_home.html
        ├── Admin_new_service.html
        ├── Admin_professional.html
        ├── Customer_Search.html
        ├── Customer_Service.html
        ├── Customer_Summary.html
        ├── Customer_details.html
        ├── Customer_edit_details.html
        ├── Customer_header.html
        ├── Customer_home.html
        ├── Customer_register.html
        ├── Customer_req_close.html
        ├── Login.html
        ├── Professional_Search.html
        ├── Professional_Summary.html
        ├── Professional_details.html
        ├── Professional_edit_details.html
        ├── Professional_header.html
        ├── Professional_home.html
        └── Professional_register.html
```
## Database Structure
### 3. Customer - An individual who has to book a service request

- Customer can Login/Register
- Cumtomer can View/ Search/ Book/ Close a respective service
- He/she can give remarks to the Professional after closing the service

  
