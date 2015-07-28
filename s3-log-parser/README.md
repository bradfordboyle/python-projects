s3-log-parser
=============

For static sites hosted on AWS S3, using the built-in logging feature results in
a collection of log object/files in a separate bucket. In addition to web views,
logs are also generated for other non-HTTP events. This script collates the
separate log files in a **local** directory and applies some useful filters
before geolocating the visitors the host site.
