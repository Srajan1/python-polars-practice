import polars as pl

# https://leetcode.com/problems/big-countries/description/?envType=study-plan-v2&envId=30-days-of-pandas&lang=pythondata
'''
A country is big if:

    it has an area of at least three million (i.e., 3000000 km2), or
    it has a population of at least twenty-five million (i.e., 25000000).
return all big countries.

+-------------+------------+---------+
| name        | population | area    |
+-------------+------------+---------+
| Afghanistan | 25500100   | 652230  |
| Algeria     | 37100000   | 2381741 |
+-------------+------------+---------+
'''

countries = pl.DataFrame(
    {
        "name": ["Afghanistan","Albania","Algeria","Andorra","Angola",],
        "continent": ["Asia","Europe","Africa","Europe","Africa",],
        "area": [652230, 28748, 2381741, 468, 1246700,],
        "population": [25500100, 2831741, 37100000, 78115, 20609294,],
        "gdp": [20343000000, 12960000000, 188681000000, 3712000000, 100990000000,],
    }
)


big_countries = countries.select(pl.col('name', 'population', 'area')).filter((pl.col('area') >= 3000000) | (pl.col('population') >= 25000000))

# https://leetcode.com/problems/recyclable-and-low-fat-products/description/?envType=study-plan-v2&envId=30-days-of-pandas&lang=pythondata

'''
Write a solution to find the ids of products that are both low fat and recyclable.
Input: 
Products table:
+-------------+----------+------------+
| product_id  | low_fats | recyclable |
+-------------+----------+------------+
| 0           | Y        | N          |
| 1           | Y        | Y          |
| 2           | N        | Y          |
| 3           | Y        | Y          |
| 4           | N        | N          |
+-------------+----------+------------+
Output: 
+-------------+
| product_id  |
+-------------+
| 1           |
| 3           |
+-------------+
'''

products = pl.DataFrame(
    {
        "product_id": [0, 1, 2, 3, 4],
        "low_fats": ["Y", "Y", "N", "Y", "N"],
        "recyclable": ["N", "Y", "Y", "Y", "N"],
    }
)

low_fat_recycle = products.filter((pl.col('low_fats') == 'Y') & (pl.col('recyclable') == 'Y'))

# https://leetcode.com/problems/customers-who-never-order/description/?envType=study-plan-v2&envId=30-days-of-pandas&lang=pythondata
'''
find all customers who never order anything.

Customers table:
+----+-------+
| id | name  |
+----+-------+
| 1  | Joe   |
| 2  | Henry |
| 3  | Sam   |
| 4  | Max   |
+----+-------+
Orders table:
+----+------------+
| id | customerId |
+----+------------+
| 1  | 3          |
| 2  | 1          |
+----+------------+
Output: 
+-----------+
| Customers |
+-----------+
| Henry     |
| Max       |
+-----------+
'''

customers = pl.DataFrame(
    {
        "id": [1, 2, 3, 4],
        "name": ["Joe", "Henry", "Sam", "Max"],
    }
)

orders = pl.DataFrame(
    {
        "id": [1, 2],
        "customerId": [3, 1],
    }
)

customers_without_orders = customers.filter(~pl.col('id').is_in(orders['customerId']))

# https://leetcode.com/problems/article-views-i/description/?envType=study-plan-v2&envId=30-days-of-pandas&lang=pythondata

'''
Write a solution to find all the authors that viewed at least one of their own articles.
Views table:
+------------+-----------+-----------+------------+
| article_id | author_id | viewer_id | view_date  |
+------------+-----------+-----------+------------+
| 1          | 3         | 5         | 2019-08-01 |
| 1          | 3         | 6         | 2019-08-02 |
| 2          | 7         | 7         | 2019-08-01 |
| 2          | 7         | 6         | 2019-08-02 |
| 4          | 7         | 1         | 2019-07-22 |
| 3          | 4         | 4         | 2019-07-21 |
| 3          | 4         | 4         | 2019-07-21 |
+------------+-----------+-----------+------------+
Output: 
+------+
| id   |
+------+
| 4    |
| 7    |
+------+
'''

views = pl.DataFrame(
    {
        "article_id": [1, 1, 2, 2, 4, 3, 3],
        "author_id":  [3, 3, 7, 7, 7, 4, 4],
        "viewer_id":  [5, 6, 7, 6, 1, 4, 4],
        "view_date":  [
            "2019-08-01",
            "2019-08-02",
            "2019-08-01",
            "2019-08-02",
            "2019-07-22",
            "2019-07-21",
            "2019-07-21",
        ],
    }
)

viewed_own_article = (
    views
    .filter(pl.col('viewer_id').eq(pl.col('author_id')))
    .unique(subset=['author_id'])
    .select(pl.col('author_id').alias('id'))
)

# https://leetcode.com/problems/invalid-tweets/description/?envType=study-plan-v2&envId=30-days-of-pandas&lang=pythondata

'''
Find tweet which is strictly greater than 15.
Input: 
Tweets table:
+----------+-----------------------------------+
| tweet_id | content                           |
+----------+-----------------------------------+
| 1        | Let us Code                       |
| 2        | More than fifteen chars are here! |
+----------+-----------------------------------+
Output: 
+----------+
| tweet_id |
+----------+
| 2        |
+----------+
'''

tweets = pl.DataFrame(
    {
        "tweet_id": [1, 2],
        "content": [
            "Let us Code",
            "More than fifteen chars are here!",
        ],
    }
)

longer_tweets = tweets.filter(pl.col('content').str.len_chars() > 15).select('tweet_id')

# https://leetcode.com/problems/calculate-special-bonus/description/?envType=study-plan-v2&envId=30-days-of-pandas&lang=pythondata
'''
Write a solution to calculate the bonus of each employee. The bonus of an employee is 100% of their salary if the ID of the employee is an odd number and the employee's name does not start with the character 'M'. The bonus of an employee is 0 otherwise.
Return the result table ordered by employee_id.

Input: 
Employees table:
+-------------+---------+--------+
| employee_id | name    | salary |
+-------------+---------+--------+
| 2           | Meir    | 3000   |
| 3           | Michael | 3800   |
| 7           | Addilyn | 7400   |
| 8           | Juan    | 6100   |
| 9           | Kannon  | 7700   |
+-------------+---------+--------+
Output: 
+-------------+-------+
| employee_id | bonus |
+-------------+-------+
| 2           | 0     |
| 3           | 0     |
| 7           | 7400  |
| 8           | 0     |
| 9           | 7700  |
+-------------+-------+
'''

employees = pl.DataFrame(
    {
        "employee_id": [2, 3, 7, 8, 9],
        "name": ["Meir", "Michael", "Addilyn", "Juan", "Kannon"],
        "salary": [3000, 3800, 7400, 6100, 7700],
    }
)

condition = (pl.col('employee_id')%2 == 1) & (~pl.col('name').str.starts_with('M'))

result = employees.with_columns([
    pl.when(condition)
    .then('salary')
    .otherwise(0)
    .alias('bonus')
]).select(['employee_id', 'bonus'])

# https://leetcode.com/problems/fix-names-in-a-table/description/?envType=study-plan-v2&envId=30-days-of-pandas&lang=pythondata
'''
Write a solution to fix the names so that only the first character is uppercase and the rest are lowercase.

Input: 
Users table:
+---------+-------+
| user_id | name  |
+---------+-------+
| 1       | aLice |
| 2       | bOB   |
+---------+-------+
Output: 
+---------+-------+
| user_id | name  |
+---------+-------+
| 1       | Alice |
| 2       | Bob   |
+---------+-------+
'''

users = pl.DataFrame(
    {
        "user_id": [1, 2],
        "name": ["aLice", "bOB"],
    }
)

fixed_named_users = users.with_columns(pl.col('name').str.to_titlecase())

# https://leetcode.com/problems/find-users-with-valid-e-mails/description/?envType=study-plan-v2&envId=30-days-of-pandas&lang=pythondata

'''
Find valid emails

A valid e-mail has a prefix name and a domain where:

    The prefix name is a string that may contain letters (upper or lower case), digits, underscore '_', period '.', and/or dash '-'. The prefix name must start with a letter.
    The domain is '@leetcode.com'.
Users table:
+---------+-----------+-------------------------+
| user_id | name      | mail                    |
+---------+-----------+-------------------------+
| 1       | Winston   | winston@leetcode.com    |
| 2       | Jonathan  | jonathanisgreat         |
| 3       | Annabelle | bella-@leetcode.com     |
| 4       | Sally     | sally.come@leetcode.com |
| 5       | Marwan    | quarz#2020@leetcode.com |
| 6       | David     | david69@gmail.com       |
| 7       | Shapiro   | .shapo@leetcode.com     |
+---------+-----------+-------------------------+
Output: 
+---------+-----------+-------------------------+
| user_id | name      | mail                    |
+---------+-----------+-------------------------+
| 1       | Winston   | winston@leetcode.com    |
| 3       | Annabelle | bella-@leetcode.com     |
| 4       | Sally     | sally.come@leetcode.com |
+---------+-----------+-------------------------+
'''


users_valid_email = pl.DataFrame(
    {
        "user_id": [1, 2, 3, 4, 5, 6, 7],
        "name": ["Winston", "Jonathan", "Annabelle", "Sally", "Marwan", "David", "Shapiro"],
        "mail": [
            "winston@leetcode.com",
            "jonathanisgreat",
            "bella-@leetcode.com",
            "sally.come@leetcode.com",
            "quarz#2020@leetcode.com",
            "david69@gmail.com",
            ".shapo@leetcode.com",
        ],
    }
)

valid_email_regex = r'^[A-Za-z][A-Za-z0-9._-]*@leetcode\.com$'
valid_emails = users_valid_email.filter(pl.col('mail').str.contains(pattern=valid_email_regex))

# https://leetcode.com/problems/patients-with-a-condition/description/?envType=study-plan-v2&envId=30-days-of-pandas&lang=pythondata
'''
Find patients who have Type I Diabetes. Type I Diabetes always starts with DIAB1 prefix.
Patients table:
+------------+--------------+--------------+
| patient_id | patient_name | conditions   |
+------------+--------------+--------------+
| 1          | Daniel       | YFEV COUGH   |
| 2          | Alice        |              |
| 3          | Bob          | DIAB100 MYOP |
| 4          | George       | ACNE DIAB100 |
| 5          | Alain        | DIAB201      |
+------------+--------------+--------------+
Output: 
+------------+--------------+--------------+
| patient_id | patient_name | conditions   |
+------------+--------------+--------------+
| 3          | Bob          | DIAB100 MYOP |
| 4          | George       | ACNE DIAB100 | 
+------------+--------------+--------------+
'''

patients = pl.DataFrame(
    {
        "patient_id": [1, 2, 3, 4, 5],
        "patient_name": ["Daniel", "Alice", "Bob", "George", "Alain"],
        "conditions": ["YFEV COUGH", "", "DIAB100 MYOP", "ACNE DIAB100", "DIAB201"],
    }
)

diabetic_patients = patients.filter(pl.col('conditions').str.starts_with('DIAB1') | pl.col('conditions').str.contains(' DIAB1'))

