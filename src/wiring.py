import config
from util.http_client import HttpClient
from services.ice_fire_api_service import IceFireApiService

def http_client(timeout):
    return HttpClient(timeout)

def ice_fire_service():
    return IceFireApiService(http_client(config.ICEFIRE_API_TIMEOUT))