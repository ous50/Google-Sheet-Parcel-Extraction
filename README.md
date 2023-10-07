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

### For Arch Linux users
If you are using Arch Linux, you can install the required packages using the following command:

```bash
sudo pacman -Syu && sudo pacman -S python-pip python-flask python-requests python-google-api-python-client python-google-auth-oauthlib python-waitress 
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
  --path PATH, -p PATH  Path to the endpoint.
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

### For Users
If you are a user, you can access the follwing url to get the data:

```bash
http://<IP>:<PORT>/<endpoint>?roomNumber=<roomNumber>&bark=<bark>&bark_url=<bark_url>
```

You can also POST json data:

```bash
{
    "roomNumber": <roomNumber>,
    "bark": <bark>,
    "bark_url": <bark_url>
}
```
 For example:
 ```bash
 curl -X POST -H "Content-Type: application/json" -d '{"roomNumber": "b123f", "bark": true, "bark_url": "https://bark.com"}' http://<IP>:<PORT>/<endpoint>
 ```

## LICENSE
[MIT]()

## Disclaimer
This script is only designed for personal use. I am not responsible for any loss caused by the use of this script. Create an issue if you have any questions or found any bug.

## Credits
- [bark](https://github.com/Finb/Bark)

## Author
[ous50](https://ous50.moe)