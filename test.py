import requests

# Replace with your actual API key and channel ID
api_key = '8A9REPRTD4IP4G6L'
channel_id = '2472958'

# Function to overwrite data with null values
def overwrite_data_with_null():
    # Retrieve the current data
    response = requests.get(f'https://api.thingspeak.com/channels/{channel_id}/feeds.json', params={'api_key': api_key, 'results': 1000})
    if response.status_code == 200:
        feeds = response.json().get('feeds', [])
        for feed in feeds:
            # Create a payload with null values for all fields
            payload = {'api_key': api_key}
            for field in range(1, 9):  # Assuming there are 8 fields
                payload[f'field{field}'] = ''

            # Update the data point with null values
            update_url = f'https://api.thingspeak.com/update.json'
            response = requests.post(update_url, data=payload)
            if response.status_code == 200:
                print(f'Successfully updated entry ID {feed["entry_id"]} with null.')
            else:
                print(f'Failed to update entry ID {feed["entry_id"]}. Status code: {response.status_code}, Response: {response.text}')
    else:
        print(f'Failed to retrieve data. Status code: {response.status_code}, Response: {response.text}')

# Call the function to overwrite data with null
overwrite_data_with_null()