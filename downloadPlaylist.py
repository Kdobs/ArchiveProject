#Currently brocken due to the library

#Program will archive the every video in a playlist to archive multiple videos at a time
#instructions for using the program
# install the packages fastapi pytube and uvicorn (pip install fastapi uvicorn pytube)
# Enter this command into the terminal:
#   uvicorn downloadPlaylist:app --reload
#Enter a curl command in the terminal with the following format:
#   curl "http://127.0.0.1:8000/download?url=<https://www.youtube.com/playlist?list=PLTv_eI6E4XUQaU1jrPQC_lAD3PrIQg0pb&path=F:\YoutubeArchive\AlphaOxtrot&resolution=720p"

from fastapi import FastAPI, HTTPException, Query
from pytube import Playlist
import os
# create instance of the fast API
app = FastAPI() 
@app.get("/download")
def download_Playlist(url: str = Query(description="URL of the playlist: "),
    path: str = Query(description="Path to the storage location: "),
    resolution: str = Query(default="720p", description="Video resolution(Ex: 720p, 1080p): ")):
    try:
        #check the path for the storage location
        if not os.path.exists(path):
            os.makedirs(path)
        
        #create the playlist object
        playlist = Playlist(url)
        if not playlist.videos:
            raise ValueError("Playlist is empty")
        
        #for storing the videos that downloaded
        results = []
        
        #Loop through the video objects
        for count, video in enumerate(playlist.videos, start=1):
            try:
                stream = video.streams.filter(res=resolution, file_extension="mp4").first()
                if not stream:
                    results.append(f"Video #{count}: Resolution '{resolution}' not available.")
                    continue
                stream.download(path)
                results.append(f"Video #{count}: Downloaded successfully.")
            except Exception as e:
                results.append(f"Video #{count}: Error - {str(e)}")
        return{"message": "Download complete", "results": results}
    except ValueError as ve:
         raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
         raise HTTPException(status_code=500, detail=str(e))


        