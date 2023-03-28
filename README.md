Bot Description:

The bot is designed to automatically check the availability of Instagram names on proxy servers. The bot works asynchronously and checks tens of thousands of free proxies for 100 multi-threads at a time. After getting an available proxy, the bot checks the names for availability,
while the first part of the bot continues to search for a proxy. The more available proxies, the higher the speed of operation, it reaches 0.0000+ms. If the name is free, the bot enters it into the dictionary of available names. This also happens asynchronously. After checking for the availability of names, the bot creates a JSON file and renames users by dictionary using Selenium.

The bot starts by downloading a list of free proxies. The bot then uses multithreading to check the proxy for availability using concurrent.futures. After getting an available proxy, the bot uses it to check the availability of Instagram names using the requests library. To speed up the process of checking Instagram names, the bot uses multithreading and divides the list of names into parts of 50. If the name is free, the bot enters it into the dictionary of available names.

After checking all Instagram names, the bot creates a JSON file with information about the available name and login-password pairs from the second TXT file. The bot renames users on Instagram using Selenium. To do this, the bot opens the browser in the background and logs in to Instagram using the transmitted username and password. The bot then renames the users with an available name.

The bot regularly records information about the progress of work in log files to ensure transparency of work and simplify debugging. If errors occur, the bot automatically sends notifications to warn about problems in operation, and continues working with other data.

in open access, I do not fix my earnings, sorry)
