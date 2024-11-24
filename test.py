import json

# Load JSON data from files
def load_data(user_file, shelter_file):
    with open(user_file, 'r') as user_file:
        users_data = json.load(user_file)
    with open(shelter_file, 'r') as shelter_file:
        shelter_data = json.load(shelter_file)
    return users_data, shelter_data

# Function to validate JSON data
def validate_data(users_data, shelter_data):
    # Check if required fields are present in users
    for user in users_data:
        if 'pesel' not in user or 'firstName' not in user or 'lastName' not in user:
            print(f"User data missing required fields: {user}")
    
    # Check if required fields are present in shelters
    for shelter in shelter_data:
        if 'id' not in shelter or 'name' not in shelter or 'availablePlaces' not in shelter or 'users' not in shelter:
            print(f"Shelter data missing required fields: {shelter}")

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

# Function to remove a user from a shelter
def remove_user_from_shelter(users_data, shelter_data, user_pesel):
    # Find the user by PESEL
    user = next((u for u in users_data if u['pesel'] == user_pesel), None)
    if not user:
        print("User not found!")
        return

    # Check if the user is assigned to a shelter
    if 'shelter' not in user or user['shelter'] is None:
        print(f"User {user['firstName']} {user['lastName']} is not assigned to any shelter.")
        return
    
    # Find the shelter by the ID in user's record
    shelter_id = user['shelter']
    shelter = next((s for s in shelter_data if s['id'] == shelter_id), None)
    if not shelter:
        print("Shelter not found!")
        return
    
    # Remove the user from the shelter
    shelter['users'].remove(user_pesel)
    shelter['availablePlaces'] += 1
    user['shelter'] = None
    print(f"Removed {user['firstName']} {user['lastName']} from shelter {shelter['name']}.")


# Function to display users in a specific shelter
def display_users_in_shelter(users_data, shelter_data, shelter_id):
    # Find the shelter by ID
    shelter = next((s for s in shelter_data if s['id'] == shelter_id), None)
    if not shelter:
        print("Shelter not found!")
        return
    
    # Find users assigned to this shelter
    user_list = [u for u in users_data if u.get('shelter') == shelter_id]
    if not user_list:
        print(f"No users currently assigned to shelter '{shelter['name']}'.")
        return

    # Display users
    print(f"Users assigned to shelter '{shelter['name']}':")
    for user in user_list:
        print(f"- {user['firstName']} {user['lastName']} (PESEL: {user['pesel']})")

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

# Validate data
validate_data(users_data, shelter_data)

# Assign a user to a shelter
assign_user_to_shelter(users_data, shelter_data, "02232800863", 1)

# Display users in a specific shelter
display_users_in_shelter(users_data, shelter_data, 1)

# Remove a user from a shelter
remove_user_from_shelter(users_data, shelter_data, "02232800863")

# Display the updated user count for the shelter
display_shelter_user_count(shelter_data, 1)

# Optionally save updated data back to files
# with open(user_file_path, 'w') as user_file:
#     json.dump(users_data, user_file, indent=4)
# with open(shelter_file_path, 'w') as shelter_file:
#     json.dump(shelter_data, shelter_file, indent=4)
