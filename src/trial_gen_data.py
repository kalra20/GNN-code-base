import random
import pandas as pd
import numpy as np
from faker import Faker

def generate_data():
    fake = Faker()

    # Number of entities
    num_customers = 50
    num_merchants = 20
    num_drivers = 15

    # Helper functions
    def random_time_of_day():
        return random.choice(['Morning', 'Afternoon', 'Evening', 'Night'])

    def random_zipcode():
        return fake.zipcode()

    def random_cuisine():
        return random.choice(['Italian', 'Chinese', 'Indian', 'Mexican', 'American', 'Thai'])

    # Generate Customers
    customers = []
    for i in range(num_customers):
        customers.append({
            'customer_id': f'CUST_{i+1}',
            'joining_date': fake.date_this_decade(),
            'location_zipcode': random_zipcode(),
            'no_of_orders_last_30_days': random.randint(0, 20),
            'no_of_clicks_at_merchants': random.randint(0, 100),
            'average_sessions_per_day': round(random.uniform(1, 10), 2),
            'most_active_time_of_the_day': random_time_of_day(),
            'primary_cuisine_preference': random_cuisine()
        })

    # Generate Merchants
    merchants = []
    for i in range(num_merchants):
        merchants.append({
            'merchant_id': f'MER_{i+1}',
            'merchant_name': fake.company(),
            'location_zipcode': random_zipcode(),
            'no_of_orders_last_30_days': random.randint(0, 200),
            'no_of_clicks_at_the_merchant': random.randint(50, 500),
            'average_visits_per_day': round(random.uniform(5, 50), 2),
            'most_active_time_of_the_day': random_time_of_day(),
            'cuisines_served': ', '.join(random.sample([random_cuisine() for _ in range(5)], k=random.randint(1, 3)))
        })

    # Generate Drivers
    drivers = []
    for i in range(num_drivers):
        drivers.append({
            'driver_id': f'DR_{i+1}',
            'no_of_orders_last_deliverd_30_days': random.randint(10, 300),
            'no_of_merchants_visited': random.randint(5, 50),
            'average_deliveries_per_day': round(random.uniform(2, 15), 2),
            'most_active_time_of_the_day': random_time_of_day(),
            'average_delivery_time': round(random.uniform(15, 60), 2), # in minutes
            'average_daily_incentives': round(random.uniform(20, 100), 2) # in currency units
        })

    # Convert to DataFrames for easy viewing and insertion
    customers_df = pd.DataFrame(customers)
    merchants_df = pd.DataFrame(merchants)
    drivers_df = pd.DataFrame(drivers)

    # print("Customers Data:")
    # print(customers_df.head())

    # print("\nMerchants Data:")
    # print(merchants_df.head())

    # print("\nDrivers Data:")
    # print(drivers_df.head())

    relationships = []

    # Customer to Merchant relationships (Visits/Orders)
    for customer in customers:
        for _ in range(random.randint(1, 5)):  # Each customer might interact with 1 to 5 merchants
            merchant = random.choice(merchants)
            relationships.append({
                'customer_id': customer['customer_id'],
                'merchant_id': merchant['merchant_id'],
                'relationship': random.choice(['VISITS', 'ORDERS'])
            })

    # Driver to Merchant relationships (Delivers)
    for driver in drivers:
        for _ in range(random.randint(1, 10)):  # Each driver might interact with 1 to 10 merchants
            merchant = random.choice(merchants)
            relationships.append({
                'driver_id': driver['driver_id'],
                'merchant_id': merchant['merchant_id'],
                'relationship': 'DELIVERS'
            })

    # Customer to Driver relationships (Receives)
    for customer in customers:
        for _ in range(random.randint(1, 3)):  # Each customer might receive deliveries from 1 to 3 drivers
            driver = random.choice(drivers)
            relationships.append({
                'customer_id': customer['customer_id'],
                'driver_id': driver['driver_id'],
                'relationship': 'RECEIVES'
            })

    # Print a few generated relationships for verification
    # print("Sample Relationships:")
    # for rel in relationships[:5]:
    #     print(rel)

    return customers_df, merchants_df, drivers_df, relationships

    