

class Profile:
    country: str

    display_name: str
    email:str
    uri: str

    subscription_level: str
    
    scope: str

    def __init__(self, raw_data: dict, spotify_scope: str) -> None:
        self.country = raw_data["country"]
        
        self.display_name = raw_data["display_name"]
        self.email = raw_data["email"]
        self.uri = raw_data["uri"]

        self.subscription_level = raw_data["product"]
        self.scope = spotify_scope
