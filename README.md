# Resale HDB Data Analysis Tool

**Steps to set up the project:**
1. clone project:  
```git clone https://github.com/hanyi97/data-analysis-resale-hdb.git```

2. checkout remote develop branch:  
```git checkout origin/develop```

3. create and checkout feature branch:  
```git checkout -b feature/<featurename>```

4. push your feature branch to GitHub:  
```git push -u origin feature/<featurename>```

**Basic workflow:**
1. Create and checkout new feature branch  
```git checkout -b feature/<featurename>```

2. Code and test your feature  

3. Add your changes to the feature branch (best practice to add the files that you modified only)  
```git add <file name>```

4. Commit your changes  
```git commit -m “<commit message>”```
or
```git commit``` Press enter and type the summary and description for the commit. Then press esc and type :wq  

5. Push your changes to Github  
```git push```

Once the feature is completed, merge it to develop branch:  
6. Checkout develop branch  
    ```git checkout develop```
7. Merge your feature branch to develop branch  
    ```git merge <featurename>```
8. Delete local feature branch  
    ```git branch -d <featurename>```
9. Delete remote feature branch  
    ```git push origin --delete <featurename>```

Note: Best practice to commit your changes regularly

Naming conventions: 
Git branches:  
gui/main-menu  
feature/export  
feature/filter  
feature/bargraph

Code:  
Variables, Function and Module names to be lowercase and separated by “_”.  
csv_helper.py  
get_data()  
my_variable
