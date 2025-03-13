# Simple Record Register Scheduler
How to run: download/save this repository in your local pc. Then do the following to get started:

1. Run the Generate_dataset.ipynb, This is where you dataset will be created.
2. Run the first block in Sql_database.ipynb, skip the second block. the first block will create a local database to test the functions on.
3. Run "run_scheduler.py" in the terminal with the commmand: python run_scheduler.py
4. End

  
In most cases you can leave the Update_code_logic.py as it is if you dont have any specific changes you want to to (of course you are welcome to experiment!)


In this repositoy I have worked on creating a simple register scheduler that updates sql database table with new data from a csv file and logs the changes made to the table. it register peoples name, age and city. With a scheduler to automate the operations, the library used for the scheduler is named "schedule".
