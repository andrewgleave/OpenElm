#Open Elm Project
[http://www.openelm.org.im/](http://www.openelm.org.im/)

*Andrew Gleave, [Red Robot Studios Ltd](http://www.redrobotstudios.com/)*

The [Open Elm Project](http://www.openelm.org.im/) is a public crowdsourcing initiative to collect data on the Elm tree population of the Isle of Man and help track and tackle increasing outbreaks of Dutch Elm Disease. The Island is one of the few places left in the UK which have a healthy population (unlike England which lost 23 million trees between 1960 and 1988), and the with the public's involvement, we hope to keep it that way.

##Source

We've distributed the full source for both the site and mobile apps under the GPL v3 (see license.txt). Artwork, images and other media is not covered under this license and cannot be reused for other purposes.

###Site
The site is a standard Django app which makes use of [Celery](http://celeryproject.org/) to handle distributed tasks, such as handling the media uploads and pushing the media to S3. You should be able to clone the project and run the app if you have the necessary dependencies installed.

###Mobile Apps
The mobile apps are built with [jQuery Mobile](http://jquerymobile.com/) and wrapped for iOS and Android with [PhoneGap](http://www.phonegap.com/). We chose to build the apps using HTML5 to increase the chance that other developers may could deploy the app to other platforms. 

Essentially, these apps are reference implementations, and native versions would give improved performance, features and reliability. Initial funding precluded building native versions for iOS and Android, but any interested developers could build a native version for any platform if they want – the data and API is fully exposed, and you would just need to ask me to create an account so the app could save to the CouchDB database.

###Database
This project uses CouchDB to store records. CouchDB is not a standard RDBMS, and is best described as a non-relational document store. The project's database is located at [http://redrobot.couchone.com/_utils/database.html?openelm](http://redrobot.couchone.com/_utils/database.html?openelm). The great thing about CouchDB is that there is no API middleware – the database is the API. I'd encourage you to take a look at CouchDB in detail if you're interested in accessing the data: [CouchDB the definitive guide](http://guide.couchdb.org/) is a good place to start.


#Credits

All the contributors of: the [Django Project](http://www.djangoproject.com/), [CouchDB](http://couchdb.apache.org/), [CouchOne/Iris Couch](http://www.iriscouch.com/), [CouchDBKit](http://couchdbkit.org/), [Celery](http://celeryproject.org/), [PhoneGap](http://www.phonegap.com/) and [jQuery Mobile](http://jquerymobile.com/).

If you're interested in contributing to the project please get in touch.
