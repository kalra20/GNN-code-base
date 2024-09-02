import json

def config():

    with open('config.json', 'r') as file:
        config = json.load(file)

    NEO4J_URI = config['neo4j']['uri']
    NEO4J_USER = config['neo4j']['user']
    NEO4J_PASSWORD = config['neo4j']['password']

    return NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD