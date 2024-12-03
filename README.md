# Household-Services-Application

Household Services Application is a multi-user web based app (requires one admin and other service professionals/ customers) which acts as platform for providing comprehensive home servicing and solutions.

![Home](https://github.com/user-attachments/assets/c4b6c1a0-66d9-4326-8449-fdb14d231d0e)

## Index
-   [Roles](#Features)
-   [File Structure](#File-Structure)
-   [Database Structure](#Database-Structure)
    -   [Customer Table Schema](#Customer-Table-Schema)
    -   [Professional Table Schema](#Professional-Table-Schema)
    -   [Service Table Schema](#Service-Table-Schema)
    -   [Service_request Table Schema](#Service_request-Table-Schema)
    -   [Rejected_req Table Schema](#Rejected_req-Table-Schema)
-   [DB Schema ER Diagram](#DB-Schema-ER-Diagram)
-   [Technologies Used](#Technologies-Used) 
-   [Getting Started](#Getting-Started)
	-   [Prerequisites](#Prerequisites)
	-   [Installation](#Installation)
-   [Screenshots](#Screenshots)

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


### 3. Customer - An individual who has to book a service request

- Customer can Login/Register
- Cumtomer can View/ Search/ Book/ Close a respective service
- He/she can give remarks to the Professional after closing the service

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


### Customer Table Schema
```bash
| Column Name    | Column Type | Constraints                           |
|----------------|-------------|---------------------------------------|
| Id             | Integer     | Primary Key, Auto Increment, Not Null |
| Full_name      | String      | Not Null                              |
| Email          | String      | Unique, Not Null                      |
| Phone_number   | Integer     | Not Null                              |
| Password       | String      | Not Null                              |
| Address        | String      | Not Null                              |
| Pincode        | Integer     | Not Null                              |

```


### Professional Table Schema
```bash
| Column Name    | Column Type | Constraints                           |
|----------------|-------------|---------------------------------------|
| Id             | Integer     | Primary Key, Auto Increment, Not Null |
| Full_name      | String      | Not Null                              |
| Email          | String      | Unique, Not Null                      |
| Password       | String      | Not Null                              |
| Phone_number   | Integer     | Not Null                              |
| Service_name   | String      |                                       |
| Address        | String      | Not Null                              |
| Pincode        | Integer     | Not Null                              |
| Experience     | Integer     |                                       |
| Status         | String      |                                       |

```


### Service Table Schema
```bash
| Column Name    | Column Type | Constraints                           |
|----------------|-------------|---------------------------------------|
| Service_id     | Integer     | Primary Key, Auto Increment, Not Null |
| Service_name   | String      | Not Null                              |
| Price          | Integer     | Not Null                              |
| Time_required  | Integer     | Not Null                              |
| Description    | String      | Not Null                              |

```

### Service_request Table Schema
```bash
| Column Name         | Column Type | Constraints                                |
|---------------------|-------------|--------------------------------------------|
| Id                  | Integer     | Primary Key, Auto Increment, Not Null      |
| Service_id          | Integer     | Foreign Key (service.Service_id), Not Null |
| Customer_id         | Integer     | Foreign Key (customer.Id), Not Null        |
| Professional_id     | Integer     | Foreign Key (professional.Id)              |
| date_of_request     | Date        | Not Null                                   |
| date_of_completion  | Date        |                                            |
| Service_status      | String      | Not Null                                   |
| Remarks             | String      |                                            |

```

### Rejected_req Table Schema
```bash
| Column Name         | Column Type | Constraints                                |
|---------------------|-------------|--------------------------------------------|
| id                  | Integer     | Primary Key, Auto Increment, Not Null      |
| service_req_id      | Integer     | Foreign Key (service_request.Id), Not Null |
| professional_id     | Integer     | Foreign Key (professional.Id), Not Null    |

```

## DB Schema ER Diagram

![Database](https://github.com/user-attachments/assets/609c407e-d17e-42fb-a22e-bd007654a63f)

## Technologies Used

1. Flask: Backend framework for building the web application.
2. SQL Alchemy: ORM (Object-Relational Mapping) tool for database interactions.
3. SQLite: Database management system for storing application data.
4. HTML/CSS: Frontend technologies for user interface design and interactivity.
5. Datetime: Python library for handling date and time operations.
6. Jinja2: Template engine for rendering dynamic HTML content.
7. Matplotlib: Python library used for creating different types of charts on the admin/Customer/Professional dashboard.


## Getting Started

### Prerequisites
- Python 3.x
- Flask
- Flask-SQLAlchemy

### Installation
- Clone the repository:
```bash
    git clone https://github.com/Vaibhav0221/Household-Services-Application.git
```

- Navigate to the project directory:
```bash
    cd Code
```

- Install the required packages:
```bash
    pip install -r requirements.txt
```

- Run the app file
```bash
    flask run 
```

- You can also run the main.py
```bash
    python main.py
``` 

- You can also directly run script file
```bash
    ./Setup_and_Run.sh
``` 


## Screenshots

### Login & Register

![Home](https://github.com/user-attachments/assets/af7592a3-318b-40a9-b26a-2a7d6c66db0c)
![C_Signup](https://github.com/user-attachments/assets/5df0d217-63a3-4e4e-bafe-209a952ef291)
![S_Signup](https://github.com/user-attachments/assets/5b5d5b75-f920-4186-849e-c3ef95d884f1)

###Admin Page
![A_home](https://github.com/user-attachments/assets/97185ba1-fa88-4bb5-9b55-eb35fa90a8a8)
![A_Service](https://github.com/user-attachments/assets/c912d914-8e5e-488e-890f-222b8ef1c2d2)
![A_new_service](https://github.com/user-attachments/assets/9d3624b5-d65e-41fc-9a20-b95e01f07ec6)
![A_C_details](https://github.com/user-attachments/assets/7501e583-46ac-419d-b12f-0f97e9a78676)
![A_P_Details](https://github.com/user-attachments/assets/ce1be5b7-9467-4adb-8b40-dd018ff89709)
![A_Search](https://github.com/user-attachments/assets/bf19dcd2-5c6d-4b21-b0cd-cde731183d04)
![A_Summary](https://github.com/user-attachments/assets/0c789723-3f5e-4d13-b479-e0f4efa6657a)


### Customer Page
![C_home](https://github.com/user-attachments/assets/925c92ce-6773-440b-9225-8ffd41849586)
![C_Search](https://github.com/user-attachments/assets/f6f5c8fe-594e-4344-8708-a60f9ff113fa)
![C_summary](https://github.com/user-attachments/assets/2ae793f0-e3d8-4cf2-9586-e40dd9fcb227)




### Professional Page
![P_Home](https://github.com/user-attachments/assets/e4fb22d2-8689-41ed-9fdc-5b915554364e)
![P_Search](https://github.com/user-attachments/assets/c3cf1f8c-fdf4-4ebe-9cf9-59432b22c050)
![P_Summary](https://github.com/user-attachments/assets/3429e5e9-16d5-47ef-ac47-c47eef85a156)

