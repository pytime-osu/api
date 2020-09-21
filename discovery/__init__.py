from django.conf import settings
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import DiscoveryV1


class DiscoveryClient:
    def __init__(self):
        self.authenticator = IAMAuthenticator(settings.DISCOVERY_API_KEY)
        self.client = DiscoveryV1(
            version='2019-04-30',
            authenticator=self.authenticator
        )
        self.client.set_service_url(service_url=settings.DISCOVERY_SERVICE_URL)
        self.environment = self.collection = None

    def init_environment(self, name):
        response = self.client.create_environment(name=name)
        return response.get_result()

    def environments(self):
        response = self.client.list_environments()
        result = response.get_result()
        return [env for env in result['environments'] if not env['read_only']]

    def delete_environments(self):
        environments = self.environments()
        for env in environments:
            self.client.delete_environment(environment_id=env['environment_id'])

    def create_collection(self, environment_id, name):
        response = self.client.create_collection(environment_id=environment_id, name=name)
        return response.get_result()

    def delete_collection(self, environment_id, collection_id):
        self.client.delete_collection(environment_id=environment_id, collection_id=collection_id)

    def setup(self, environment_name, collection_name):
        self.delete_environments()
        self.environment = self.init_environment(name=environment_name)
        self.collection = self.create_collection(
            environment_id=self.environment['environment_id'], name=collection_name)

    def add_document(self, file, filename=None):
        return self.client.add_document(
            environment_id=self.environment['environment_id'],
            collection_id=self.collection['collection_id'],
            file=file,
            filename=filename).get_result()
