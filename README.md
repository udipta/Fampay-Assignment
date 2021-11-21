# FamPay-Hiring-Assignment
Backend Assignment
***
<h4>TechStack Used</h4>

1. Python (Programming Language)<br>
2. Django (Web Framework)<br>
3. PostgreSQL (Database)<br>
***
<h4> API's Postman Screenshots</h4>
<h6> 1. Get Videos (GET Request)</h6>
Returns all the videos order by latest published date. When you get an error <b>All APIKey's Quota is over/Empty, Add a new APIKey</b> use Add Key API (2nd point) for adding a new Youtube Data API Key in the database.

***
![Alt text](get_video.png?raw=true "Get Videos Page")

| Status  |   Time  |    Size     |
| ------- | ------- | ------------|
| 200 OK  |   76 ms |   19.79 KB  |
***

<h6> 2. Add Key (POST Request)</h6>
When you get an error <b>All APIKey's Quota is over, Add a new APIKey</b>, then use this api, for adding a new Youtube Data API Key in the database, so the service will start again, fetch and store videos in the database.

***
![Alt text](add_key.png?raw=true "Add Key Page")

| Status  |   Time  |    Size     |
| ------- | ------- | ------------|
| 201 OK  |   27 ms |    378 B    |
***

<h5><a href="https://www.getpostman.com/collections/0c922d080f0bbd00fc56"> Postman Collection</a></h5>

***
<h4> Steps to Follow</h4>

1. Clone the Repository
2. Run the following command
    ```
    $ docker-compose up --build
    ```

3. Now create superuser for accessing the dashboard to view the stored videos
    ```
    $ docker exec -it fampay bash
    $ python3 manage.py createsuperuser
    ```

4. To access the dashboard checkout http://127.0.0.1/admin

***
Now run the following apis described in the Postman collection for testing the project.

