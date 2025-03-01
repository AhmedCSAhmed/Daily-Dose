import google.generativeai as genai
import os
def configure():
    """
    Configures the Google Generative AI client using an API key stored in the environment variables.

    Raises:
        KeyError: If the environment variable 'GOOGLE_GENERATIVE_AI_KEY' is not set.
    """
    
    genai.configure(api_key=os.environ["GOOGLE_GENERATIVE_AI_KEY"])




configure()

def giveSentanceOnVibe(vibe, text):
    
    """
    Generates a single sentence from the provided Quranic text that aligns with the user's vibe.

    Args:
        vibe (str): The user's current vibe or mood.
        text (str): The Quranic ayahs to reference.

    Returns:
        str: A single sentence from the Quranic ayahs that best matches the user's vibe.

    Raises:
        AttributeError: If the response object does not contain the expected structure.
    """
    
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(
    f"Based on the provided Quranic ayahs: {text}, use the text I provided as reference to identify and return a single sentence that best aligns with the user's current vibe: '{vibe}'. Use the ayahs exactly as they are. DO NOT CHANGE THEM. Select the sentence that is most relevant."
)
    return str(response.candidates[0].content.parts[0].text)


def giveVibeAdvice(vibe):
    """
    Generates a short, meaningful, and unique response based on the user's vibe.

    Args:
        vibe (str): The user's current vibe or mood.

    Returns:
        str: A short and unique response tailored to the user's vibe.

    Raises:
        AttributeError: If the response object does not contain the expected structure.
    """
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(
f"The user's current vibe is '{vibe}'. Generate a short, meaningful, and unique response that aligns with this vibe, as if you're speaking casually with a friend. Keep it concise, avoid newline characters, and feel free to include emojis where they add value or emphasis. Ensure each response is highly unique and never reuse any previous messages.")    
    return str(response.candidates[0].content.parts[0].text)




def giveRandomAyah(text):
    
    """
    Generates a single sentence from the provided Quranic text that aligns with the user's vibe.

    Args:
        text (str): The Quranic ayahs to reference.

    Returns:
        str: A single sentence from the Quranic ayahs that best matches the user's vibe, with an emoji added at the end.

    Raises:
        AttributeError: If the response object does not contain the expected structure or parts.
    """
    
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(
            f"Based on the provided Quranic ayahs: {text}, use the text I provided as reference to identify and return a single sentence that best aligns with the user's current vibe: 'which we don't know so take a guess'. Use the ayahs exactly as they are. DO NOT CHANGE THEM. Select the sentence that is most relevant. please addd an emohi at the end"

    )
    return str(response.candidates[0].content.parts[0].text)



def generateResources(text):
    
    """
    Generates a single sentence from the provided Quranic text that aligns with the user's vibe.

    Args:
        text (str): The Quranic ayahs to reference.

    Returns:
        str: A single sentence from the Quranic ayahs that best matches the user's vibe, with an emoji added at the end.

    Raises:
        AttributeError: If the response object does not contain the expected structure or parts.
    """
    
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(
       f"Based on the provided Quranic ayahs: {text}, suggest 1 reputable link directly related to the themes or context of these ayahs (e.g., https://example.com/resource) with no additional explanation or commentary and no \\n character at all"
        )
    return str(response.candidates[0].content.parts[0].text)




def analyze(text):
    
    """
    Generates a single sentence from the provided Quranic text that aligns with the user's vibe.

    Args:
        text (str): The Quranic ayahs to reference.

    Returns:
        str: A single sentence from the Quranic ayahs that best matches the user's vibe, with an emoji added at the end.

    Raises:
        AttributeError: If the response object does not contain the expected structure or parts.
    """
    
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(    
                                      
    f"Analyze the provided Quranic ayahs: {text}. Reflect briefly on their meaning and significance without altering the original text. Keep the analysis concise, limited to 1 to 1.5 paragraphs. Conclude with an appropriate emoji."
    
    )

    return str(response.candidates[0].content.parts[0].text)