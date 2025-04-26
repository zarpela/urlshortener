## How to run URL shortener
### Step 1: set MySQL password
To run this project, you need to set the database password on the `main.py` file. Follow the following steps to set it.

1. Open the `main.py` file in your code editor
2. Find go to line 12  and set your MySQL database password. Example:

   ```python
   banco = mysql.connect(
    host="localhost",
    user="root",
    password="YOUR_PASSWORD",
    database="URLShortener"
    )

### Step 2: run the SQL query to create the database
To make the data persist, the shortened urls are stored in the table created in the `sql.sql` file. To create the database run the following command:

  `mysql -u root -p < "sql.sql"`

### Step 3: run the project
To run the project, execute the following command:

  `fastapi dev main.py`
      
And then open the ip showed at '   server   Server started at http://x.x.x.x:xxxx' on your browser of choice
