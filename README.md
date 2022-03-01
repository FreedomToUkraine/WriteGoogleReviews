This software has been created only to help Ukraine.

To automatically write reviews on google:

1. Clone the repository
2. Make sure that under C:\Program Files\Mozilla Firefox\firefox.exe is Mozilla Firefox executable
3. Run the script: python app.py
4. If the Mozilla does not launch please check step 2 and make sure that the geckodriver is compatible to your Mozilla's Version.
   You can download the proper version here: https://github.com/mozilla/geckodriver/releases.

   When the Mozilla opens properly the script will be looking for restaurants/hotels in cities listed in data.json

   Sometimes the script misses some reviews but when it finally finds the first one you will be prompted to login to your google account. You have 20sec for that.
   If everything works correctly you can leave the program running for 24h/7 and keep informing the Russian people about the situation.

Please remove a few cities form the data.json and try to start from another letter than 'A'. It will speed up reviews publishing.

You can adjust the message in under 'write_review' function.
