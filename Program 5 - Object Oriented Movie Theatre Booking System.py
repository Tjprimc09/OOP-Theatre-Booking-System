class Theater():
    def __init__(self, name, location):
        self.name = name
        self.location = location
        self.movies = {
            "Avatar: Fire and Ash": 14.00,
            "The Running Man": 13.50,
            "Kill Bill: The Whole Bloody Affair": 12.75,
            "Five Nights at Freddy's": 11.50,
            "The SpongeBob Movie: Search for SquarePants": 10.00
        }

    def update_name(self):
        while True: #Loop until new_name is validated
            new_name = input("{:^}".format("Enter the new name for the theater (x to cancel):\n")).strip()

            if new_name == 'x':
                print("Returning to menu.\n")
                return
            if not new_name:
                print("{:^}".format("Theater name cannot be empty. Please try again.\n"))
                continue
            break   
        self.name = new_name #update self.name
        print("{:^}".format(f"Theater name updated to: {self.name}\n"))
        print(self)        
    
    def update_location(self):
        while True: #Loop until new_location is validated
            new_location = input("{:^}".format("Enter the new location for the theater (x to cancel):\n")).strip()

            if new_location == 'x':
                print("Returning to main menu.\n")
                return
            if not new_location:
                print("{:^}".format("Theater location cannot be empty. Please try again.\n"))
                continue
            break 

        self.location = new_location #update self.location
        print("{:^}".format(f"Theater location updated to: {self.location}\n"))
        print(self)
    

    def __str__(self): #Returns a STRING 
        print()
        info_header = "{:^50}".format(f"Welcome to {self.name:} at {self.location}!\n")
        info_subheader = "{:^50}".format("Available Movies:\n")
        info = info_header + "\n" + info_subheader

        for movie, price in self.movies.items(): 
            line = "{:^}".format(f"{movie:>30}: ${price:.2f}\n")
            info += "\n" + line + "\n"
        return info


class BookingSystem(Theater):
    def __init__(self, name, location):
        Theater.__init__(self, name, location)
        self.movie_title = ''
        self.num_tickets = 0
        self.bookings = {}
        self.receipt = []
        

    def add_booking(self):
        while True: #Main Loop. Continuously loop until user decides to stop adding bookings
            #Get a title     
            self.movie_title = input("{:^}".format("Enter the movie title you wish to purchase tickets for (x to cancel):\n")).strip()
            
            if self.movie_title == 'x':
                return
            
            if self.movie_title not in self.movies: #if title entered is not in available movies
                print("{:^}".format("Movie not found. Please select a movie from the list.\n"))
                continue #go back and try again
            
            seating = 100 - sum(self.bookings.get(self.movie_title, [])) #Set a seating capacity for each movie   
        
            while True: #Loop continuously until self.num_tickets is validated
                try:
                    self.num_tickets = int(input("{}".format(f"Enter the number of tickets you wish to book for '{self.movie_title}':\n")))
                    
                    if self.num_tickets <= 0: #validate input is a positive integer.
                        print("{:^}".format("Must book at least one ticket. Please try again.\n"))
                        continue
                
                    elif self.num_tickets + sum(self.bookings.get(self.movie_title, [])) > seating:
                        print("{:^}".format(f"Oops! This will exceed the seating capacity of {seating} for this movie!\n"))
                        print("{:^}".format(f"You have booked {sum(self.bookings.get(self.movie_title, []))} so far.\n"))
                        print("{:^}".format(f"You can book a maximum of {seating - sum(self.bookings.get(self.movie_title, []))} additional tickets.\n"))
                        continue

                    '''                                                  ^^^
                    Thinking about the concept of preventing overbooking here.
                    Mostly just practicing use of dict.get() with a default value.
                    dict.get() is useful for a situation where the key may or may not exist yet.
                    '''

                except ValueError:
                    #Response adjusts dynamically based on how many are already booked
                    print("{:^}\n".format(f"Input must be an integer (1-{seating - sum(self.bookings.get(self.movie_title, []))}). Please try again.\n"))
                    continue
                break 
            
            
            if self.movie_title in self.bookings: #check if movie selected alread exists in bookings dict
                self.bookings[self.movie_title].append(self.num_tickets) #if True, append the num of tickets as a batch to the movie's list of booked tickets
            
            else:# if the movie isn't already in bookings
                self.bookings[self.movie_title] = [self.num_tickets] #set a k:v pair in bookings w/ movie_title as k and v as a list with num_tickets as the first element
            
            print("{:^}".format(f"Successfully booked {self.num_tickets} tickets for '{self.movie_title}'.\n"))
            print("{:^}".format(f"Current ticket cost for this title: ${sum(self.bookings[self.movie_title]) * self.movies[self.movie_title]:.2f}\n"))
            print(f"Total cost of all bookings: ${sum([sum(self.bookings[title]) * self.movies[title] for title in self.bookings]):.2f}")
            seating -= self.num_tickets #decrement seating capacity
            
            '''
            Comprehending a list by iterating through bookings.
            For each title in bookings, 
            sum of tickets booked for that movie 
            * the ticket price for that movie.
            Then, sum of the completed list. 
            ''' 
            total = sum([sum(self.bookings[title]) * self.movies[title] for title in self.bookings])
            
            if not self.receipt: #if the receipt is currently empty:
                self.receipt = [self.bookings, total] #update it with bookings and total
                
                #if the user has left the add_booking loop, but is for some reason RETURNING
                #to add more (they already have a receipt with bookings and a total; it's just being updated)
            else: 
                self.receipt[1] = total #simply update the total
                #self.receipt[0] should be referencing an updated bookings dict
            
            if self.another_booking(): #if another_booking() returns true:
                continue #go back to the top of the main while loop and repeat the full process    
            break
            
    def another_booking(self):
        # Get a selection for adding another booking. 
        while True:
            another = input("{:^}".format("Would you like to make another booking? (y/n):\n")).strip().lower()
            if another not in ['y', 'n']:
                print("{:^}".format("Invalid input. Please enter 'y' for yes or 'n' for no.\n"))
                continue
            if another == 'y':
                return True
            return False
             
    def remove_booking(self):
        while True: #Loop continuously until user decides to stop removing bookings
            if not self.bookings:
                    print("{:^}".format("You have no bookings to remove. Returning to main menu.\n"))
                    return
            
            self.disp_bookings() #Display current bookings

            while True: #Loop continuously until remove is validated
                remove = input("{:^}".format("Which movie title would you like to remove bookings for? (x to cancel):\n")).strip()
                
                if remove.lower() == 'x': #Allow user to exit the remove_booking process
                    print("{:^}".format("Booking removal cancelled. Returning to main menu.\n"))
                    return
                
                if remove.isdigit(): #Validate given input is not numeric
                    print("{:^}".format("Invalid movie title. Please enter a valid movie title from your bookings.\n"))
                    continue

                if remove not in self.bookings: #Validate given input exists in bookings
                    print("{:^}".format(f"You have no bookings for '{remove}'. Please enter a valid movie title from your bookings.\n"))
                    continue #if not, go back and try again
                break 
            
            while True: #Loop until all is validated
                all = input("{:^}".format(f"Do you want to remove all tickets for '{remove}'? (y/n) (x to cancel):\n")).strip().lower()
                
                if all not in ['y', 'n', 'x']:
                    print("{:^}".format("Invalid input. Please enter 'y' for yes, 'n' for no, or 'x' to cancel.\n"))
                    continue
                if all == 'x': #Allow user to exit the remove_booking process
                    print("{:^}".format("Booking removal cancelled. Returning to main menu.\n"))
                    return
                break
            
            if all == 'n': #if the user doesn't wan't to remove them all
                while True: #Loop until num_remove is validated
                    try:
                        num_remove = int(input("{:^}".format(f"Enter the number of tickets you wish to remove from '{remove}':\n")))
                        
                        if num_remove <= 0: #validate num_remove is a positive int
                            print("{:^}".format("Must remove at least one ticket. Please try again.\n"))
                            continue
                        
                        elif num_remove > sum(self.bookings[remove]): #validate num_remove is a reasonable number to remove
                            print("{:^}".format(f"You only have {sum(self.bookings[remove])} tickets booked for '{remove}'. Please enter a number between 1 and {sum(self.bookings[remove])}.\n"))
                            continue
                    
                    except ValueError: #Handle bad input
                        print("{:^}".format(f"Input must be an integer. Please enter a valid number (1 - {len(self.bookings[remove])}).\n"))
                        continue
                    break #num_remove is now validated. We can move on.
                
                while True:
                    proceed = input("{:^}".format(f"Are you sure you want to remove {num_remove} tickets from '{remove}'? (y/n)(x to cancel):\n")).strip().lower()
                    if proceed not in ['y', 'n', 'x']:
                        print("{:^}".format("Invalid input. Please enter 'y' for yes, 'n' for no, or 'x' to cancel.\n"))
                        continue
                    elif proceed == 'x': #Allow user to exit the remove_booking process
                        print("{:^}".format("Booking removal cancelled. Returning to main menu.\n"))
                        return
                    elif proceed == 'n':
                        print("{:^}".format("No tickets were removed from your bookings.\n"))
                        continue #go back to the top of the main while loop and repeat the full process.
                    break
                
                left = num_remove

                #WALK INDEXES. NOT ELEMENTS.  
                for i in range(len(self.bookings[remove]) -1, -1, -1):#walk the indexes backwards, otherwise items shift left every iteration
                        
                    if self.bookings[remove][i] <= left: #if current element is <= what's left to remove:
                        left -= self.bookings[remove].pop(i) #pop it
                        
                    else: #But if what's left to remove is less than the current element:
                        self.bookings[remove][i] -= left #decrement the element by what's left
                        break #exit loop early in this case. no need to walk the rest of the indexes. 

                print("{:^}".format(f"Successfully removed {num_remove} tickets for '{remove}' from your bookings.\n"))
            
            else: #If the user chose to remove all the tickets for this movie:
                self.bookings.pop(remove) #just get rid of the whole k:v pair in bookings
                
                print("{:^}".format(f"Successfully removed all tickets for '{remove}' from your bookings.\n"))
            
                '''
                According to the design of the program, we know if it has made
                it this far, there exists a receipt. Therefore...
                Use the same comprehension as before to update the total
                '''
                total = sum([sum(self.bookings[title]) * self.movies[title] for title in self.bookings])
                self.receipt[1] = total #update the receipt with updated total
            
            if self.remove_another():
                continue
            break
                

    def remove_another(self):
        while True:
            another = input("{:^}".format("Would you like to remove another booking? (y/n):\n")).strip().lower()
            
            if another not in ['y', 'n']:
                print("{:^}".format("Invalid input. Please enter 'y' for yes, 'n' for no, or 'x' to cancel.\n"))
                continue

            if another == 'y':
                return True
            
            return False
        
    def __str__(self): #Playing with string formatting to make a nice looking receipt
        if not self.receipt:
            return "No bookings made yet. Receipt is empty.\n"
        
       
        info = "{:^100}".format("Booking Receipt\n")
        
        for movie, tickets in self.receipt[0].items():
            line = "{:^}".format(f"Title: {movie} | Tickets Booked: {sum(tickets)} | Ticket Price: ${self.movies[movie]:.2f} | Subtotal: ${sum(tickets) * self.movies[movie]:.2f}\n")
            info += "\n" + line + "\n"
        
         
        total_line = "{:>50}".format(f"'Total Amount Due: ${self.receipt[1]:.2f}\n")
        info += "\n" + total_line + "\n"
        
        return info
    
    def disp_bookings(self):
        print("{:^50}".format("Current Bookings\n"))
        print("{:^25}{:^25}".format("Movie Title", "Number of Tickets\n"))
        for k,v in self.bookings.items():
            print(f"{k:^25}:{sum(v):^25}")
            

def get_theater_details():
    while True:
        name = input("{:^}".format("Enter theater name:\n")).strip()
        
        if name == "":
            print("{:^}".format("Theater name required. Please try again\n"))
            continue
        
        if name.isdigit():
            print("{:^}".format("Invalid name. Please try again\n"))
            continue
        break

    while True:
        location = input("{:^}".format("\nEnter theater location:\n")).strip()
        
        if location == "":
            print("{:^}".format("Theater location required. Please try again.\n"))
            continue
        break
    
    return (name, location)

def create_system(arg1):
    t = Theater(arg1[0], arg1[1])
    bs = BookingSystem(arg1[0], arg1[1])
    return t, bs
    
def menu():
    
    menu = {
        '1': "Update Theater Name",
        '2': "Update Theater Location",
        '3': "Add Booking",
        '4': "Remove Booking",
        '5': "View Receipt",
        '6': "Exit"
    }
    
    disp_menu(menu)
    
    return menu

def disp_menu(menu_dict):
    print("{:^35}".format("-Menu-\n"))
    for key, value in menu_dict.items():
        print(f"{key:^3}| {value:^30}")
    print()

def menu_choice(menu_dict):
    while True:
        choice = input("Enter your choice (1-6):\n").strip()
        if choice not in menu_dict:
            print("Invalid choice. Please try again.\n")
            continue
        return choice
    
def route_selection(theater, booking_system):

    while True:
        choice = menu_choice(menu()) 
        if choice == '1':
            theater.update_name()
            continue 
        elif choice == '2':
            theater.update_location()
            continue
        elif choice == '3':
            booking_system.add_booking()
            continue                
        elif choice == '4':
            booking_system.remove_booking()
            continue
        elif choice == '5':
            print(booking_system)
            continue
        elif choice == '6':
            print("Thank you for using the Movie Booking System. Goodbye!")
            return False
        
            
    
def main():
        print("\nWelcome to the Movie Booking System!\n")
        syst = create_system(get_theater_details()) #Create theater and booking system objects. create_system returns a tuple
        print(syst[0]) #Display theater info
        if not route_selection(syst[0], syst[1]):
            return
            
        
                 
    
    
    


        
if __name__ == "__main__":
    main()