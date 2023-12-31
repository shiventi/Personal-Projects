# LEO - Chatbot with Web Interface

# Overview

LEO is a chatbot with a web interface, using natural language processing (NLP) and Facebook's Blenderbot for conversational interactions. The chatbot is designed to provide responses to user inputs based on predefined intents.

## Features

- Natural Language Processing: The chatbot employs NLP techniques to understand and respond to user inputs.
- Machine Learning: The underlying model is trained using TensorFlow and TFLearn for improved conversation handling as well as a pre-built Facebook chatbot.
- Web Interface: Users can interact with the chatbot through a simple web page, enhancing the user experience.

## Getting Started

### Prerequisites

- Python 3.X
- Required Python libraries: `os`, `sys`, `json`, `nltk`, `random`, `tflearn`, `numpy`, `socketserver`, `tensorflow`, `transformers`

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/shiventi/Personal-Projects.git
   cd Personal-Projects/LEO

## Usage:
    python facebook_bot.py (make sure to pip install all libraries)

## Customization: 
- Customize chatbot responses by modifying the intents.json file.
- Train the chatbot with additional data by updating the training data in the script or through external files.

## Project Structure
LEO/
- facebook_bot.py          # Main script containing the chatbot logic and web server setup.
- intents.json             # JSON file containing training data for the chatbot.
- chatbot_dependencies.py  # Module for additional chatbot dependencies.
- webchat.html             # HTML file for the web interface.
- favicon1.png              # Image for HTML (favicon).
- leo_inaction.png         # Image of LEO in action.
- model.tflearn            # Saved model file (will be created once the code runs).
