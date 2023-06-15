# instagram-scrape
Instagram Scrape is a Python-based web scraping project that allows you to extract information from Instagram posts, including likes count, image, text, and published day. It utilizes Selenium for automated web browsing and interacts with Instagram's web interface.

## Installation and Setup

**1. Clone the project:**  
$ git clone https://github.com/tim646/instagram-scrape.git  
**2. Set up .env file.**    
 use .env.example file  
**3. Create venv file and install packages**  
$ python3 -m venv venv  
$ source venv/bin/activate  
$ pip install -r requirements/develop.txt  
**4. Configure Python Interpreter**  
**5. Apply migrations**  
$ python3 manage.py migrate
## Set up Instagram login credentials
**1. Create Super User to login to admin panel**  
$ python3 manage.py createsuperuser  
**2. Enter Instagram username and Password. and Target Username**  





![Screenshot from 2023-06-15 16-04-35](https://github.com/tim646/instagram-scrape/assets/91428417/a12210f9-6f5b-4ade-bc41-f4ae5e285eec)

## Run the Celery worker

**$ celery -A core/config worker --beat -l info**    
