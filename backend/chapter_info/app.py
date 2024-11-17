from fastapi import FastAPI
from pydantic import BaseModel

from backend.api.quarn_api import get_chapter_name, fetch_chapter_info, get_random_chapter_id, get_english_translations

from backend.ml import giveSentanceOnVibe, giveVibeAdvice

"""
Use POST to send data, and GET to retrieve data.
"""



app = FastAPI()
class VibeRequest(BaseModel):
    vibe: str
    
    
class ChapterRequest(BaseModel):
    chpater_id: int
    
    
    
    
# Sending via JSON
@app.post("/vibe") 
async def get_vibe(vibe: VibeRequest):
    """
    Retrieves the user's current vibe and returns relevant information.
    
    This endpoint assesses the user's current mood or "vibe" and
    returns details or suggestions based on it.
    
    send to ML
    """
    # If the vibe is ever empty set a defult vibe 
    if vibe == "" or not vibe:
        return {"vibe":"Feeling Netural"}
    
    # PROCESS ML MODEL model here call the function right here
    #  call the function and pass the proceses vibe here 
    res = giveVibeAdvice(vibe)
   
    
    return {"vibe": res}


# Get path params must be Scaler so (int, str, etc.). and not Pydantic only POST and PUT can be those
@app.get("/ayah/")
async def get_ayah(chapter_id: int, vibe:str):
    """
    Sends a curated Ayah.

    This endpoint generates a meaningful Ayah (verse) for the user by:
    1. Calling `get_vibe` to assess the user's current emotional state.
    2. Passing this vibe and a randomly selected Ayah to the `getText` function 
       (from the OpenAIAPI module), which processes and returns the most impactful text.
    
    **Note**: Ensure that all inputs and outputs adhere to the defined Pydantic model specifications.
    """
    if chapter_id < 1 or chapter_id > 113:
        chapter_id = 1
        
    if not vibe:
        vibe = "Netrual"
    
    
    chapterID = get_random_chapter_id()
    text = fetch_chapter_info(chapterID)
    name = get_chapter_name(text)
    translation = get_english_translations(text)
    

    # Allows us to get the chapter name and the text
    # ALl we need to do is Curate the ml model
    
    res = giveSentanceOnVibe(vibe, translation)
    print(res)
    
    return {"name":name, "text":res}
    
    
@app.get("/ayah/random")
async def get_random_ayah():
    """
    Retrieves a random Ayah.

    This endpoint selects and returns a random Ayah from the Quran database.
    Useful for providing users with a new Ayah each time or when they are exploring.
    """
    
  
    
    # CALL ML MODEL RIGHT HERE 
    # Replace the text
    # return {"name": name, "text":text, "Number":chapter_id}
    
    pass
    
    
   

@app.post("/ayah/analyze")
async def analyze_ayah():
    """
    Analyzes a specific Ayah to determine its most impactful message.

    This function uses the user's vibe and an external AI model (e.g., OpenAI) to analyze 
    a given Ayah and extract its core meaning. This could provide a deeper, context-specific 
    interpretation to the user.
    """
    pass

@app.get("/vibe/recommendation")
async def get_recommendation():
    """
    Provides recommendations based on the user's current vibe.

    Using the user's vibe, this function suggests specific Ayahs, prayers, or resources 
    that may help them in their current state.
    """
    pass

@app.get("/chapters")
async def get_all_chapters():
    """
    Retrieves information about all chapters.

    This endpoint fetches details about each chapter in the Quran, which can be used 
    to help users explore different chapters or find specific content.
    """
    pass

@app.get("/chapter/{chapter_id}")
async def get_chapter(chapter_id: int):
    """
    Retrieves information for a specific chapter by its ID.

    This endpoint provides details about a particular chapter, such as its name, 
    number of verses, and themes. Useful for when a user wants to explore a specific chapter.
    """
    pass

@app.get("/ayah/{ayah_id}")
async def get_ayah_by_id(ayah_id: int):
    """
    Retrieves a specific Ayah by its ID.

    This endpoint allows users to retrieve a particular Ayah directly by specifying its ID,
    enabling direct access to verses they want to revisit.
    """
    pass

@app.post("/vibe/update")
async def update_user_vibe():
    """
    Updates the user's current vibe.

    This endpoint accepts data from the user to update their current vibe, allowing 
    the app to deliver more personalized recommendations and Ayahs in the future.
    """
    pass


# Take it via JSON
@app.post("/feedback") 
async def get_user_feedback():
    """
    Collects user feedback on Ayah recommendations or vibe-based suggestions.

    This endpoint allows users to submit feedback on the Ayahs they receive, 
    which could be used to improve the recommendation engine or the vibe analysis.
    """
    pass