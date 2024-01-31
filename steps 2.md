# Orchestration

Automation of sequential processes eg ETL: triggering, monitoring

## Mage
### Configure Mage
- Install or update Mage `docker pull mageai/mageai:latest`
- Clone the mage docker project 
- Create the env file `cp dev.env .env`
- Build the docker project `docker compose build`
- Run the project `docker compose up`
- Access the project on "http://localhost:6789"

### Configure postgres
create pipeline block and 


### Connect to GCS
- Edit the GOOGLE_SERVICE_ACCOUNT_KEY_PATH the io_config.yml file to access the key file in the `/home/src/<path to file>`
- 