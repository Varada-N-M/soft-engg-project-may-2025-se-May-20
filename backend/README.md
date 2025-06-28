

## Local development setup
### Create a virtual environment

```bash
python -m venv env
```

### Activate environment

For Linux
```bash
source env/bin/activate
```
For Windows
```bash
env\Scripts\activate.bat
```
### Install required dependencies
```bash
pip install -r requirements.txt 
```

### Running development server 
```bash
flask --app main --debug run
or
python main.py
```
Default server URL: ```http://127.0.0.1:5000```


## Database Migration
To freshly migrate (delete and recreate) the database tables, run:

```bash
python migrate.py
```

You will be prompted for confirmation before the database is deleted and recreated.

---