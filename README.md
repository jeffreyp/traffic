# Traffic Merging Simulation

A graphical simulation to visualize and analyze the impact of cars merging onto a main road with configurable traffic parameters.

## Features

- Visual simulation of traffic patterns with cars merging from a side lane onto a main road
- Configurable parameters:
  - Number of cars merging per minute
  - Number of cars passing on the main road per minute
- Real-time visualization of traffic movement and merging behaviors
- Collision avoidance between vehicles
- Data collection on merge times and success rates
- Automated report generation with graphs and statistics

## Controls

- **Up/Down Arrow Keys**: Increase/decrease the rate of merging cars
- **Left/Right Arrow Keys**: Increase/decrease the rate of main road cars
- **R Key**: Generate and save a report with current simulation data
- **Close Window**: End the simulation and generate a final report

## Reports

Reports are automatically saved to the `reports` folder and include:
- Distribution of merge times with average
- Success rate of merging vehicles
- Simulation parameters summary

## Requirements

This simulation requires:
- Python 3.6+
- Pygame
- Matplotlib
- NumPy

## Installation

1. Clone this repository
2. Install the required packages:
```
pip install pygame matplotlib numpy
```

## Running the Simulation

To start the simulation, run:
```
python main.py
```

## Understanding the Visualization

- **Blue Cars**: Main road traffic
- **Red Cars**: Merging traffic
- The simulation shows how changing traffic rates affects merging efficiency
- Statistics are displayed in real-time at the top of the screen

## Example Report Analysis

The reports provide insights on:
- How increasing merging traffic affects merge times
- Relationship between main road traffic volume and successful merges
- Optimal traffic flow configurations