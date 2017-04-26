# smartbox
Cloud based services are ubiquitous today. 
They are popular, because they offer many advatages to the user, like platform independence of web services and the availability of your own data from anywhere at any time.

However, by using centralized services e.g. offered by Google, Facebook, Amazon or Microsoft, your personal data is given to these companies.

In fact there are many (free software) projects that aim to bring cloud services under your control:

* Owncloud as replacement for Dropbox or Google drive
* An XMPP server as replacement for any centralized messaging system (e.g. WhatsApp, Telegram, Signal, Threema, ...)
* A Mediacenter like Kodi as replacement (or in addition to) Netflix or Spotify
* A Gnusocial or Diaspora pod as replacement for Twitter or Facebook

The reason why so few people use these alternatives could be, that the user has to set up and administrate the server him-/herself.
This is not feasible for most users.

Smartbox is supposed to be a solution here, as it will make it easy to run an own server at home with all sorts of services on it.
It is based on the rkt container engine and will have some interesting features available via the web interface:

* Install services from docker or rkt containers
* Assign dynamic DNS or zeroconf hostnames to the services
* Set up a SSL certificates for publicly available services
* Automate backups (to a classic NAS, encrypted to Google drive or even to another Smartbox)

Check out the build directory to get build instructions.
