# FlappyBirdAI
Flappy Bird AI Trainer
This project is a Flappy Bird AI Trainer implemented using Python and the NEAT (NeuroEvolution of Augmenting Topologies) algorithm. The goal is to train an AI agent to play Flappy Bird, an addictive mobile game where the player controls a bird and navigates it through a series of pipes without colliding.

Features
AI agent: The trainer utilizes the NEAT algorithm to train an AI agent to play Flappy Bird. The agent learns to make decisions on when to flap its wings to avoid colliding with the pipes.
Python: The trainer is implemented in Python, a powerful and widely-used programming language, making it easy to understand and modify the code.
NEAT: NEAT is an evolutionary algorithm that evolves neural networks with a variable number of nodes and connections. It allows the AI agent to adapt and improve its performance over time.
Flappy Bird Game: The trainer includes the Flappy Bird game itself, where you can watch the AI agent play or even play the game manually.
Requirements
To run the Flappy Bird AI Trainer, you need to have the following:

Python 3.x: Make sure you have Python 3.x installed on your system.

NEAT-Python: Install the NEAT-Python library to use the NEAT algorithm. You can install it using pip:

![image](https://github.com/W3ndig0u0/FlappyBirdAI/assets/70271139/a4909cc7-61e2-4652-aa01-3f8ab8b8522b)

Copy code
pip install neat-python
Usage
Clone the repository:

bash
Copy code
git clone https://github.com/your-username/flappy-bird-ai-trainer.git
Navigate to the project directory:

bash
Copy code
cd flappy-bird-ai-trainer
Run the trainer:

Copy code
python trainer.py
This will start the training process, and you will see the AI agent playing Flappy Bird in the console.

Alternatively, you can play the game manually:

Copy code
python manual_play.py
Use the spacebar to flap the bird's wings and navigate through the pipes.

In Progress
Currently, the ability to save and use the best model is still in progress. We are working on implementing this feature to allow you to save the trained AI agent and use it for future gameplay.

Note
Please note that the settings menu is currently locked, and you cannot change any settings such as the AI's population size, mutation rates, or game difficulty. We are actively working on adding customization options to enhance the training experience.

Contributing
We welcome contributions to the Flappy Bird AI Trainer project. If you find any issues or have suggestions for improvements, please feel free to open an issue or submit a pull request on the project's GitHub repository.

License
This project is licensed under the MIT License. Feel free to use, modify, and distribute the code as per the license terms.
