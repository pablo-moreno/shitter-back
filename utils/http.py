import re
import requests


class HttpService(object):
    model = None
    serializer_class = None
    api_url = ''
    authorization_header = 'Bearer'
    authorization_header_name = 'Authorization'
    default_http_client = requests

    def __init__(self):
        self.token = None
        self.headers = dict()
        self.http = self.default_http_client

    def get_token(self):
        return self.token

    def set_token(self, token):
        self.token = token

    def get_serializer_class(self):
        return self.serializer_class

    def get_model(self):
        return self.model

    def pluralize(self, text: str):
        return f'{text}ies' if text[-1] == 'y' else f'{text}s'

    def get_model_slug(self):
        slug = re.sub('(?<=.)([A-Z]+)', '-\\1', self.get_model().__name__).lower()
        return self.pluralize(slug)

    def get_url(self, pk='', *extra_params):
        params = (self.api_url, self.get_model_slug(), str(pk), *extra_params)
        return '/'.join([param for param in params if param != ''])

    def get_headers(self):
        token = self.get_token()
        if token:
            headers = {
                self.authorization_header_name: f'{self.authorization_header} {token}',
                **self.headers,
            }
            return headers
        return self.headers

    def serialize(self, instance, many=False):
        serializer = self.get_serializer_class()
        return serializer(instance, many=many).data

    def deserialize(self, data, many=False):
        serializer = self.get_serializer_class()
        return serializer(data=data, many=many)

    def get_response_data(self, response):
        if response.status_code not in range(200, 300):
            raise Exception(f'Error {response.status_code}')

        data = response.json()
        return data, isinstance(data, list)

    def list(self):
        response = self.http.get(self.get_url(), headers=self.get_headers())
        data, many = self.get_response_data(response)
        return self.deserialize(data=data, many=many)

    def retrieve(self, pk):
        response = self.http.get(self.get_url(pk), headers=self.get_headers())
        data, many = self.get_response_data(response)
        return self.deserialize(data=data, many=many)

    def post(self, data, query=''):
        response = self.http.post(self.get_url(), data=data, headers=self.get_headers(), json=query)
        data, many = self.get_response_data(response)
        return self.deserialize(data=data, many=many)

    def put(self, pk, data):
        response = self.http.put(self.get_url(pk), data=data, headers=self.get_headers())
        data, many = self.get_response_data(response)
        return self.deserialize(data=data, many=many)

    def delete(self, pk):
        response = self.http.delete(self.get_url(pk), headers=self.get_headers())
        data, many = self.get_response_data(response)
        return self.deserialize(data=data, many=many)
