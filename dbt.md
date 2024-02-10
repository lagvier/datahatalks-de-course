### Installation
- Ensure python is installed and while using vscode install the following extensions: python, dbt-power-user
- Create a directory and withing it, create and activate a virtual environment.
- install relevant dbt database adapter `pip install dbt-snowflake` -- check others dbt --version

#### Start a dbt project
- Create a `.dbt` folder within your home directory 
- Create a repository where you want to start your dbt project
- From your project folder run the command `dbt init` and follow the prompts to create the project. A `profile.yml` file will be generated in the `$pwd/.dbt` folder

