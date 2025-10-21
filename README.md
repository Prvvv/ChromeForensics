# ChromeForensics
Different code samples for Chrome browser analysis &amp; post exploitation

> ChromeForensics should ***NOT*** be used for the purposes of unethical system hijacking or doxxing, and was made with the intentions of security research, pentests and data analysis. Any issues or complaints: prv@anche.no

## Overview & Purpose

These samples are designed for finding and analysing different sources of data extracted from a ***Windows based Google Chrome browser***, the samples listed are designed to fetch and format data from the target systems internal files and locally stored cache.
They are designed for researchers and cyber security professionals to effectively and quickly extract sensitive data from a chrome profile and format them in a timebased, analytical state.

## Samples and usage

![](https://i.ibb.co/8612gMR/chromepost.png)

ChromeForensics samples are capable of harvesting the following data from a chrome profile

### The Browsers Installation & Default state.  
It can detect whether Google Chrome is installed and if it is currently being used as the default browser on the system 

### Profile/User image
It can download the users currently used profile image locally from Chromes cache to the desktop 

### Extentions
What browser extentions the user currently has installed on their Google Chrome profile

### Bookmarks
What bookmarks the user has added on their topbar within the browser

![](https://i.ibb.co/BPTF6b0/bookmark.png)

### Download History
All of the users recent and old download history, including links, timestamps and external sources

### Search History
All of the users search history from within the systems cache and default browser settings including timestamps, urls and visited 3rd party redirects

![](https://i.ibb.co/jhHMZMV/passwords.png)

### Saved Passwords & Login History
All of the users 'kept' site logins, along with password hashes, full urls, timestamps and when the login was created on the system

