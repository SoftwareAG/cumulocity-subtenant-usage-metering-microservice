# cumulocity-subtenant-usage-metering-microservice


This project is an microservice that requests tenant statistics for all its subtenants and historicizes them as measurements. It therefore creates a device for ecery subtenant. With that approach it can be monitored on a timeseries bases what happens in the subtenants. Furthermore e.g. Smart Rules or Analytics Builder can be used to alert due to certain usage behaviours.

# Content
- [cumulocity-subtenant-usage-metering-microservice](#cumulocity-subtenant-usage-metering-microservice)
- [Content](#content)
- [Quick Start](#quick-start)
- [Solution components](#solution-components)
- [Installation from scratch](#installation-from-scratch)

# Quick Start
Use the provided zip here in the release and upload it as microservice.

![Upload](/resources/upload.png)

# Solution components

The microservice consists of 4 modules and a main runtime:
* `run.py`: Main runtime that opens an health endpoint at /health and also triggers the request of  statistics including persisting it as measurements
* `API/authentication.py`: Contains the Authentication class that requests the service user via the bootstrap user from within the microservice environment. See [documentation](https://cumulocity.com/guides/microservice-sdk/concept/#microservice-bootstrap) for more details.
* `API/inventory.py`: Consists of the logic to deliver the internalId of the device representation of the subtenant or creates the device if a new subtenant appears. Currently the externalId is set as the tenantID. The name of the device representation of its particular subtenant is chosen to be {domain-name} - ({tenantID}).
* `API/measurment.py`: Creates the measurement payload from the statistics retreived from API and sends it to Cumulocity.
* `API/statistics.py`: Delivers statistics for all included subtenants via the following REST-API endpoint: /tenant/statistics/summary. See [openAPI description](https://cumulocity.com/api/10.11.0/#operation/getSummaryAllTenantsUsageStatistics) for more details about that.

Currently the sheduled request for statistics is set to be 900s which equals 15 minutes. Debug Level is set to be INFO. Feel free to adjust the resolution but keep in mind that a device is created for every subtenant as well as a certain device class is associated with that.

# Installation from scratch

To build the microservice run:
```
docker buildx build --platform linux/amd64 -t {NAMEOFSERVICE} .
docker save {NAMEOFSERVICE} > image.tar
zip {NAMEOFSERVICE} cumulocity.json image.tar
```

You can upload the microservice via the UI or via [go-c8y-cli](https://github.com/reubenmiller/go-c8y-cli)

![Measurements](/resources/measurements.png)


------------------------------

These tools are provided as-is and without warranty or support. They do not constitute part of the Software AG product suite. Users are free to use, fork and modify them, subject to the license agreement. While Software AG welcomes contributions, we cannot guarantee to include every contribution in the master project.
_____________________
For more information you can Ask a Question in the [TECHcommunity Forums](http://tech.forums.softwareag.com/techjforum/forums/list.page?product=cumulocity).

You can find additional information in the [Software AG TECHcommunity](http://techcommunity.softwareag.com/home/-/product/name/cumulocity).
