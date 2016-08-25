==================================================================
STEPS TO RUN APPLICATION
==================================================================

1) Run pip install -r requirements.txt
2) If you want to start with clean database
    a) open python shell in project directory
    b) execute 'from app import db'
    c) execute 'db.create_all()', which will create neccessary tables and db files
3) After setting up database run 'python app.py': It will have application ready, which can be accessed at
    http://localhost:5000


IMPORTANT NOTES:
1) Instead of providing explicit search button I provide search box which will search appointments with description,
       I implemented it more like instant search
2) I used few more libraries for date picker, time picker to make it look good


