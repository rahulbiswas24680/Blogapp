
# Django Blog (CRUD) Application




## About Project

- [Authentication Sign Up & Login]()
- [Google authentication & Gmail authentication & Github authentication]()
- [Posts order distributed in Category]()
- [Blog post CREATE, UPDATE, DELETE, LIKES, COMMENT, REPLY features]()
- [Pagination]()
- [Author's Post]()
- [User Profile Setup & Update]()
- [User PASSWORD Reset]()
- [Rich text Editor to customize post](https://ckeditor.com/ckeditor-5/)


## Project Screenshots

![App Screenshot](https://via.placeholder.com/468x300?text=App+Screenshot+Here)


## Run Locally

Clone the project

```bash
  git clone https://github.com/rahulbiswas24680/Blogapp.git
```

After cloning the repository, create Virttual Emvironment

```bash
  python3 -m venv <your_env_name>
```

To activate environment on Windows, run:

```bash
<your_env_name>\Scripts\activate.bat
```
On Unix or MacOS, run:

```bash
source <your_env_name>/bin/activate
```

Go to the project directory
```bash
  cd Blogapp
```

Install all the packages from requirement.txt file required to run the application

```bash
  pip install -r requirements.txt
```

Set Database (Make Sure you are in directory same as manage.py)

```bash
python manage.py makemigrations
python manage.py migrate
```

Create SuperUser

```bash
python manage.py createsuperuser
```

Tor run this on browser,

```bash
python manage.py runserver
```
