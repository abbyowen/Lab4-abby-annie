# LAB 4 - Abby Owen and Annie Revers

### TO RUN
`python3 blog_cli.py`
* From here you can provide stdin inputs. 

### TESTING (MAIN FUNCTIONALITY)
`python3 blog_cli.py < testfile1.in > grader.testfile1.out 2>&1`
* Since our data is already added, we will have to drop the tables in order to reproduce the `testfile1.out` file as these tests were made when the database was completely empty. **BEFORE COMPARING TESTING FILES**, run `python3 blog_cli.py` and input the command `clear` to remove all info from the tables.
* This will write the output of our test file to a file for grading

### TESTING (EXTRA CREDIT)
* Run the first testing file first to add sufficient data needed for testing as our tests rely on some previous data.
* `python3 blog_cli.py < extracredit.in > grader.extracredit.out 2>&1`

#### Notes on the timestamp feature
We provide the option of providing a timestamp for a given action or autogenerating one. For the sake of our testing files, we create our own timestamps and supply them. This way, we can control what comes out in our out file. 