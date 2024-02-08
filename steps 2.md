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


## Deployment of Mage to GCP
1. Requirements:
    - Google cloud permission
    - Terraform
    - gcloud cli    
    - Terraform templates

2. Cloud permission: Artifact registry reader, Artifact registry writer, Cloud run developer, Cloud sql admin, Service account token creator.

3. Mage terraform templates
```
https://github.com/mage-ai/mage-ai-terraform-templates
```
Now from the relevant repo within template, you can issue terraform commands to create cloud mage in the relevant cloud repo. 
- Access the mage from cloud: Cloud run > Open the relevant service > and get the url for access
- Allow external access of address under Networking ingress control allow (you can also whitelist your specific IP to access the url)

4. Git sync
- You can configure your local Mage and online Mage (cloud) so that changes in the local and online updates are synchronized through git repo.

### Other options for Mage
- Pipelines: stream, data integration
- Alerting
- Triggers and scheduling