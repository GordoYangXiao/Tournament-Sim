import random
import time
import pickle
from PIL import Image, ImageDraw, ImageFont
from tkinter import filedialog
import tkinter as tk
from PIL import Image, ImageTk

class Fighter:
    # Basic fighter and character values, saves the amount of wins, losses, and image path for fighter 
    # Plan to work on abstraction of the fighter character, allows the code to expand further than just MMA or fighting
    def __init__(self, name, stamina, strength, agility, image_path, wins = 0, losses = 0, knockdown=0):
        self.name = name
        # By default every fighter will always have 100 health, (This can be adjusted in the future if there are different scaling)
        self.health = 100             
        self.stamina = stamina         
        self.strength = strength       
        self.agility = agility
        self.image_path = image_path          
        self.wins = wins
        self.losses = losses
        self.knockdown = knockdown
        
class FightType:
    # Parent class for each fighting style such as boxing or wrestling, shows displayed name, the randomizer's damage range, and how many rounds for each fight
    def __init__(self, name, damage_range, rounds):
        self.name = name
        self.damage_range = damage_range
        self.rounds = rounds
    def fight(self, fighter1, fighter2):
        pass

class Boxing(FightType):
    def __init__(self):
        # Mock boxing for now uses damage between 40-50 and 3 rounds
        super().__init__("Boxing", (40, 50), 3)
        self.action_events = 3

    def fight(self, fighter1, fighter2):
        # Some fight logic for boxing, there is the ability to punch and dodge punches, based on player stats and randomness 
        def helper(f1, f2):
            punch_strength = random.randint(self.damage_range[0], self.damage_range[1]) + int(f1.strength/10) - int(f2.agility / 5)
            dodge_chance = f2.agility / 150 - int(f1.agility / 200)
            if random.random() < dodge_chance:
                print(f"{f2.name} dodges the straight punch", end = "! ")
                punch_strength = max(0, punch_strength - int(dodge_chance * random.randint(30,50)))
                if punch_strength == 0:
                    return ""
            # Knockout system that keeps track of amounts of knockouts, it then would end the match if there is more than 4 for a fighter
            if f2.health <= punch_strength:
                f2.knockdown += 1
                if f2.knockdown >= 4:
                        return f"{f2.name} has been knocked down 4 times. They lose by TKO!"
                f2.health = 50 + int(f2.stamina/10)
                return f"{f2.name} is knocked down!"
            else:
                f2.health -= punch_strength
            return f"{f1.name} punches {f2.name} for {punch_strength} health!"
        
        # Picks which fighter gets to punch by randomization and a little bit of chance from fighter's agility
        action_event = random.random()
        if action_event < (0.5 + (.1*fighter1.agility/100) - (.1*fighter2.agility/100)):  
            return helper(fighter1,fighter2)
        else:  
            return helper(fighter2, fighter1)

# Mock system for wrestling, it does not work similar to real wrestling, there is more research that needs to be done
class Wrestling(FightType):
    def __init__(self):
        super().__init__("Wrestling", (5, 15), 3)
        self.action_events = 3

    def fight(self, fighter1, fighter2):
        action_event = random.random()

        if action_event < 0.3:  # 30% chance for a takedown
            takedown_strength = random.randint(self.damage_range[0], self.damage_range[1])
            fighter2.health -= takedown_strength
            return f"performs a takedown on {fighter2.name} for {takedown_strength} damage!"
        else:
            submission_chance = fighter1.strength / 100
            if random.random() < submission_chance:
                return f"attempts a submission on {fighter2.name}!"
            else:
                return f"{fighter1.name}'s takedown or submission fails!"

# Main class for the game to run
class Game:
    def __init__(self):
        # Automatically loads a fighter file, if it does not exist, then it will automatically create one in the same directory as your .py. 
        self.fighters = self.load_fighters("fighters.pkl")
        # Allows for abstraction and easily add more fighting types with different logic to the game 
        self.available_fight_types = [Boxing(), Wrestling()]

    # Creates a fighter and saves it to the pickle file
    def create_fighter(self):
        name = input("Enter fighter's name: ")
        stamina = int(input("Enter fighter's stamina: "))
        strength = int(input("Enter fighter's strength: "))
        agility = int(input("Enter fighter's agility: "))

        # Select an image to save to the fighter. This will have to be adjusted. I plan to save the image to a different location so when the user deletes or moves their file, we have it working saved somewhere else
        image_path = filedialog.askopenfilename(title=f"Select an image", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])

        fighter = Fighter(name, stamina, strength, agility, image_path)
        self.fighters.append(fighter)  
        self.save_fighters()      
        return fighter

    # Edit an existing fighters stats 
    def edit_fighter_stats(self, fighter):
        print(f"{fighter.name}'s original stats:")
        print(f"Stamina: {fighter.stamina}")
        print(f"Strength: {fighter.strength}")
        print(f"Agility: {fighter.agility}")
        # Prints the fighters stats to the user first so they know what to adjust 
        
        valid_input = False
        # Attempts error checking and allows for reinput, needs to readjust to reprompt
        while not valid_input:
            # Asks for the user inputs of the new stats, basically create_fighter
            try:
                new_stamina = int(input(f"Enter {fighter.name}'s new stamina: "))
                new_strength = int(input(f"Enter {fighter.name}'s new strength: "))
                new_agility = int(input(f"Enter {fighter.name}'s new agility: "))

                image_path = filedialog.askopenfilename(title=f"Select an image for {fighter.name}",
                                        filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
                valid_input = True
                fighter.stamina = new_stamina
                fighter.strength = new_strength
                fighter.agility = new_agility
                fighter.image_path = image_path
                self.save_fighters()  # Save the updated fighter data

            except ValueError:
                print("Invalid input. Please enter valid numbers for stats.")

    def save_fighters(self):
        # Convert fighters to a list of dictionaries
        fighters_data = [{"name": fighter.name, "stamina": fighter.stamina, "strength": fighter.strength, "agility": fighter.agility,"image_path": fighter.image_path, "wins": fighter.wins, "losses": fighter.losses} for fighter in self.fighters]
        
        with open("fighters.pkl", "wb+") as file:
            pickle.dump(fighters_data, file)

    def load_fighters(self, filename):
        # Loads the fighters into a dictionary that the class can use. 
        try:
            with open(filename, 'rb') as file:
                fighters_data = pickle.load(file)
                fighters = [Fighter(data["name"], data["stamina"], data["strength"], data["agility"],data["image_path"], data["wins"], data["losses"]) for data in fighters_data]
        except (FileNotFoundError, EOFError):
            fighters = []
        return fighters

    def choose_fight_type(self):
        # Choose what type of fight style you want to use, so far only boxing and wrestling
        print("Choose a fight type:")
        for i, fight_type in enumerate(self.available_fight_types):
            print(f"{i + 1}. {fight_type.name}")
        choice = int(input("Enter the number of the fight type: ")) - 1

        if 0 <= choice < len(self.available_fight_types):
            return self.available_fight_types[choice]
        else:
            print("Invalid choice. Using the default fight type (Boxing).")
            return Boxing()

    # Draft function to merge and open images to display to the user when the fight happens 
    def merge_images(self, image_path1, image_path2):
        # Open images
        image1 = Image.open(image_path1)
        image2 = Image.open(image_path2)

        # Determine the maximum height
        max_height = max(image1.height, image2.height)

        # Calculate the new width for each image while maintaining the aspect ratio
        new_width1 = int(max_height * (image1.width / image1.height))
        new_width2 = int(max_height * (image2.width / image2.height))

        # Resize images
        resized_image1 = image1.resize((new_width1, max_height))
        resized_image2 = image2.resize((new_width2, max_height))

        # Create a new image with black background
        merged_width = new_width1 + new_width2
        merged_height = max_height
        merged_image = Image.new("RGB", (merged_width, merged_height), "black")

        # Paste the resized images
        merged_image.paste(resized_image1, (0, 0))
        merged_image.paste(resized_image2, (new_width1, 0))

        # Add text "VS" to the center of the merged image with a larger font size
        draw = ImageDraw.Draw(merged_image)
        font_size = 60  
        font = ImageFont.truetype("arial.ttf", font_size) 
        text = "VS"
        text_size = draw.textbbox((0, 0), text, font)
        text_position = ((merged_width - text_size[2]) // 2, (merged_height - text_size[3]) // 2)
        draw.text(text_position, text, fill="red", font=font)

        merged_image.show()
        return merged_image

    # Main fighting system for the game, prompts the fighting type class to execute it's fight functions. 
    # time.sleep() is used in order for it to be more immersive for the user to see what's happening
    def fight_round(self, fighter1, fighter2, fight_type):
        for round_num in range(1, fight_type.rounds + 1):
            print(f"Round {round_num} begins!")

            for _ in range(fight_type.action_events):
                time.sleep(3)

                fighter_action = fight_type.fight(fighter1, fighter2)
                print(f"{fighter_action}")
                
                # For now, this is to break out of the loops, but in the future this should be put into the fight_type class 
                if fighter1.health <= 0 or fighter2.health <= 0 or fighter1.knockdown >= 4  or fighter2.knockdown >= 4:
                    break
            
            time.sleep(3)
            # For now, this is to break out of the loops, but in the future this should be put into the fight_type class 
            if fighter1.health <= 0 or fighter2.health <= 0 or fighter1.knockdown >= 4 or fighter2.knockdown >= 4:
                break
            
            fighter1.health = min(100, fighter1.health + 10)
            fighter2.health = min(100, fighter2.health + 10)
            time.sleep(1)
            # Displays fighter stats after each round. 
            print(f"End of Round {round_num} - {fighter1.name} energy: {max(0, fighter1.health)}, knockdowns: {fighter1.knockdown} \n \t \t {fighter2.name} energy: {max(0, fighter2.health)}, knockdowns: {fighter2.knockdown}")
        self.determine_winner(fighter1, fighter2)

    # Finishes the fight with a message and records it to each fighters stats and saves. This will be put into the fight_type in the future. 
    def determine_winner(self, fighter1, fighter2):
            if fighter1.knockdown > fighter2.knockdown:
                print(f"{fighter2.name} wins the fight by knockout!")
                fighter2.wins += 1
                fighter1.losses += 1
            elif fighter2.knockdown > fighter1.knockdown:
                print(f"{fighter1.name} wins the fight by knockout!")
                fighter1.wins += 1
                fighter2.losses += 1
            elif fighter1.knockdown == fighter2.knockdown and fighter1.health > fighter2.health:
                print(f"{fighter1.name} wins the fight!")
                fighter1.wins += 1
                fighter2.losses += 1
            elif fighter1.knockdown == fighter2.knockdown and fighter2.health > fighter1.health:
                print(f"{fighter2.name} wins the fight!")
                fighter2.wins += 1
                fighter1.losses += 1
            else:
                print("It's a draw!")

    # Displays all the stats of the fighter
    def display_fighter_stats_and_records(self, fighter):
        print(f"Name: {fighter.name}")
        print(f"Health: {fighter.health}")
        print(f"Stamina: {fighter.stamina}")
        print(f"Strength: {fighter.strength}")
        print(f"Agility: {fighter.agility}")
        print(f"Image: {fighter.image_path}")
        print(f"Wins: {fighter.wins}")
        print(f"Losses: {fighter.losses}")
        
    # Delete fighter from the dictionary that you want 
    def delete_fighter(self, fighter_choice):
        fighter_name = self.fighters[fighter_choice].name
        del self.fighters[fighter_choice]
        print(f"{fighter_name} has been deleted.")

    # Main game function, inside a while loop it will continue to prompt until the user wants to quit out 
    def run(self):
        while True:
            print("\nTournament Simulator")
            print("1. Fight")
            print("2. Create a New Fighter")
            print("3. Edit Fighter Stats")
            print("4. Delete a Fighter")
            print("5. Display Fighter Stats and Records")
            print("6. Quit")
            choice = input("Enter your choice: ")

            if choice == "1":
                # Ask the player to choose two fighters to fight
                print("\nChoose the first fighter:")
                for i, fighter in enumerate(self.fighters):
                    print(f"{i + 1}. {fighter.name}")
                fighter_choice1 = int(input("Enter the number of the first fighter: ")) - 1

                print("\nChoose the second fighter:")
                for i, fighter in enumerate(self.fighters):
                    print(f"{i + 1}. {fighter.name}")
                fighter_choice2 = int(input("Enter the number of the second fighter: ")) - 1

                if 0 <= fighter_choice1 < len(self.fighters) and 0 <= fighter_choice2 < len(self.fighters) and fighter_choice1 != fighter_choice2:
                    fighter1 = self.fighters[fighter_choice1]
                    fighter2 = self.fighters[fighter_choice2]
                    fight_type = self.choose_fight_type()
                    
                    self.merge_images(fighter1.image_path, fighter2.image_path)
                    self.fight_round(fighter1, fighter2, fight_type)

                    # Reset fighter health values to 100
                    fighter1.health = 100
                    fighter2.health = 100
                    fighter1.knockdown = 0
                    fighter2.knockdown = 0

                    # Save the updated fighter data
                    self.save_fighters()
                else:
                    print("Invalid choices. Please select two different fighters.")

            # Create fighter
            elif choice == "2":
                self.create_fighter()

            # Edit fighter
            elif choice == "3":
                print("Choose a fighter to edit:")
                for i, fighter in enumerate(self.fighters):
                    print(f"{i + 1}. {fighter.name}")
                fighter_choice = int(input("Enter the number of the fighter to edit: ")) - 1
                if 0 <= fighter_choice < len(self.fighters):
                    self.edit_fighter_stats(self.fighters[fighter_choice])
                    self.save_fighters()
                else:
                    print("Invalid choice.")
            
            # Delete a fighter
            elif choice == "4":
                print("Choose a fighter to delete:")
                for i, fighter in enumerate(self.fighters):
                    print(f"{i + 1}. {fighter.name}")
                fighter_choice = int(input("Enter the number of the fighter to delete: ")) - 1
                if 0 <= fighter_choice < len(self.fighters):
                    self.delete_fighter(fighter_choice)
                    self.save_fighters()
                else:
                    print("Invalid choice.")

            # Display fighter stats
            elif choice == "5":
                print("Choose a fighter to display stats and records:")
                for i, fighter in enumerate(self.fighters):
                    print(f"{i + 1}. {fighter.name}")
                fighter_choice = int(input("Enter the number of the fighter to display stats and records: ")) - 1
                if 0 <= fighter_choice < len(self.fighters):
                    self.display_fighter_stats_and_records(self.fighters[fighter_choice])
                else:
                    print("Invalid choice.")

            # Quit
            elif choice == "6":
                break

            else:
                print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    root = tk.Tk()
    game = Game()
    game.run()
    root.withdraw()

    
# The main game is operational with some bugs that needs to be addressed. tk.TK() window does not close, but when root.withdraw() happens, the use is not prompted with the choice to pick an image for creating or editing a fighter after the first attempt. 
# Fight_style fight logic is very generalized and can be improved on based on how real fighting in boxing or wrestling works
# The idea of the project is to work with abstraction and new imports such as tk, PIL, and files that I have never worked with before. It is to learn how to refactor code to work with a more generalized idea that will be able to be used in a lot of different sports
# Plans for future development: Bug fixes, more styles of fighting, better accuracy to fighting styles, more immersive character creation, tournament system graphics that keep track of where each player is. 
