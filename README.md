# Chess Minigame

Chess Arena is a fullstack web app that allows users to login, play chess games against the computer, and view their own profile.

## Installation

Fork this repo, then copy the SSH link for your forked repo, and type "git clone 'SSH link'" into your terminal in your desired directory. Once on your local machine, open the terminal and type "pipenv install -r requirements.txt" to create the virtual environment with the necessary packages (make sure you have pipenv installed (pip install pipenv --user) before running the pipenv command). Then open the instance of the environment using "pipenv shell". Then cd into the frontend folder "cd frontend/" and type the following command "npm install". Then open a second terminal and cd into the backend folder "cd ../backend". At this point you should have a terminal in the frontend and the other in the backend folders. Run the folloing in the backend terminal:

 - "python manage.py makemigrations"
 - "python manage.py migrate"
 - "python manage.py runserver"

 Then in the terminal, copy the http address and paste it into the .env file in the frontend folder in this format "VITE_API_URL="http://000.0.0.0:0000/"". Finally type the following command in the frontend terminal "npm run dev" and open the url in a browser.

## Usage

The Chess Arena allows a user to create an account and play against an AI bot. Once logged in, a user can start a new chess game against the AI.

## Sample GIF of Application

![CLI Chess Minigame Demo](./lib/videos/video2992411945.gif)

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Roadmap

I plan on eventually adding the capability for the computer to change difficulty. 

Also I am planning on adding the capability for the user to be a color other than white.

## License

[MIT](https://choosealicense.com/licenses/mit/)