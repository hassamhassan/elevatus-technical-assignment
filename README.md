# Elevatus Technical Assignment

## 🧩 Features

+ Python
+ FastApi
+ Async MongoDB
+ Poetry
+ Pydantic
+ Pytest
+ Docker
+ PreCommit Hooks
+ JWT Authentication


## 🚚 Clone the repository
```shell
git clone git@github.com:hassamhassan/elevatus-technical-assignment.git
```

## 📦 Setup Docker Environment
```shell
cp .env.sample .env
docker compose build
docker compose up -d
```

## 🏗️ Local Setup without Docker
#### 1. create virtual environment
```shell
cd elevatus-technical-assignment
python -m venv venv
source venv/bin/activate
```

#### 2. Install requirements
```shell
bash ./setup.sh
```

#### 3. Create `.env` file in the root directory
```shell
cp sample.env .env
```
Update the MONGODB_URL environment variables to this `mongodb://localhost:27017/`.

#### 4. Start the application:
```shell
bash run.sh
```
The server will be accessible [here](http://0.0.0.0:8000) and swagger docs [here](http://0.0.0.0:8000/docs) 😎.


## 🧪 Run test cases
```shell
pytest
```
