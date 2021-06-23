# Extracting unique names from csv file

## Approach

Task of finding unique names was treated as a problem of duplicate names deletion.
In the first step names are normalized by converting names to lower character 
forms, deleting excessive whitespace and deleting dot characters.

Next, dictionary with names as keys and set of alternative ways of writting names 
is created. Alternative forms of name are created by converting name into 
different initials form and deleting hyphen characters.

After that, every combination of name pairs is compared by finding common name
forms in anternative name forms sets. If two names have common item in alternative
forms set shorter name is deleted and longer name is kept back. 

Presented solution can be easily extened by adding new ways of representing names.

Major drawback of this solution is execution time, as every combination of names
has to be compared resulting in very long loop (lasting ~20 minutes on 
mid-level laptop cpu).

If this solution were to be deployed as a service in production environment 
it would be necessary to wrap created script with some server-like 
functionality (eg. by using python library flask) and create a queue system 
for accepting request and serving results upon algorithm completion.

## Running the script
Script is written in python 3, it can be run in virtual environment or
inside Docker container.

### Running in virtual env
#### Prerequisites:
```bash
# creating virtual env
virtualenv .venv --python=python3

# activation virtual env
source .venv/bin/activate   

# installing depencencies
pip install -r requirements.txt 
```

#### Running script:
```bash
python main.py [PATH_TO_INPUT_FILE] [PATH_TO_OUTPUT_FILE]
```

### Running in Docker container
#### Prerequisites:

```bash
# building Docker image
docker build -t unique_names . 
```

#### Running script:

When running inside docker container it's necessary to mount volume for input 
and output files, in the example below `data` directory is mounted inside docker.

```bash
docker run -v $(pwd)/data:/data -it unique_names /data/publications_min.csv /data/names.csv 
```