class Configuration(object):
    SERVER = "192.168.1.247"
    PORT = 8082
    ENDPOINT = "ws/home/overview"

    LANG = "en_us"
    TOKEN = "25493ca9-9c20-45fd-924f-58176efa54a2"
    
    
    def GenerateWebsocktUri(self):
        return f"ws://{self.SERVER}:{self.PORT}/{self.ENDPOINT}"