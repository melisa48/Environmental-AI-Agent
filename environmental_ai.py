import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from collections import defaultdict
import json
import os

class EnvironmentalAIAgent:
    def __init__(self, user_name):
        self.user_name = user_name
        self.data_path = f"data/{user_name}/"
        self.carbon_data = self._load_or_create_data("carbon_footprint.json", {
            "transportation": [],
            "energy": [],
            "food": [], 
            "purchases": []
        })
        self.eco_tips = self._load_tips()
        self.sustainable_products = self._load_sustainable_products()
        self.user_preferences = self._load_or_create_data("preferences.json", {
            "diet_type": "omnivore",
            "home_type": "apartment",
            "transportation_primary": "car",
            "interests": []
        })
        
    def _load_or_create_data(self, filename, default_data):
        """Load data from file or create new with default structure"""
        try:
            os.makedirs(self.data_path, exist_ok=True)
            file_path = os.path.join(self.data_path, filename)
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    return json.load(f)
            else:
                with open(file_path, 'w') as f:
                    json.dump(default_data, f)
                return default_data
        except Exception as e:
            print(f"Error loading data: {e}")
            return default_data
            
    def _save_data(self, filename, data):
        """Save data to file"""
        try:
            file_path = os.path.join(self.data_path, filename)
            with open(file_path, 'w') as f:
                json.dump(data, f)
            return True
        except Exception as e:
            print(f"Error saving data: {e}")
            return False
    
    def _load_tips(self):
        """Load environmental tips database"""
        return {
            "transportation": [
                "Consider carpooling to reduce emissions",
                "Try using public transportation once a week",
                "Combine errands to reduce total driving distance",
                "Consider an electric vehicle for your next car purchase",
                "Keep your tires properly inflated to improve fuel efficiency"
            ],
            "energy": [
                "Switch to LED light bulbs to reduce energy consumption",
                "Unplug electronics when not in use to avoid phantom energy",
                "Use a smart thermostat to optimize heating and cooling",
                "Air dry clothes instead of using a dryer when possible",
                "Consider adding insulation to your home to reduce energy needs"
            ],
            "food": [
                "Try incorporating one meatless meal per week",
                "Buy local produce to reduce transportation emissions",
                "Plan meals to reduce food waste",
                "Compost food scraps instead of sending to landfill",
                "Choose seasonal fruits and vegetables"
            ],
            "purchases": [
                "Consider secondhand items before buying new",
                "Look for products with minimal packaging",
                "Invest in quality items that last longer",
                "Repair items when possible instead of replacing",
                "Choose products made from recycled materials"
            ]
        }
    
    def _load_sustainable_products(self):
        """Load sustainable product recommendations"""
        return {
            "home": [
                {"name": "Smart thermostat", "description": "Reduces energy usage by 10-15%"},
                {"name": "Low-flow showerhead", "description": "Reduces water usage while maintaining pressure"},
                {"name": "Wool dryer balls", "description": "Reduces drying time and eliminates need for dryer sheets"}
            ],
            "kitchen": [
                {"name": "Beeswax food wraps", "description": "Reusable alternative to plastic wrap"},
                {"name": "Silicone food storage bags", "description": "Durable alternative to disposable plastic bags"},
                {"name": "Compost bin", "description": "Convenient way to collect food scraps for composting"}
            ],
            "personal": [
                {"name": "Bamboo toothbrush", "description": "Biodegradable alternative to plastic toothbrushes"},
                {"name": "Shampoo bar", "description": "Zero-waste alternative to bottled shampoo"},
                {"name": "Reusable water bottle", "description": "Reduces plastic waste from disposable bottles"}
            ]
        }
    
    def track_transportation(self, mode, distance, passengers=1):
        """Track transportation activity and carbon impact"""
        emissions_factors = {
            "car": 0.192,  # kg CO2 per km
            "bus": 0.105,  # kg CO2 per km per person
            "train": 0.041,  # kg CO2 per km per person
            "bicycle": 0,
            "walk": 0,
            "plane": 0.255  # kg CO2 per km per person
        }
        
        if mode not in emissions_factors:
            return f"Sorry, I don't recognize '{mode}' as a transportation mode."
        
        # Calculate emissions
        if mode == "car":
            emissions = emissions_factors[mode] * distance / max(1, passengers)
        else:
            emissions = emissions_factors[mode] * distance
            
        entry = {
            "date": datetime.now().isoformat(),
            "mode": mode,
            "distance": distance,
            "passengers": passengers,
            "emissions": round(emissions, 2)
        }
        
        self.carbon_data["transportation"].append(entry)
        self._save_data("carbon_footprint.json", self.carbon_data)
        
        return f"Tracked {distance} km via {mode} with carbon impact of {round(emissions, 2)} kg CO2e"
    
    def track_energy_usage(self, type, amount, unit):
        """Track home energy usage and carbon impact"""
        emissions_factors = {
            "electricity": 0.233,  # kg CO2 per kWh (US average)
            "natural_gas": 0.181,  # kg CO2 per kWh
            "heating_oil": 0.249,  # kg CO2 per kWh
            "propane": 0.215,  # kg CO2 per kWh
            "renewable": 0.015  # kg CO2 per kWh (small lifecycle emissions)
        }
        
        if type not in emissions_factors:
            return f"Sorry, I don't recognize '{type}' as an energy type."
            
        # Convert units if needed
        if unit == "therms" and type == "natural_gas":
            amount = amount * 29.3001  # Convert therms to kWh
            unit = "kWh"
            
        if unit != "kWh":
            return f"I currently only support kWh units. Please convert {unit} to kWh."
            
        emissions = emissions_factors[type] * amount
        
        entry = {
            "date": datetime.now().isoformat(),
            "type": type,
            "amount": amount,
            "unit": unit,
            "emissions": round(emissions, 2)
        }
        
        self.carbon_data["energy"].append(entry)
        self._save_data("carbon_footprint.json", self.carbon_data)
        
        return f"Tracked {amount} {unit} of {type} with carbon impact of {round(emissions, 2)} kg CO2e"
    
    def track_food(self, items):
        """Track food consumption and approximate carbon impact"""
        emissions_factors = {
            "beef": 27.0,        # kg CO2e per kg
            "lamb": 39.2,        # kg CO2e per kg
            "pork": 12.1,        # kg CO2e per kg
            "chicken": 6.9,      # kg CO2e per kg
            "fish": 6.1,         # kg CO2e per kg
            "eggs": 4.8,         # kg CO2e per kg
            "rice": 2.7,         # kg CO2e per kg
            "milk": 1.9,         # kg CO2e per kg
            "cheese": 13.5,      # kg CO2e per kg
            "vegetables": 2.0,   # kg CO2e per kg
            "fruits": 1.1,       # kg CO2e per kg
            "beans": 2.0,        # kg CO2e per kg
            "nuts": 2.3          # kg CO2e per kg
        }
        
        total_emissions = 0
        tracked_items = []
        
        for item in items:
            food_type = item.get("type")
            amount = item.get("amount", 0)  # kg
            local = item.get("local", False)
            organic = item.get("organic", False)
            
            if food_type not in emissions_factors:
                continue
                
            # Calculate base emissions
            item_emissions = emissions_factors[food_type] * amount
            
            # Apply modifiers
            if local:
                item_emissions *= 0.8  # 20% reduction for local food
            if organic:
                item_emissions *= 0.9  # 10% reduction for organic food
                
            total_emissions += item_emissions
            
            tracked_items.append({
                "type": food_type,
                "amount": amount,
                "local": local,
                "organic": organic,
                "emissions": round(item_emissions, 2)
            })
        
        entry = {
            "date": datetime.now().isoformat(),
            "items": tracked_items,
            "total_emissions": round(total_emissions, 2)
        }
        
        self.carbon_data["food"].append(entry)
        self._save_data("carbon_footprint.json", self.carbon_data)
        
        return f"Tracked {len(tracked_items)} food items with total carbon impact of {round(total_emissions, 2)} kg CO2e"
    
    def track_purchase(self, category, description, price, eco_friendly=False):
        """Track purchases and estimated carbon impact"""
        # Rough estimates of kg CO2e per dollar spent
        emissions_factors = {
            "clothing": 0.5,
            "electronics": 0.7,
            "furniture": 0.8,
            "household": 0.4,
            "hobby": 0.3
        }
        
        category = category.lower()
        if category not in emissions_factors:
            category = "household"  # default
            
        # Calculate emissions based on price
        emissions = emissions_factors[category] * price
        
        # Apply discount for eco-friendly products
        if eco_friendly:
            emissions *= 0.7  # 30% reduction
            
        entry = {
            "date": datetime.now().isoformat(),
            "category": category,
            "description": description,
            "price": price,
            "eco_friendly": eco_friendly,
            "emissions": round(emissions, 2)
        }
        
        self.carbon_data["purchases"].append(entry)
        self._save_data("carbon_footprint.json", self.carbon_data)
        
        return f"Tracked purchase: {description} with estimated carbon impact of {round(emissions, 2)} kg CO2e"
    
    def get_carbon_footprint_summary(self, time_period="month"):
        """Calculate carbon footprint summary for specified time period"""
        today = datetime.now()
        
        if time_period == "week":
            start_date = (today - timedelta(days=7)).isoformat()
        elif time_period == "month":
            start_date = (today - timedelta(days=30)).isoformat()
        elif time_period == "year":
            start_date = (today - timedelta(days=365)).isoformat()
        else:
            return f"Unsupported time period: {time_period}. Please use 'week', 'month', or 'year'."
        
        summary = {
            "transportation": 0,
            "energy": 0,
            "food": 0,
            "purchases": 0,
            "total": 0
        }
        
        # Calculate transportation emissions
        for entry in self.carbon_data["transportation"]:
            if entry["date"] >= start_date:
                summary["transportation"] += entry["emissions"]
        
        # Calculate energy emissions
        for entry in self.carbon_data["energy"]:
            if entry["date"] >= start_date:
                summary["energy"] += entry["emissions"]
        
        # Calculate food emissions
        for entry in self.carbon_data["food"]:
            if entry["date"] >= start_date:
                summary["food"] += entry["total_emissions"]
        
        # Calculate purchase emissions
        for entry in self.carbon_data["purchases"]:
            if entry["date"] >= start_date:
                summary["purchases"] += entry["emissions"]
        
        # Calculate total
        summary["total"] = (
            summary["transportation"] + 
            summary["energy"] + 
            summary["food"] + 
            summary["purchases"]
        )
        
        # Round all values
        for key in summary:
            summary[key] = round(summary[key], 2)
        
        return summary
    
    def get_personalized_tips(self, category=None, count=3):
        """Get personalized environmental tips based on user data and preferences"""
        if category and category not in self.eco_tips:
            return [f"Sorry, I don't have tips for the category '{category}'."]
            
        categories = [category] if category else list(self.eco_tips.keys())
        selected_tips = []
        
        # Analyze user data to find areas for improvement
        footprint = self.get_carbon_footprint_summary("month")
        if isinstance(footprint, dict):
            # Sort categories by highest emissions
            sorted_categories = sorted(
                [(k, v) for k, v in footprint.items() if k != "total"],
                key=lambda x: x[1],
                reverse=True
            )
            
            # Prioritize tips from high-emission categories
            for high_category, _ in sorted_categories:
                if high_category in self.eco_tips and high_category in categories:
                    tips = self.eco_tips[high_category]
                    if tips:
                        selected_tips.append(tips[np.random.randint(0, len(tips))])
                        if len(selected_tips) >= count:
                            break
        
        # Fill remaining slots with random tips
        while len(selected_tips) < count:
            random_category = categories[np.random.randint(0, len(categories))]
            tips = self.eco_tips[random_category]
            if tips:
                tip = tips[np.random.randint(0, len(tips))]
                if tip not in selected_tips:
                    selected_tips.append(tip)
        
        return selected_tips
    
    def recommend_sustainable_products(self, category=None, count=3):
        """Recommend sustainable products based on user preferences and data"""
        if category and category not in self.sustainable_products:
            return [f"Sorry, I don't have product recommendations for the category '{category}'."]
            
        categories = [category] if category else list(self.sustainable_products.keys())
        recommendations = []
        
        for cat in categories:
            products = self.sustainable_products[cat]
            if products:
                # For simplicity, just selecting random products
                # A more sophisticated system would use user preferences and past purchases
                available_products = products.copy()
                np.random.shuffle(available_products)
                recommendations.extend(available_products[:min(count, len(available_products))])
                if len(recommendations) >= count:
                    recommendations = recommendations[:count]
                    break
        
        return recommendations
    
    def generate_report(self, time_period="month"):
        """Generate comprehensive environmental impact report"""
        footprint = self.get_carbon_footprint_summary(time_period)
        if isinstance(footprint, str):  # Error message
            return f"Couldn't generate report: {footprint}"
            
        # Get average per-category emissions
        summary = footprint
        
        # Get improvement tips
        tips = self.get_personalized_tips(count=5)
        
        # Generate comparison to average
        # These values are fictional averages - would use real data in production
        average_footprints = {
            "week": {"transportation": 23, "energy": 58, "food": 35, "purchases": 18},
            "month": {"transportation": 92, "energy": 232, "food": 140, "purchases": 72},
            "year": {"transportation": 1104, "energy": 2784, "food": 1680, "purchases": 864}
        }
        
        comparison = {}
        if time_period in average_footprints:
            avg = average_footprints[time_period]
            comparison = {
                cat: {
                    "user": summary[cat],
                    "average": avg[cat],
                    "difference_percent": round((summary[cat] - avg[cat]) / avg[cat] * 100, 1) if avg[cat] > 0 else 0
                }
                for cat in avg
            }
            comparison["total"] = {
                "user": summary["total"],
                "average": sum(avg.values()),
                "difference_percent": round(
                    (summary["total"] - sum(avg.values())) / sum(avg.values()) * 100, 1
                ) if sum(avg.values()) > 0 else 0
            }
        
        report_data = {
            "time_period": time_period,
            "carbon_footprint": summary,
            "comparison": comparison,
            "improvement_tips": tips,
            "generated_at": datetime.now().isoformat()
        }
        
        # Generate text report
        text_report = f"ENVIRONMENTAL IMPACT REPORT - {time_period.upper()}\n"
        text_report += f"Generated on {datetime.now().strftime('%B %d, %Y')}\n\n"
        
        text_report += "YOUR CARBON FOOTPRINT SUMMARY:\n"
        text_report += f"- Transportation: {summary['transportation']} kg CO2e\n"
        text_report += f"- Home Energy: {summary['energy']} kg CO2e\n"
        text_report += f"- Food Choices: {summary['food']} kg CO2e\n"
        text_report += f"- Purchases: {summary['purchases']} kg CO2e\n"
        text_report += f"- TOTAL: {summary['total']} kg CO2e\n\n"
        
        if comparison:
            avg_total = sum(average_footprints[time_period].values())
            diff = comparison["total"]["difference_percent"]
            text_report += "COMPARISON TO AVERAGE:\n"
            if diff < 0:
                text_report += f"Your footprint is {abs(diff)}% LOWER than average. Great job!\n\n"
            elif diff > 0:
                text_report += f"Your footprint is {diff}% HIGHER than average. There's room for improvement.\n\n"
            else:
                text_report += "Your footprint is about AVERAGE.\n\n"
        
        text_report += "PERSONALIZED IMPROVEMENT TIPS:\n"
        for i, tip in enumerate(tips, 1):
            text_report += f"{i}. {tip}\n"
            
        return text_report
    
    def visualize_carbon_footprint(self, time_period="month"):
        """Generate visualization of carbon footprint data"""
        summary = self.get_carbon_footprint_summary(time_period)
        if isinstance(summary, str):  # Error message
            return f"Couldn't create visualization: {summary}"
            
        # Create visualization (would output file path in real implementation)
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        # Pie chart of emission sources
        labels = [k for k in summary if k != "total"]
        sizes = [summary[k] for k in labels]
        
        if sum(sizes) > 0:  # Ensure we have data to plot
            ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
            ax1.axis('equal')
            ax1.set_title(f'Carbon Footprint Breakdown - {time_period.capitalize()}')
            
            # Bar chart comparing to average
            # These values are fictional averages - would use real data in production
            average_footprints = {
                "week": {"transportation": 23, "energy": 58, "food": 35, "purchases": 18},
                "month": {"transportation": 92, "energy": 232, "food": 140, "purchases": 72},
                "year": {"transportation": 1104, "energy": 2784, "food": 1680, "purchases": 864}
            }
            
            if time_period in average_footprints:
                avg = average_footprints[time_period]
                categories = [k for k in avg]
                
                user_values = [summary[k] for k in categories]
                avg_values = [avg[k] for k in categories]
                
                x = np.arange(len(categories))
                width = 0.35
                
                ax2.bar(x - width/2, user_values, width, label='Your Footprint')
                ax2.bar(x + width/2, avg_values, width, label='Average')
                
                ax2.set_ylabel('kg CO2e')
                ax2.set_title(f'Your Footprint vs. Average - {time_period.capitalize()}')
                ax2.set_xticks(x)
                ax2.set_xticklabels(categories)
                ax2.legend()
                
                plt.tight_layout()
                
                # In a real implementation, save to file and return path
                # plt.savefig(f"{self.data_path}/footprint_{time_period}.png")
                
                return "Visualization created successfully! (Would display or save image in actual implementation)"
            else:
                return f"No average data available for time period: {time_period}"
        else:
            return "Not enough data to generate visualization"
    
    def set_user_preferences(self, preferences):
        """Update user preferences"""
        for key, value in preferences.items():
            if key in self.user_preferences:
                self.user_preferences[key] = value
                
        self._save_data("preferences.json", self.user_preferences)
        return "User preferences updated successfully"

# Example usage
if __name__ == "__main__":
    # Create an instance for a user
    eco_agent = EnvironmentalAIAgent("user123")
    
    # Track some activities
    print(eco_agent.track_transportation("car", 15.5, 1))
    print(eco_agent.track_energy_usage("electricity", 120, "kWh"))
    print(eco_agent.track_food([
        {"type": "vegetables", "amount": 1.2, "local": True, "organic": True},
        {"type": "chicken", "amount": 0.5, "local": False, "organic": False}
    ]))
    print(eco_agent.track_purchase("electronics", "Smartphone", 800, eco_friendly=False))
    
    # Get personalized tips
    tips = eco_agent.get_personalized_tips()
    print("\nPersonalized Tips:")
    for i, tip in enumerate(tips, 1):
        print(f"{i}. {tip}")
    
    # Generate carbon footprint report
    summary = eco_agent.get_carbon_footprint_summary("month")
    print(f"\nTotal Carbon Footprint: {summary['total']} kg CO2e")
    
    # Get sustainable product recommendations
    recommendations = eco_agent.recommend_sustainable_products()
    print("\nRecommended Products:")
    for i, product in enumerate(recommendations, 1):
        print(f"{i}. {product['name']} - {product['description']}")