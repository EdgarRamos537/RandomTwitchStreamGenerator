# Random Twitch Stream Generator
Webapp that finds a random Twitch stream.

## Installation
To use app either access website, locally install, or run with Docker. From there click the _Find Random Stream_ button to generate a URL to a currently live Twitch stream. Adjust options if needed to fit your perfereneces.

<details>
  <summary>Website</summary>
  Link: https://random-twitch-stream.herokuapp.com/
  
  - Hosted using [Heroku](http://www.heroku.com)
</details>

<details>
  <summary>Local Installation</summary>
  
  1. Clone the repository 
  ```shell
  git clone https://github.com/EdgarRamos537/RandomTwitchStreamGenerator.git
  ```
  2. Change current directory 
  ```shell
  cd RandomTwitchStreamGeneratorTest
  ```
  3. Install requirements
  ```shell
  pip install -r requirements.txt
  ```
  4. Run main.py
  ```shell
  python main.py
  ```
  5. Open http://localhost:5000
  
</details>
<details>
  <summary>Run with Docker</summary>
  
  1. Clone the repository
  ```shell
  git clone https://github.com/EdgarRamos537/RandomTwitchStreamGenerator.git
  ```
  2. Change current directory
  ```shell
  cd RandomTwitchStreamGeneratorTest
  ```
  3. Build Docker image
  ```shell
  docker build -t random_twitch_stream .
  ```
  4. Run app
  ```shell
  docker run -it --rm -p 5000:5000 random_twitch_stream
  ```
  5. Open http://localhost:5000
</details>



## Usage
Click on _Find Random Stream_ to generate a random Twitch stream URL. Adjust the options for more personalized results. __It is highly suggested to, at the very least, include a language when searching.__
  
| Option  | Description |
| ------------- | ------------- |
| Language | Select a Language from the list. Only streams that have their primary language for streaming set to the selected language will appear. _Defaults to All._ |
| *#* of Top Game(s) | Numeric value ranging from 1-200. Only streams from the Top N Games on Twitch will appear where N = the number entered in the field. "Only include game(s) in search" takes precedence over this option. _Defaults to 200._ |
| Only include game(s) in search | Type the name of the game(s) exactly as they appear on Twitch to search only for streams that are playing those games. Separate each game name with a single ",". For games that have "," included in their names (e.g. Animals, Aquariums, and Zoos) place "" around the name. |
| Exclude game(s) in search | Type the name of the game(s) exactly as they appear on Twitch to exclude any streams that are playing those games. Separate each game name with a single ",". For games that have "," included in their names (e.g. Animals, Aquariums, and Zoos) place "" around the name. |
| Family Friendly | Check to enable only Family-Friendly streams to appear. __This may significantly slow down request time.__ |
| Charity Streams | Check to enable only Charity streams to appear. __This may significantly slow down request time.__ |
| Closed Captions | Check to enable streams with the Closed Captions tag to appear. __This may significantly slow down request time.__ |
| V-Tuber | Check to enable only streams with the _Vtuber_ tag to appear. |
| No Sponsored Streams | Check to disable any streams that have "#ad" in their title from appearing. |
| Custom Tag | Enter a Tag ID into the text box to search for only streams with that tag. The Tag ID of a tag can be found by going to the [Twitch Browse Live Channels](https://www.twitch.tv/directory/all) page and selecting the desired tag in the search bar. The Tag ID will be the last part of the URL. Please note that this feature only works with Stream Tags and not Game Tags. |
| Min Viewers | Numeric value with a default = 0. Must be less than Maximum Viewer Count |
| Max Viewers | Numeric value with a default = 9999999. Must be greater than Minimum Viewer Count. |

## License
