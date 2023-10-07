# Google-Sheet-Parcel-Extraction
Check your parcels listed in Google Sheet and return a msg.

This script is used to check the parcels listed in Google Sheet and return a msg.
To use this script, you need to have a service account token and a Google Sheet ID.
If you don't know how to get them, please refer to the following links:
- [Google Sheet API](https://developers.google.com/sheets/api/quickstart/python)
- [Google Service Account](https://cloud.google.com/iam/docs/creating-managing-service-accounts)

## Installation
1. Clone this repository

```bash
git clone https://github.com/ous50/Google-Sheet-Parcel-Extraction.git
```

2. Install the required packages

```bash
pip install -r requirements.txt
```

3. Put your service account token in the same directory as the script and rename it to `service_account.json`. This script only uses the `service_account.json` file to get the credentials and will only use read-only access to publically shared Google Sheets.

4. Put your Google Sheet ID in the `config.json` file


## Usage
Run the script

```bash
python main.py 
```

You have the option to run the script:

```bash
  --port PORT, -P PORT  Port to run the backend on.
  --host HOST, -H HOST  Binding IP.
  --debug DEBUG, -D DEBUG Run in debug mode.
```

If you want to run the script in the background, you can use the following command:

For Linux/MacOS:
```bash
nohup python main.py 
```

For Windows:
```bash
pythonw main.py 
```

If you want to run the script in the background and log the output, you can use the following command:

For Linux/MacOS:
```bash
nohup python main.py > log.txt &
```

For Windows:
```bash
pythonw main.py > log.txt &
```

You can also run the getmsg.py script to get the data without starting API server.

```bash
python getmsg.py <-R room> <-B>
```

## 

## LICENSE
[MIT]()