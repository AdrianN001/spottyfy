from threading import Thread

from spoti import SpotifyClient
import os
from dotenv import load_dotenv
from tui import GraphicClient
import readchar


import time

load_dotenv()


CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']


def main(_args: list[str]) -> None:
    spoti_client = SpotifyClient(CLIENT_ID, CLIENT_SECRET)
    spoti_client.fetch_current_song()    

    


    graphic_client = GraphicClient()
    graphic_client.attach_spotify_client(spoti_client)
   


    graphic_client.run()



if __name__ == "__main__":
    main([])
