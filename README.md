# Procore Status
This application can be run via Docker container in Azure to regularly check the
status of Procore's services. When it is detected that a service is down, this
application will scrape a webpage to store information on which services are
down. This content will then be uploaded to Blob Storage in Azure.