# The Book Of Business Recon App
This app is designed specifically to help you perform your repetitive book of business checks. 

Follow the instructions in the sections below to:
- Install the recon app
- Open the recon app
- Create a new recon
- Use an existing recon
- Get support from Mito
    
# Installing the app on a new computer
### Install Python and Git

- If you don’t have Python 3.8-3.11 installed on your computer, install it [here](https://www.python.org/downloads/release/python-3116/).
  - In the installer menu, make sure `Add python.exe to PATH` is toggled on
- Open Command Prompt
- Confirm that you’ve installed Python on your computer by running the command `python –version`
- Install git for windows [here](https://git-scm.com/download/win)


### Set up the Book of Business Checker App

- Open Command Prompt
- Run the following command to navigate to your Desktop
  ```
  cd Desktop
  ```
- Run the following command to download the recon app
  ```
  git clone https://github.com/mito-ds/BookOfBusinessRecon.git
  ```
- Run the following command to navigate to the recon app
  ```
  cd BookOfBusinessRecon
  ```
- Run the command following command to setup the recon app
  ```
  setup.bat
  ```
- Run the following command to open the recon app
  ```
  run.bat
  ```

# Open the app after you’ve installed it

- Open the Command Prompt
- Run the following command to navigate to the recon app
  ```
  cd Desktop/BookOfBusinessRecon
  ```
- Run the following command to open the recon app
  ```
  run.bat
  ```


# Create a new recon

If the book of business that you need to check has a unique data structure from the previous recon automations that you’ve built, you’ll need to create a new recon automation. To do so:

- Open the recon app
- Click on the `Start new automation` button
- [Import](https://docs.trymito.io/how-to/importing-data-to-mito) the two data sources that you want to compare
- [Merge](https://docs.trymito.io/how-to/combining-dataframes/merging-datasets-together) the data sources together by selecting a merge key. The merge key should uniquely identify each row in the dataframe. 
- Create a new column, and use the `=CHECK(column1, column2, [text to display if not matching])` spreadsheet function to compare the attributes from each dataset. 
- Click the `Save Automation` button.

The next time you get similarly structured data (probably from the same provider), you’ll be able to rerun the checks without redoing those steps. See [Reuse Existing Recon Automation](#Reuse Existing Recon Automation) for instructions. 

# Reuse Existing Recon Automation

If you've already used this app to check a book of business from the same provider, automatically perform the same checks by:

- Open the recon app
- Click on the `Use Existing Automation' button
- Select the name of the saved analysis that you want to rerun
- Import the new datasets to compare
- Click run
- [Download](https://docs.trymito.io/how-to/exporting-to-csv-and-excel) the resulting checks as a CSV or Excel file to continue processing. 


# Questions and Help?
Have questions? Want help managing your app or building a new recon? Here are a few resources that you might find useful:
- The [Mito documentation](https://docs.trymito.io) contains an explanation of every piece of functionality available in Mito. If you’re looking to build a new recon and need to do some data cleaning before you compare that datasets, this is a good place to start. In particular you might find useful: [spreadsheet formulas](https://docs.trymito.io/how-to/interacting-with-your-data/mito-spreadsheet-formulas), [filters](https://docs.trymito.io/how-to/filter-data/filter-by-condition), and [column type changes](https://docs.trymito.io/how-to/type-changes). 
- Your Mito customer success manager can always be reached at `aaron@sagacollab.com` to assist you with any questions. 
