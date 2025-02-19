# Environmental AI Agent
The Environmental AI Agent is a Python application designed to help users track, analyze, and improve their personal carbon footprint. The system logs daily activities across four key categories: transportation, energy usage, food consumption, and purchases, calculating their environmental impact in terms of CO2 equivalent emissions (CO2e).

## Features
- **Carbon Footprint Tracking**: Log daily activities and see their estimated environmental impact
- **Personalized Reports**: Generate summaries for different time periods (week/month/year)
- **Data Visualization**: Visual breakdown of carbon footprint by category
- **Eco Tips**: Personalized recommendations based on user behavior patterns
- **Sustainable Product Recommendations**: Suggestions for eco-friendly alternatives

## Installation

### Prerequisites
- Python 3.6 or higher
- pandas
- numpy
- matplotlib

### Setup
1. Clone this repository
2. Install required dependencies:
   ```
   pip install pandas numpy matplotlib
   ```
3. Create a `data` directory in your project folder for storing user data

## Usage

### Basic Usage
```python
from environmental_ai_agent import EnvironmentalAIAgent

# Create an agent instance for a user
eco_agent = EnvironmentalAIAgent("user123")

# Track transportation
eco_agent.track_transportation("car", 15.5, passengers=1)

# Track energy usage
eco_agent.track_energy_usage("electricity", 120, "kWh")

# Track food consumption
eco_agent.track_food([
    {"type": "vegetables", "amount": 1.2, "local": True, "organic": True},
    {"type": "chicken", "amount": 0.5, "local": False, "organic": False}
])

# Track purchases
eco_agent.track_purchase("electronics", "Smartphone", 800, eco_friendly=False)
```

### Generating Reports
```python
# Get a summary of your carbon footprint
summary = eco_agent.get_carbon_footprint_summary("month")
print(f"Total Carbon Footprint: {summary['total']} kg CO2e")

# Generate a detailed text report
report = eco_agent.generate_report("month")
print(report)

# Create visualizations
eco_agent.visualize_carbon_footprint("month")
```

### Getting Recommendations
```python
# Get personalized environmental tips
tips = eco_agent.get_personalized_tips(count=3)

# Get sustainable product recommendations
products = eco_agent.recommend_sustainable_products(category="home")
```

## Data Storage
User data is stored in JSON format within the `data/{username}/` directory:
- `carbon_footprint.json`: Contains all logged activities and their emissions
- `preferences.json`: Stores user preferences used for personalized recommendations

## Emissions Calculation
The system uses standard emissions factors to estimate carbon impact:
- Transportation: Emissions per km based on transport mode
- Energy: Emissions per kWh based on energy type
- Food: Emissions based on food type, with modifiers for local/organic options
- Purchases: Estimated emissions based on spending amount and product category

## Limitations
- Emissions factors are simplified estimates and may not reflect regional variations
- The visualizations are currently only displayed, not saved (commented out in code)
- Advanced analytics features like predictive modeling are not implemented

## Future Improvements
- Integration with smart home devices and fitness trackers
- Machine learning for more accurate personalized recommendations
- Regional emissions factors based on user location
- Mobile app interface

## License
[MIT License]

## Contributing
Contributions are welcome! Please open an issue or submit a pull request.
