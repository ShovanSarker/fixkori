# Fixkori (Prototype)

This is the prototype for a startup called fixkori. The purpose of building this application to provide the user fixing or maintaining service at doorsteps. User can make service order to the portal mentioning the type and other details information and the requests sent to admin. After assigning the order to the suitable vendor, the vendor can directly communicate with the user.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install required libraries.

```bash
pip install -r requirements.txt
```
or installing the required libraries manually by 
```bash
pip install Django
```

## Usage
After the required libraries installed, go inside the project directory and check if the ```manage.py``` file is there. If it is there run the following code:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```
these commands will update the database structure(if necessary) and run the service on [localhost](http://localhost:8000) on 8000 port.

## License
[MIT](https://choosealicense.com/licenses/mit/)
