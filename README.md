# Line-BOT-member-registration
Line BOT for member registration and manage by user roles via store status in databases

## Requirements & Dependencies
Libraries Needed: <br>
- MySQL <br>
- Python 3.6 <br>
- pip install line-bot-sdk <br>
- pip install falsk* <br>
- pip install mysqlclient <br>
- pip install oauth2 <br>
- pip install gunicorn <br>
- pip install request


## Features

- member registration -> verify by LINE uid <br>
- member auto assign role for push different Ads -> different role store on MySQL <br>
- Role: sales/doctor <br>


## Command Examples and Flows

- doctor
  - Welcome Dr. $NAME 
  - Not registered yet, Please Enter your Name
    - Please Enter E-mail
      - Registered, Welcone Dr. $NAME
        - Push Ads which for Doctors
 - sales
   - Welcome $NAME
   - Not registered yet, please Enter your Name
     - Please Enter E-mail
       - Registered, Welcome $NAME
         - Push Ads which for sales


## Tips

Bacause Line SDK doesn't accept multiple command, so need to check status which store in database to verify.
