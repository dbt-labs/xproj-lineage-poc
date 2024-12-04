# ***Archival Notice***
This repository has been archived.

As a result all of its historical issues and PRs have been closed.

Please *do not clone* this repo without understanding the risk in doing so:
- It may have unaddressed security vulnerabilities
- It may have unaddressed bugs

<details>
   <summary>Click for historical readme</summary>

# xproj-lineage-poc
POC for a DAG of projects using the Discovery API

## Usage 

1. Create a python virtual env and activate it
2. Set env vars:
   1. DBT_API_TOKEN (required) - token for hitting discovery API
   3. DBT_ACCOUNT_ID - dbt Cloud Account ID to analyze
   2. DBT_ENV_ID (required) - dbt Cloud Environment ID for model-level information
   4. DBT_METADATA_URL (optional) - metadata API url (defaults to beta URL)
3. Install dependencies
```
pip install --upgrade pip
pip install -r requirements.txt
```
1. Run the app
```
streamlit run home.py
```


