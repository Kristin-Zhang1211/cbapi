# cbapi
With Crunchbase API, the script is trying to download the information about the organizations and people that we need automatically and the output of those information is stored in a pd.DataFrame

# the main functions
```
import cbapi

org = org_data(name='capital management', organization_types="investor")
people = people_data(name='taylor', locations='New York')
```

# install the package
Install cbapi using pip:
```
pip install git+https://github.com/Kristin-Zhang1211/cbapi.git
```

# requirement
```
Python
Pandas
Json
Requests
```
