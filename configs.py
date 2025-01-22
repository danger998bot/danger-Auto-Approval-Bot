# Don't Remove Credit @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot @Tech_VJ
# Ask Doubt on telegram @KingVJ01


from os import path, getenv

class Config:
    API_ID = int(getenv("API_ID", "25325861"))
    API_HASH = getenv("API_HASH", "d945b8c295a892802530fe808bde0d76")
    BOT_TOKEN = getenv("BOT_TOKEN", "7523038603:AAGuX_1paZCZSZrzN-oAcpOZPXnL-94fjJQ")
    # Your Force Subscribe Channel Id Below 
    CHID = int(getenv("CHID", "-1002354912335")) # Make Bot Admin In This Channel
    # Admin Or Owner Id Below
    SUDO = list(map(int, getenv("SUDO", "7830741296").split()))
    MONGO_URI = getenv("MONGO_URI", "mongodb+srv://sibasahu036:U2SRRz3W1Q7lZLwK@cluster0.7qoey.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    
cfg = Config()

# Don't Remove Credit @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot @Tech_VJ
# Ask Doubt on telegram @KingVJ01
