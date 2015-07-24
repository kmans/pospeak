[![Build Status](https://api.travis-ci.org/kmans/pospeak.png)](https://travis-ci.org/kmans/pospeak)


# po/Speak
#####po/Speak is a mobile-first, instanced chat service engine specifically targeting users on limited data connections.
#####It is built for the modern web, and works best on mobile devices running modern browsers. 
<br>
The goal of this project was to create a way for people to communicate in groups without having to download an application or be tied down to a specific mobile device.

#####Any suggestions or ideas on how to improve this very alpha build of po/Speak are much appreciated!
#####tweet me [@supermansuri]
<br>
### Version
v0.11 - July 2015<br>
v0.1 alpha - June 2015

### Open Source Projects used in po/Speak

* [Flask] - Python Framework for getting all of this working
* [Twitter Bootstrap] - for mobile/responsive design (HTML/CSS)
* [jQuery] - for some of the animations
* [gunicorn] - recommended WSGI Server
* [nginx] - recommended HTTP proxy
* [jenkins] - wonderful CI tool

### Installation/Usage
#####po/speak has been tested on Python 2.7.10

- *set a SECRET_KEY in the config.py file*
- *change DEBUG = False in config.py file if not testing*
- ```pip install -r requirements.txt```
- ```python run.py```
- *test it out on localhost:5000*

###Changelog/Future Updates

#####Changelog
  - v0.11 - Fixed Python3 compatibility, fixed user sign-off bug


#####Fixes coming in next update
  - Correctly authenticate users and send verification token emails
  - Publish unit tests

#####Fixes coming in future updates
  - Implement websockets to replace POST requests
  - Move over to using Postgres, and use memcache to handle session data

###Attribution and Licensing
#####**po/Speak is licensed under the GPL v3.0 <gpl-3.0.txt>**
#####**(c)2015 Kamil Mansuri**
#####**[@supermansuri]**
<br>
#####Flask is licensed under the BSD license
#####gunicorn is licensed under the MIT license
#####tinyurl algorithm is based on the work of Michael Fogleman and is licensed under the MIT license

[Flask]:http://flask.pocoo.org/
[gunicorn]:http://gunicorn.org/
[Twitter Bootstrap]:http://twitter.github.com/bootstrap/
[jQuery]:http://jquery.com
[@supermansuri]:http://twitter.com/supermansuri
[nginx]:http://nginx.org/
[jenkins]:https://jenkins-ci.org/
