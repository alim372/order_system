**Order System** 
APIs built using Django and Django Rest Framework


please install requirements using this command before start
using this command
**" pip install -r requirements.txt "**

there are two permission:


**-administartor**
to create user with administrator's permission use the command of 
(python manage.py createsuperuser)
and then use login endpoint with the inserted credintials to get the token and use it 

**-user**
to create normal user please use register endpoint

-----------------------------------------------------

important notes :


**User model:**
-the initial django auth User model was overrided and replaced with custom User model 
also i have replace create_superuser function with another customized one in Custom User Manager class 

**soft delete :**
-when apply delete product end point the will not appear to users anymore
but it is still exist in database, there is state attribute in table products which would be 'deleted' if the user delete item 
this step is important for recovery and more reasons 
so i used SoftDeleteManager which help to do that. 

**transaction.atomic:**
-this help to roleback if there is any error occure before finishing the function

**Swagger:** 
-all APIs is documented using swagger 
so you can check 
http://localhost:8000/doc/ 
or 
http://localhost:8000/redoc/
to know more about each endpoint 
don't forget copy and past token in authorize and also don't forget write word "token" before the token which you can get from login endpoint 

**testing** 
to know more about unit and integration testing use this command 
**"python manage.py test"**
and check this file to know more about each test case **'test-cases.txt'**

**Currancy**
the base currancy is EUR because the fixer is free just when request the most recent exchange rate data
and need to upgrade for use conversion api
so i make the conversion manually
