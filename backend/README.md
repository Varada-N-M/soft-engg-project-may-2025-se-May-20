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