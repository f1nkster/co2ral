## Open Points

* Download values as csv
* Sharable URL
* Nutrients to add: Ammonia: 0 - 1


# Deployment
CO2RAL is using waitress for the WSGI app and nginx for the webserver.
Linux service is defined in /etc/systemd/system/co2ral.service

How to check the status: ```sudo systemctl status co2ral```
How to stop: ```sudo systemctl stop co2ral```
How to start: ```sudo systemctl start co2ral```
Show logs: ```sudo journalctl -u co2ral```
