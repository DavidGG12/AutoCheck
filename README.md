# Auto Check

This project is to help me to enter my in-hour and out-hour of my job. An automatized task when i sign in my computer.

We need to install the next libraries:

- Selenium
- PyWin32
- SQLite3

```cmd
pip install selenium

pip install pywin32

pip install sqlite3
```

All configuration of settings to extract user, worker number or ID (however you know it), url to enter the hour, etc. We need to create a file .json with the name "appsettings.json" with the next structure:

```json
{
    "Url": [Url you need],
    "Browser": [Browser that you going to use for the bot],
    "Services": [
        {
            //If seleniun can't download the service to the driver of seleniu of the browser you want to use, you need to fill this object.
            [Name of yout browser in Upper case]: [Local path of the service]
        }
    ],
    "Users": {
        "SessionUser": [Name of PC user],
        "WorkerNumber": [Worker Number or ID] 
    }
}
```