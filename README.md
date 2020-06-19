# Tweeter

Tweeter is a web application for interacting with twitter in a more data driven way

## Getting Started

### Using Docker for development
1. Clone or fork this repository
2. Create a new .env file based on the .env.example file
   - Don't change any of the postgress variables
   - If you want the sentiment analysis to work, put your twitter credentials in the last four variables
2. Make sure docker is running and run the command `docker-compose up -r --build`
3. Once the above command is completed, run `docker-compose exec db psql --username=tweeter`
4. Now at the tweeter postgress shell, type in `create extension hstore;` (the ';' is required)
5. Once you get the response "CREATE EXTENSION" back, quit the shell using `\q`
6. Then run `docker-compose exec web python manage.py migrate --noinput` to make django migrations
7. If that is completed successfully, go to localhost:8000 in your browser of choice (I have been using chrome)

## Usage

### Live Application
Go to the app [here](https://tweeter-v2.herokuapp.com/)

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change. 
You can also create your own generator, if there's space left. Just go to the websitre and find the create generator tab.
