# python-test-project
Flask API that allow uploading an Excel file and returns a summary of provided columns

## How to run

1. Go to the cloned project main directory and create a virtual environment

```
python -m venv ./venv
```

2. Activate virtual environment

On Windows, run:
```
.\venv\Scripts\activate.bat
```

On Unix or MacOS, run:
```
source ./venv/bin/activate
```

3. Install dependencies by `setup.py`

```
pip install python_test_project
```

4. Run flask application

```
python main.py
```

## Docker

You can also use Docker to run the application.

1. Go to the directory with `Dockerfile` and create docker image

```
docker image build -t flask_test_project .
```

2. Run docker image

```
docker run -p 5000:5000 -d flask_test_project
```

## Documentation

The app will by default run on `http://localhost:5000`. You can check documentation and test API by visiting `http://localhost:5000/apidocs/`.
