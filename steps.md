# Docker

### Create docker network
`docker network create pg-network`

### download the docker
```
docker run -it \
-e POSTGRES_USER="root" \
-e POSTGRES_PASSWORD="root" \
-e POSTGRES_DB="ny_taxi" \
-v $(pwd)/green_data:/var/lib/postgressql/data \
-p 5432:5432 \
--network=pg-network \
--name=pg-database \
postgres:13
```

--name=pddatabase \

### install the librariespip 
`pip install pgcli sqlalchemy psycopg2`

## Transfer the data to the postgres using the jupyter notebook

### connect database
```
pgcli -h localhost  -u root -d ny_taxi -p 5432
\dt # show tables
\d <table> # describe a table: column information
select COUNT(1) from green_taxis # count number of records in the database
```

### install pgadmin from docker. 
On another terminal run the command below. After installation access it in localhost:8080 in the browser
```
docker run -it \
-e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
-e PGADMIN_DEFAULT_PASSWORD="root" \
-p 8080:80 \
--network=pg-network \
dpage/pgadmin4
```

Click add new server and provide as provided during postgres installation:
- Under general name input name for it
- Under connections host: input the postgres name (`pg-database`) and respective username:`root` and password: `root` 


### convert the jupyter notebook to script
```
pip install nbconvert -U
jupyter nbconvert --to=script <name_of_notebook.ipynb>
```


### run the script
```
URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-01.csv.gz"
python data2postgres.py \
    --host=localhost \
    --port=5432 \
    --user=root \
    --password=root \
    --db=ny_taxi \
    --table_name=greens \
    --url=${URL}
```

### CREATE Dockerfile with the instructions
```
FROM python:3.9

RUN apt-get install wget
RUN pip install pandas sqlalchemy psycopg2

WORKDIR /app
COPY <script>.py <script>.py 

ENTRYPOINT ["python", "<script>.py "]
```

### Build the docker
`docker build -t <dockername>:<version_number> .`

### Run the docker container with the relevant parameters
```
URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-01.csv.gz"
docker run -it \
    <dockername>:<version_number> \
      --host=localhost \
      --port=5432 \
      --user=root \
      --password=root \
      --db=ny_taxi \
      --table_name=thegreen \
      --url=${URL}
```
--url=https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-01.csv.gz

- You can open the working directory like a webpage with python with `python -m http:server`

##  Docker Compose: connect the containers with YAML file
- This allows concurrent running and communication among the containers.

create docker-compose.yaml file with:
```
services:
  pgdatabase:
    image: postgres:13
    environment: 
      - POSTGRES_USER=root 
      - POSTGRES_PASSWORD=root 
      - POSTGRES_DATABASE=green_taxis
    volumes:
      - "./green_data:/var/lib/postgresql/data:rw"
    ports:
      - "5432:5432"
  pgadmin: 
    image: dpage/pgadmin4
    environment:
      - PGADMIN_DEFAULT_EMAIL=admin@admin.com
      - PGADMIN_DEFAULT_PASSWORD=root
    ports:
      - "8080:80"
```
- Run docker compose: `docker-compose up` or `docker-compose up -d`

- Open the pg admin `http://localhost:8080` and enter create a server with host address being the service specified in the docker compose `pgdatabase`

- Shut down the docker-compose: `docker-compose down`

---

# GCP Services
### Define VM Instances
- From your local machine generate ssh key `ssh-keygen -t rsa -f <FILENAME> -C key-user -b 2048`
- Upload the public key: Compute Engine > Metadata > Paste on the SSH and click save
- Create Instance: Compute engine > VM Instances > Create instance (name, region, machine type, Disk boot disk) and click create
- Note the External IP address.

### Install GC SDK
- Download [Google Cloud SDK](https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe) and install (ensure to check that the installation is added to the PATH).
- Test the installion using the command `gcloud version`
- Check authorize gcloud accounts: `gcloud auth list`
- List cloud storages `gcloud storage ls`


### Connect to the VM
- ssh to the vm using command `ssh -i ~/.ssh/privatekey key_user@ip-address` 
- You can check details of the VM using command `htop`

### Configure
- Ensure you have installed Anaconda on local machine
- Inside the .ssh folder create `config` file (without extension) with the content:
```
Host <Alias-name>
  HostName <GCP_EXTERNAL-IP-ADDRESS>
  User <key-user>
  IdentityFile <full-path-of -key-file>

```
- Now you can just login to the VM using the command `ssh <Alias-name>`
- Now you can install relevant applications eg docker, anaconda, etc

You can also install `remote ssh` extension in vscode to be able to configure and access the VM from the local vscode.

# Teraform
### Install
- Install relevant option from [terraform website)[https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli]. For windows. just put the binary file in a folder and add the path of the folder to the windows environment.

### Create resource and deploy terraform actions
- Enable services to a project: APIs & Services > Library. Then browse and enable relevant services for the project
- On Google console, create a service account for specific services: AIM & ADMIN > service account. Then provide a name for service account and specify the roles.
- You can also edit permission of a service account through edit icon next to the account from IAM & ADMIN page
- Generate access key: From the AIM & ADMIN page, click the three dots next to the account and select manage keys to create and download the key file (json file)
- create `main.tf` file with resource and provider information
- Run the `terraform init` to download the required configurations to access provider resources
- Add more information in the file 
- You can run `terraform fmt` to format and align the information neatly
- Run `terraform plan` check the credentials and information to be deployed
- If everything is ok, run `terraform apply` to deploy 
- If your want to detroy the resource run `terraform destroy`

### Use variables.tf 
- Convert the the information in the `main.tf` to variables eg 
```
variable "bq_dataset_name" {
  description = "test dataset name"
  default = "demo_dataset"
}

variable "location" {
  description = "Project location"
  default = "US"
}
```
- Reference the variable in the `main.tf` eg:
```
resource "goodle_storage_bucket"{
  name = var.bq_dataset_name
  location = var.location
  force_destroy = true

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type="AbortIncompleteMultipartUpload"
    }
  }
}
```





https://www.youtube.com/watch?v=Y2ux7gq3Z0o&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=12

/c/Program Files (x86)/Google/Cloud SDK/google-cloud-sdk/bin

