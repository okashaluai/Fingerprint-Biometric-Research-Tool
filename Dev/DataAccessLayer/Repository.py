from pymongo import  MongoClient


class Repository:
    def __init__(self):
        self.db_client = MongoClient('localhost', 27017)
    def get_playground(self):
        return ''

    def add_experiment(self, experiment):
        database = self.db_client['programdb']
        experiments_collection = database['experiments']
        experiments_collection.insert_one(experiment)
    def delete_experiment(self, experiment_id : int):
        database = self.db_client['programdb']
        experiments_collection = database['experiments']

    def add_operation(self, operation):
        database = self.db_client['programdb']
        operations_collection = database['operations']
        operations_collection.insert_one(operation)
        self.add_asset(operation.operation_input)
        self.add_asset(operation.operation_output)

    def delete_operation(self, experiment_id : int, operation_id : int):
        database = self.db_client['programdb']
        operations_collection = database['operations']
        
    def add_asset(self, asset):
        database = self.db_client['programdb']
        assets_collection = database['assets']
        assets_collection.insert_one(asset)
    def delete_asset(self):
        database = self.db_client['programdb']
        assets_collection = database['assets']


