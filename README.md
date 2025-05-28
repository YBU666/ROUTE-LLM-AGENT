# Route Planning Agent

A Streamlit-based web application that helps users plan routes between two locations using OpenRouteService API.

## Features

- Interactive route planning between any two locations
- Real-time route visualization on an interactive map
- Turn-by-turn directions
- Distance and duration calculations
- Clean and modern user interface

## Prerequisites

- Python 3.7+
- OpenRouteService API key

## Installation

1. Clone the repository:
```bash
git clone https://github.com/YBU666/ROUTE-LLM-AGENT.git
cd ROUTE-LLM-AGENT
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root and add your OpenRouteService API key:
```
ORS_API_KEY=your_api_key_here
```

## Usage

Run the Streamlit app:
```bash
streamlit run app.py
```

The application will open in your default web browser.

## Technologies Used

- Streamlit
- OpenRouteService API
- Folium
- Geopy
- Python-dotenv

## License

MIT License 