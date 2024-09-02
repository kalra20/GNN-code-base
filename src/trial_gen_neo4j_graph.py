from neo4j import GraphDatabase
from trial_gen_data import generate_data
# Replace with your Neo4j credentials
NEO4J_URI = "bolt://localhost:7687"  # Default URI
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "neo4j123"

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

customers_df, merchants_df, drivers_df, relationships = generate_data()
def create_customers(tx, customers):
    for _, row in customers.iterrows():
        tx.run("""
            CREATE (c:Customer {
                customer_id: $customer_id,
                joining_date: $joining_date,
                location_zipcode: $location_zipcode,
                no_of_orders_last_30_days: $no_of_orders_last_30_days,
                no_of_clicks_at_merchants: $no_of_clicks_at_merchants,
                average_sessions_per_day: $average_sessions_per_day,
                most_active_time_of_the_day: $most_active_time_of_the_day,
                primary_cuisine_preference: $primary_cuisine_preference
            })
        """, **row)

def create_merchants(tx, merchants):
    for _, row in merchants.iterrows():
        tx.run("""
            CREATE (m:Merchant {
                merchant_id: $merchant_id,
                merchant_name: $merchant_name,
                location_zipcode: $location_zipcode,
                no_of_orders_last_30_days: $no_of_orders_last_30_days,
                no_of_clicks_at_the_merchant: $no_of_clicks_at_the_merchant,
                average_visits_per_day: $average_visits_per_day,
                most_active_time_of_the_day: $most_active_time_of_the_day,
                cuisines_served: $cuisines_served
            })
        """, **row)

def create_drivers(tx, drivers):
    for _, row in drivers.iterrows():
        tx.run("""
            CREATE (d:Driver {
                driver_id: $driver_id,
                no_of_orders_last_deliverd_30_days: $no_of_orders_last_deliverd_30_days,
                no_of_merchants_visited: $no_of_merchants_visited,
                average_deliveries_per_day: $average_deliveries_per_day,
                most_active_time_of_the_day: $most_active_time_of_the_day,
                average_delivery_time: $average_delivery_time,
                average_daily_incentives: $average_daily_incentives
            })
        """, **row)

def create_relationships(tx, relationships):
    for rel in relationships:
        if rel['relationship'] in ['VISITS', 'ORDERS']:
            tx.run("""
                MATCH (c:Customer {customer_id: $customer_id}), (m:Merchant {merchant_id: $merchant_id})
                CREATE (c)-[r:%s]->(m)
            """ % rel['relationship'], customer_id=rel['customer_id'], merchant_id=rel['merchant_id'])
        
        elif rel['relationship'] == 'DELIVERS':
            tx.run("""
                MATCH (d:Driver {driver_id: $driver_id}), (m:Merchant {merchant_id: $merchant_id})
                CREATE (d)-[r:DELIVERS]->(m)
            """, driver_id=rel['driver_id'], merchant_id=rel['merchant_id'])
        
        elif rel['relationship'] == 'RECEIVES':
            tx.run("""
                MATCH (c:Customer {customer_id: $customer_id}), (d:Driver {driver_id: $driver_id})
                CREATE (c)-[r:RECEIVES]->(d)
            """, customer_id=rel['customer_id'], driver_id=rel['driver_id'])

# Insert data into Neo4j
with driver.session() as session:
    session.write_transaction(create_customers, customers_df)
    session.write_transaction(create_merchants, merchants_df)
    session.write_transaction(create_drivers, drivers_df)

driver.close()

print("Data successfully inserted into Neo4j.")

# Insert relationships into Neo4j
with driver.session() as session:
    session.write_transaction(create_relationships, relationships)

driver.close()

print("Relationships successfully inserted into Neo4j.")