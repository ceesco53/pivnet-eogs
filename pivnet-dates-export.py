import requests
import csv
from datetime import datetime

# Define the products array.  Put in the slug names.
products = ['apm', 'pivotal-container-service', 'ops-manager', 'elastic-runtime', 'cloud-service-broker-azure', 'p-metric-store', 'p_spring-cloud-services', 'p-isolation-segment', 'p-rabbitmq', 'p-redis', 'p-scheduler', 'pivotal-mysql', 'pivotal-telemetry-om', 'pivotal_single_sign-on_service', 'p-healthwatch']

# Define the eogs_array
eogs_array = []

# Send a GET request to the API URL for each product in the products array
for product in products:
    response = requests.get(f"https://network.tanzu.vmware.com/api/v2/products/{product}/releases")
    data = response.json()

    # Extract the data we need from the JSON response and append it to the eogs_array
    for release in data['releases']:
        eog_data = {
            'product': product,
            'version': release.get('version'),
            'release_date': release.get('release_date'),
            'end_of_support_date': release.get('end_of_support_date'),
            'days_to_eog': None
        }

        # Calculate the difference in days between the end_of_support_date and today's date
        if eog_data['end_of_support_date']:
            eog_data['days_to_eog'] = (datetime.strptime(eog_data['end_of_support_date'], '%Y-%m-%d') - datetime.today()).days
        
        eogs_array.append(eog_data)

# Export the eogs_array to a CSV file
with open('eogs_data.csv', mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=['product', 'version', 'release_date', 'end_of_support_date', 'days_to_eog'])
    writer.writeheader()
    for eog_data in eogs_array:
        writer.writerow(eog_data)
