from fastapi import FastAPI
from pydantic import BaseModel

from backend.api.quarn_api import get_chapter_name, fetch_chapter_info, get_random_chapter_id, get_english_translations

from backend.ml import giveSentanceOnVibe, giveVibeAdvice, giveRandomAyah, generateResources, analyze

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
async def get_vibe(vibe: str):
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

    This endpoint selects a random chapter (Surah) from the Quran database,
    fetches its text, processes it using a machine learning model to extract 
    a single relevant Ayah, and returns the Ayah along with the chapter name.

    Returns:
        dict: A dictionary containing:
            - name (str): The name of the chapter (Surah).
            - ayah (str): The processed Ayah relevant to the user's vibe.
    """
    
    chapterID = get_random_chapter_id()
    text = fetch_chapter_info(chapterID)
    res = giveRandomAyah(text)
    name = get_chapter_name(text)
  
    return {"name": name, "ayah":res}
    
    
   

@app.post("/analyze")
async def analyze_ayah(chapterID: int):
    """
    Analyzes a specific Ayah to determine its most impactful message.

    This function uses the user's vibe and an external AI model (e.g., OpenAI) to analyze 
    a given Ayah and extract its core meaning. This could provide a deeper, context-specific 
    interpretation to the user.
    """
    
    if chapterID < 1 or chapterID > 113:
        chapterID = 1
    
    text = fetch_chapter_info(chapterID)
    name = get_chapter_name(text)
    res = analyze(text)
    ai_links = generateResources(text)
    links = ai_links.strip("\n")
    return {"name":name, "analysis":res, "links": links}


@app.post("/chapter")
async def get_chapter(chapter_id: int):
    """
    Retrieves information for a specific chapter by its ID.

    This endpoint provides details about a particular chapter, such as its name, 
    number of verses, and themes. Useful for when a user wants to explore a specific chapter.
    """
    text = fetch_chapter_info(chapter_id)
    name = get_chapter_name(text)
    result = giveRandomAyah(text)
    
    return {"name": name, "text":result}
    
    



