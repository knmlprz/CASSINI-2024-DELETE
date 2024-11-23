import json

# Load JSON data from files
def load_data(user_file, shelter_file):
    with open(user_file, 'r') as user_file:
        users_data = json.load(user_file)
    with open(shelter_file, 'r') as shelter_file:
        shelter_data = json.load(shelter_file)
    return users_data, shelter_data

# Function to assign a user to a shelter
def assign_user_to_shelter(users_data, shelter_data, user_pesel, shelter_id):
    # Find the user by PESEL
    user = next((u for u in users_data if u['pesel'] == user_pesel), None)
    if not user:
        print("User not found!")
        return
    
    # Find the shelter by ID
    shelter = next((s for s in shelter_data if s['id'] == shelter_id), None)
    if not shelter:
        print("Shelter not found!")
        return
    
    # Check if shelter has available places
    if shelter['availablePlaces'] <= 0:
        print("No available places in the shelter!")
        return
    
    # Assign user to shelter
    shelter['users'].append(user['pesel'])
    shelter['availablePlaces'] -= 1
    user['shelter'] = shelter_id
    print(f"Assigned {user['firstName']} {user['lastName']} to shelter {shelter['name']}.")

# Function to display the number of users in a shelter
def display_shelter_user_count(shelter_data, shelter_id):
    # Find the shelter by ID
    shelter = next((s for s in shelter_data if s['id'] == shelter_id), None)
    if not shelter:
        print("Shelter not found!")
        return
    
    # Get the number of users in the shelter
    user_count = len(shelter['users'])
    print(f"Shelter '{shelter['name']}' currently has {user_count} user(s).")

# Example usage
user_file_path = 'users.json'
shelter_file_path = 'shelters.json'

# Load data
users_data, shelter_data = load_data(user_file_path, shelter_file_path)

# Assign a user to a shelter
assign_user_to_shelter(users_data, shelter_data, "02232800863", 1)

# Display the updated user count for the shelter
display_shelter_user_count(shelter_data, 1)

# Optionally save updated data back to files
# with open(user_file_path, 'w') as user_file:
#     json.dump(users_data, user_file, indent=4)
# with open(shelter_file_path, 'w') as shelter_file:
#     json.dump(shelter_data, shelter_file, indent=4)
