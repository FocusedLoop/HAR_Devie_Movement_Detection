"python har_device_classifier.py" in the terminal to start the program
<br /><br />Setup:
<br />Input the desired model

<br /><br />Once in use:
<br />Device will start detecting movement
<br />Should print one of the 4 movement types; running, walking, situps or rest

<br /><br />CRTL+C to kill the program after use (should exit without an error)



"python har_device_data_collection.py" in the terminal to start the program
<br /><br />Setup:
<br />Input your session User - Your name
<br />Input your session ID - Number of times you have performed a movement actvity (to differentiate between entries easily if there is an issue)
<br />Input the performed movement type - The movement type you are going to perform; running, walking, situps or rest

<br /><br />During device validation:
<br />Skip - Input "y" to skip or "n" to start validation
<br />LED TEST - LED Should start blinking
<br />SENSOR TEST - The current time as well as x, y and z values from the sesnor should printed
<br />NOTE - If any of the following are not functioning as stated above then the device is NOT working

<br /><br />Once in use:
<br />Press button to start the session, after which movement data will begin being recorded
<br />Press button again to end session

<br /><br />Session Instructions:
<br />The following items below MUST be recorded for time you use the device
<br />The session ID - Number of times you have performed any movement activity
<br />The movement performed for that session - This is a backup incase the MongoDB has the incorrect movement type
<br />Time of each session - Each activty should add up to 10 minutes in total (More may be need, this will be discussed depending on how the next 2 weeks go)

<br /><br />Errors:
<br />Once a session starts the LED should be always be ON unless the session has ended (button has been pressed again)
<br />OFF LED - There is something wrong with the device or the sesnor
<br />BLINKING LED - The device has lost connection to the MongoDB (check internet connection or there is an error with the database itself)

<br /><br />CRTL+C to kill the program after use (should exit without an error)
