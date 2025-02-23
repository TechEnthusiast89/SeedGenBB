import random
import string
import logging
from tkinter import Tk, Label, Entry, Button, StringVar, IntVar, BooleanVar, messagebox, Text, Scrollbar, END, Checkbutton
import os

# Set up logging
user_home = os.path.expanduser("~")
log_file_path = os.path.join(user_home, 'seed_generator.log')
logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(message)s')

# Generate a random seed
def generate_seed(length=10):
    characters = string.ascii_letters + string.digits + "!@#$%^&*()"
    return ''.join(random.choice(characters) for _ in range(length))

# Simulate the evaluation of the seed for Battle Brothers criteria
def evaluate_seed(seed, num_stars_needed, star_count, include_negative):
    # Placeholder for actual game evaluation logic.
    # Simulated random values for demonstration purposes.
    num_stars = [random.choice([3, 4]) for _ in range(star_count)]
    
    if include_negative:
        has_negative_traits = random.choice([True, False])
    else:
        has_negative_traits = False

    if has_negative_traits:
        return False

    # Check if we have the desired number of stars
    if num_stars.count(num_stars_needed) >= star_count:
        return True
    
    return False

# Tailored traits for melee and ranged brothers
def generate_traits(brother_type, include_negative):
    positive_traits = {
        'melee': ["Strong", "Brave", "Iron Lungs", "Colossus"],
        'ranged': ["Quick", "Eagle Eyes", "Strong", "Determined"]
    }
    negative_traits = ["Pessimist", "Asthmatic", "Drunken", "Fearful"]

    traits = positive_traits.get(brother_type, [])
    if include_negative:
        traits += random.sample(negative_traits, k=1)  # Add a random negative trait if allowed

    return traits

# Main function to generate and evaluate seeds
def generate_and_evaluate_seeds(number_of_seeds, num_stars_needed, star_count, include_negative):
    valid_seeds = []
    for _ in range(number_of_seeds):
        seed = generate_seed()
        if evaluate_seed(seed, num_stars_needed, star_count, include_negative):
            # Add melee and ranged tailored traits
            melee_traits = generate_traits("melee", include_negative)
            ranged_traits = generate_traits("ranged", include_negative)
            valid_seeds.append((seed, melee_traits, ranged_traits))
    return valid_seeds

# Function to display the results
def display_results(valid_seeds, land_mass, water_ratio, other_settings):
    result_text = ""
    if not valid_seeds:
        result_text = "No valid seeds found that meet the criteria."
    else:
        result_text = f"Valid seeds meeting criteria: {len(valid_seeds)}\n"
        for seed, melee_traits, ranged_traits in valid_seeds:
            result_text += f"Seed: {seed}\n"
            result_text += f"Melee Traits: {', '.join(melee_traits)}\n"
            result_text += f"Ranged Traits: {', '.join(ranged_traits)}\n\n"
        result_text += "\nRecommended Settings:\n"
        result_text += f"Land Mass Ratio: {land_mass}%\n"
        result_text += f"Water Ratio: {water_ratio}%\n"
        result_text += "Other Settings:\n"
        for setting, value in other_settings.items():
            result_text += f"{setting}: {value}\n"
    result_display.delete(1.0, END)
    result_display.insert(END, result_text)

# Function to run the seed generation and evaluation process
def run_seed_generation():
    try:
        number_of_seeds_to_generate = seeds_to_generate.get()
        num_stars_needed = stars_needed.get()
        star_count = talents_needed.get()
        include_negative = negative_traits.get()
        
        land_mass = land_mass_ratio.get()
        water_ratio = 100 - land_mass
        other_settings = {
            "Snowline": snowline_level.get(),
            "Number of Settlements": settlements_count.get(),
            "Number of Factions": factions_count.get(),
            "Decked Out Citadels": decked_out_citadels.get(),
            "All Trade Buildings Available": trade_buildings_available.get(),
            "(Debug) Show Entire Map": show_entire_map.get()
        }

        logging.info("Generating and evaluating seeds with the given parameters.")
        valid_seeds = generate_and_evaluate_seeds(number_of_seeds_to_generate, num_stars_needed, star_count, include_negative)
        display_results(valid_seeds, land_mass, water_ratio, other_settings)
    except Exception as e:
        logging.error(f"Error during seed generation: {e}")
        messagebox.showerror("Error", f"An error occurred: {e}")

# Set up the GUI
root = Tk()
root.title("Battle Brothers Seed Generator")
root.geometry("600x400")  # Set a fixed window size

Label(root, text="Number of seeds to generate:").grid(row=0, column=0, sticky="e")
Label(root, text="Star rating needed (3 or 4):").grid(row=1, column=0, sticky="e")
Label(root, text="Number of star talents needed:").grid(row=2, column=0, sticky="e")
Label(root, text="Include negative traits?").grid(row=3, column=0, sticky="e")
Label(root, text="Land mass ratio (percentage):").grid(row=4, column=0, sticky="e")
Label(root, text="Snowline level (0-100):").grid(row=5, column=0, sticky="e")
Label(root, text="Number of settlements:").grid(row=6, column=0, sticky="e")
Label(root, text="Number of factions:").grid(row=7, column=0, sticky="e")
Label(root, text="Decked Out Citadels:").grid(row=8, column=0, sticky="e")
Label(root, text="All Trade Buildings Available:").grid(row=9, column=0, sticky="e")
Label(root, text="(Debug) Show Entire Map:").grid(row=10, column=0, sticky="e")

seeds_to_generate = IntVar(value=1000)
stars_needed = IntVar(value=4)
talents_needed = IntVar(value=4)
negative_traits = BooleanVar(value=False)
land_mass_ratio = IntVar(value=60)
snowline_level = IntVar(value=70)
settlements_count = IntVar(value=27)
factions_count = IntVar(value=6)
decked_out_citadels = BooleanVar(value=True)
trade_buildings_available = BooleanVar(value=True)
show_entire_map = BooleanVar(value=False)

Entry(root, textvariable=seeds_to_generate).grid(row=0, column=1)
Entry(root, textvariable=stars_needed).grid(row=1, column=1)
Entry(root, textvariable=talents_needed).grid(row=2, column=1)
Checkbutton(root, text="Include negative traits", variable=negative_traits).grid(row=3, column=1, sticky="w")
Entry(root, textvariable=land_mass_ratio).grid(row=4, column=1)
Entry(root, textvariable=snowline_level).grid(row=5, column=1)
Entry(root, textvariable=settlements_count).grid(row=6, column=1)
Entry(root, textvariable=factions_count).grid(row=7, column=1)
Checkbutton(root, text="Decked Out Citadels", variable=decked_out_citadels).grid(row=8, column=1, sticky="w")
Checkbutton(root, text="All Trade Buildings Available", variable=trade_buildings_available).grid(row=9, column=1, sticky="w")
Checkbutton(root, text="(Debug) Show Entire Map", variable=show_entire_map).grid(row=10, column=1, sticky="w")

Button(root, text="Generate Seeds", command=run_seed_generation).grid(row=11, column=0, columnspan=2)

scrollbar = Scrollbar(root)
scrollbar.grid(row=12, column=2, sticky='ns')

result_display = Text(root, wrap="word", yscrollcommand=scrollbar.set)
result_display.grid(row=12, column=0, columnspan=2)
scrollbar.config(command=result_display.yview)

root.mainloop()
