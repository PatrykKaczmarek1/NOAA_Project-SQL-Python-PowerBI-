# NOAA-Project

## Project Overiew
Goal of this project is to create a report showing a general overview of weather stations around the globe.
Report will provide key insights regarding stations location and data coverage.

### Programming Languages and Tools

To complete the project I used Python and T-SQL as programming languages and Visual Studio Code, Azure and Power BI as tools.

### Project Plan
1. Creating an API connection in Python to retrieve the data from the NOAA site.
2. Creating database in Azure SQL to store the retrieved data.
3. Connecting Azure SQL to Power BI and creating an report.

### Python Script
NOAA_API_and_Azure_upload is designed to fetch weather station data from the NOAA API and store it in an Azure SQL database. It's a straightforward solution for automating data retrieval and storage.
The script starts by reading API credentials and database connection details from a local file. This keeps sensitive information secure and separate from the main code. 
It builds a URL to request data from the NOAA API and uses pagination to handle large datasets - it loops through the API responses, fetching data in parts (1000 per response) until all records are retrieved.
All the retrieved data is then organized into a list, ready to be stored in a database in Azure to which script connects using the pyodbc library.
Libraries Used: requests for API interactions and pyodbc for database connectivity.

### SQL Queries
First table was created basing on the quick analysis of the data from NOAA. After first upload I detected several issues with data types using basic commands like WHERE, ORDER BY, GROUP BY.
Based on the queries result 'Stations' table was created with columns having proper data types. Data analysis also revealed two types of units used in data - foot and meters, so another query was made to harmonize the units.
Last query was used to pull the data into Power BI.

## Result

![NOAAreport](https://github.com/user-attachments/assets/2532a920-46a2-4dcb-b430-657959e0b6cb)

### Possible improvements
1. NOAA data assigns stations to an country key which is used as a basis for a "Continent" slicer. This may result in confusion ie. when selecting "North America" and seeing stations from Asia.
Solution: This could be solved by comparing the latidude and longitude of a station to a latidude and longitude of a continent. This should be done in SQL or Python to follow the general rule of solving the data issues upstream.
