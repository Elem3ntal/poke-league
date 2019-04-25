# Poke-League
A Clay's task to discover and use (python) Flask, Celery &amp; MongoDB.

# Use of the *Makefile*

* [install](https://github.com/Elem3ntal/poke-league/blob/master/README.md#install)
* [clean](https://github.com/Elem3ntal/poke-league/blob/master/README.md#clean)

### install
the command install of the makefile runs: 

*install_requirements_system*: this commands ensure that the system fulfill the requirements to host the environment for the app.

*virtual*: first ensure that the system has the capacity to create virtual environments, and then create one.

*install_requirements_python*: once the virtual environment of the app is ready, this command install the specified packages in the file requirements.txt

### clean
cleans ~~(delete)~~ the virtual environment of the app.


# How to run?
well, if all is already installed, just set to run two process.

>celery -A app.celery worker --loglevel=info

>python app.py

# How to request?
all the resources can be consumed as a get or post request. if is a post request in the headers have to set Content-Type as application/json and in the body pass a json with the parameters.

If both ways of consume the resource are in use, first is created all the params from post(body json) variables, and then updates (and create if not exist) the variables that arrive by get.

# Endpoints available

#### _host_/poke-data/update
 <sub>(the procedure is Async)</sub> 

 Brings(and stores) the complete list of pokemons available from the api of pokeapi.co. 
 
| parameters  | value tye |
|:-----------:|:---------:|
| None   |  -  | 
 

#### _host_/poke-data/list
<sub>(the procedure is Sync)</sub> 

Retrieve the list of all the pokemons stored with his names and his moves (if there is any already downloaded)
 
| parameters  | value tye |
|:-----------:|:---------:|
| None   |  -  | 
 

#### _host_/poke-data/update-powers
<sub>(the procedure is Async)</sub> 

With the name of a specific pokemon, start the request to get all the moves/powers (and then stores it).

| parameters  | value tye |
|:-----------:|:---------:|
| name   |  str  |

#### _host_/poke-league/new-league
<sub>(the procedure is Async)</sub> 

With a given name, creates a new league where the contenders can fight.

| parameters  | value tye |
|:-----------:|:---------:|
| name   |  str  |

#### _host_/poke-league/new-contender
<sub>(the procedure is Async)</sub> 

Creates a new contender (with a N numbers of random pokemons) in a specified league.

| parameters  | value tye |
|:-----------:|:---------:|
| league   |  str  |
| contender_name  |  str  |
| contender_pokemons  |  int  |

#### _host_/poke-league/fight
<sub>(the procedure is Async)</sub> 

With a league specified, calculate the result of an encounter of two players based in the combined power of the moves of all his pokemons. And then refresh the enconter stats of each player with his result (that can be: win/lose/draw) 

| parameters  | value tye |
|:-----------:|:---------:|
| league   |  str  |
| player1  |  str  |
| player2  |  str  |

#### _host_/poke-league/friendly-fight
<sub>(the procedure is Sync)</sub> 

Recreate the procedure of a normal fight, but it don't have the constraint that the players have the participate in the same league.

| parameters  | value tye |
|:-----------:|:---------:|
| player1  |  str  |
| player2  |  str  |
   
#### host/poke-league/list
<sub>(the procedure is Sync)</sub> 

Retrieve a list of all leagues with is contenders.


| parameters  | value tye |
|:-----------:|:---------:|
| None  |  -  |

#### host/poke-league/ranking
<sub>(the procedure is Sync)</sub> 

If the parameter 'league' is input, it retrieve a ranking (a sorted list) of all the contenders at the league, if not of all the leagues, sorted by his score in win/draw/lose.

| parameters  | value tye |
|:-----------:|:---------:|
| league*  | str |
_*non mandatory_

