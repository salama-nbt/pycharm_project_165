import uuid
from mep_core_api_client import Configuration, API

# Configuration data for API client instance, don't change!
# conf = Configuration(
#     username="hw-team@nbt.ag",
#     password="eMitPNKZ7T",
#     auth_url="https://stg-auth.nbt-dev.ag/",
#     service_url="https://stg-api.nbt-dev.ag/"
# )

conf = Configuration(
    username="tenant@nbt.ag",
    password="test123T!",
    auth_url="http://platform.mep/auth-api",
    service_url="http://platform.mep/api"
)

api = API(config=conf)


# Example usage: python main.py
if __name__ == "__main__":
    # specify your device id here
    device_id = "350916066834212123123"

    # it's PK of PrometheusXL device class from platform, don't change!
    device_class_id = uuid.UUID("065b8ee3-664a-7bb9-8000-f160988268b1")

    # Call API to get device or create it in case it doesn't exist on platform
    success, error = api.inventory.device.get_or_create_device(
        device_id=device_id,
        device_class_id=device_class_id
    )
    if success:
        # You can use get_device_certs without get_or_create_device if you're sure device created
        certificates_url = api.inventory.device.provision_device(device_id)
        print(certificates_url["ca"])
        print(certificates_url["certChain"])
        print(certificates_url["key"])
    else:
        print(error)
