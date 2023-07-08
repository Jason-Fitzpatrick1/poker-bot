# Welcome to the NEAT Poker Bot!

This project contains three modules: **poker**, **neat** and **test**. 

The **poker** module consists of an OOP Texas Holdem simulation, designed to be played by bots. *Note: There is not visualization for the poker game.*

The **neat** module contains an implementation of the NEAT algorithm using the Python-NEAT package. This trains a recurrent neural network with a genetic algroithm by evaluating the performance of genomes when competing against eachother. 

Additionally, a **test** module exists, which contains unit tests
to validate the classes in the **poker** module.

Each network gets the following inputs:

- **Hand Strength** - The probability of winning the hand, calculated via a Monte Carlo simulation
- **Stack Size** - The number of chips in the player's stack
- **Current Hand Investment** - The number of chips the player has invested in the current hand
- **Pot Size** - The amount of chips to be won in the hand
- **Opponent Actions** - For each other player, the action taken in the current round (No Action, Call, Check, Fold, Raise, All-In)
- **Previous Action** - The last action taken by the player (No action if starting a new round)

And returns the following outputs:
- **Call**
- **Check**
- **Hold**
- **Raise**
- **Raise Amount** - Always returned, the number of chips to be raised if raise is activated.
- **All-In**

## Project Setup

Navigate to the location you want to save the repo in the command prompt. Create a new folder that you want the repo to be contained in. Navigate to the inside of that repo and clone the repository using the HTTPS or SSH link from github.

Create a virtual environment using the following command in the 
command prompt:
```
python -m venv {insert virtual environment name here}
```
Activate the virtual environment:
```
{insert virtual environment name here}\Scripts\activate
```
Install dependencies:
```
pip install -r poker-bot\requirements.txt
```

## Training the Model

To modify the training parameters, see the global variables at ```poker-bot/neat/neat.py```, or edit the config file at ```poker-bot/neat/config.txt```. See the NEAT-Python docs for more information about the parameters defined in the config file (https://neat-python.readthedocs.io/en/latest/config_file.html)

After reviewing the parameters, run
```
python -m poker-bot.neat.neat
```
from the root directory to train the model.

**NOTE:** Training may take a very long time. For example,
training with my Intel i7-6700 HQ CPU, training with the
following parameters takes approximately 2.22 hours per generation:
```
neat.py
GAME_SIZE = 10
MAX_ROUNDS = 25
NUM_HAND_SIMS = 50

config.txt
pop_size = 50
```

Note that the bottleneck is the Monte Carlo simulation, so removing the hand strength parameter from the model, or providing
a less time-intensive metric for hand strength would greatly speed up the model.

## Using the Model

Will finish this section later...