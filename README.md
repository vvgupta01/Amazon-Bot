This program was created in IntelliJ PyCharm 2020.1.2 using Python 3.6 and Windows 10.

#### Overview
This program queries and scrapes product information from Amazon.com through the 
Windows PowerShell command-line interface. Features include:
1. Retrieving general product information from search queries.  

2. Tracking individual items for updates and changes.  

3. Saving/emailing results and important item updates.

#### Set Up
##### Required Python Packages
The following external packages are required if using a python environment separate
from the one included: 
`bs4`, `lxml`, `pandas`, `requests`.  

##### Scripts
Change line 10 in `Query.ps1` and `Track.ps1` located in the 
**scripts** directory to the absolute path of the python interpreter `python.exe` 
followed by the absolute path of `Query.py` and `Track.py` respectively.

> If opening the project in PyCharm, the path for the interpreter 
may be **C:/Users/username/PyCharmProjects/Amazon-Bot/venv/Scripts/python.exe**.  
>Then the path of `Query.py` and `Track.py` would be 
>**C:/Users/username/PyCharmProjects/Amazon-Bot/scripts/** followed by the file name.

`Query.ps1` and `Track.ps1` may be moved anywhere outside the project that is more 
easily accessible, such as the Desktop.

##### Paths
Change lines 11 and 12 in `Utils.py` located in the **src** directory to the absolute 
path of the project directory and python interpreter respectively.

> The path for the interpreter should be the same as in the previous section.  
> The path for the project may be **C:/Users/username/PyCharmProjects/Amazon-Bot**.

##### Email
The program requires email credentials in order to send an email from the account to
itself when providing product results or item updates. The most secure method of doing
so is through a Gmail account set up with an [app password](https://support.google.com/accounts/answer/185833?hl=en).  
Change the `EMAIL` and `PASSWORD` keys of the `PARAMS` dictionary on line 9 in 
`Utils.py` to your email and app password respectively. 

#### Running Scripts
To run either `Query.ps1` or `Track.ps1`, open PowerShell and change the working 
directory to the location of the script.

> If both scripts are located on the Desktop in a folder named Amazon-Bot, run 
>`cd Desktop/Amazon-Bot`.

To run scripts, enter `./` followed by the script name and any optional parameters. 

> `./script.ps1 -param1 value1 -param2 value2`

To view all parameters, their default values, and how to use them, run 
`get-help ./script.ps1 -full`  

Generated scripts are located in the **scripts_query** directory and 
**scripts_track** directory for `Query.ps1` and `Track.ps1` respectively. All scripts
may be moved anywhere outside the project that is more easily accessible.  
Generating scripts results in a bash file that can be automated to run at specific
times using [Windows Task Scheduler](https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/schtasks).

##### Querying Products
To query products, run `Query.ps1` followed by the search query and any optional 
parameters. 

> `./Query.ps1 laptop -sort price -ascending $true -pages 3 -limit 50 -email $true`
> retrieves a max of 50 products among the first 3 pages for the search 'laptop', sorts
> them by price in ascending order, and then emails the result.

All results are automatically saved as **.csv** files in the **queries** directory. Due
to how the files names are generated, running the same query within the same minute will
replace the previous file.  
To generate a script, add the parameter `-generate $true`.

##### Tracking Items
To retrieve information for a single item, run `Track.ps1` followed by the full item URL
in quotes.

> `./Track.ps1 'https://www.amazon.com/item_url'`

To actively track a product, enter any optional parameters to generate a script.


> `./Track.ps1 'https://www.amazon.com/item_url' -low 10 -high 20 -change 5 -discount 15`
> sends an email if the price of the item is less than $10, above $20, changes by at 
> least $5, or is at least 15% off. Always sends email if price is unavailable or
> item availability changes.

All results are automatically saved as **.csv** files in the **items** directory. 
Multiple trackers querying the same item will write to the same file.

##### Clarifications
- The list price of an item is its original price, meaning the item is discounted 
if and only if the list price exists. The price is always the current price of the 
item.   
- Items with 0 reviews always have no rating.  
- If the stock of an item exists, it means the stock is low. If it does not, it means
there is sufficient stock or no stock is available.

#### Warning
Excessive querying within a short period of time from the same IP address may cause
Amazon to flag you as a bot and generate a CAPTCHA, preventing the program from querying.
If this happens, the program will automatically attempt to reconnect up to 10 times. If
still unable to query, try again later with different queries/URLs.