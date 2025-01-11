import requests
from io import BytesIO
import time

Info = {
    "Description": "Provide Lyrics For The Song Given"
}

def fetch_lyrics(song):
    """
    Fetches song details (lyrics, title, artist, and image) from the API.
    
    :param song: The song name to search for.
    :return: A dictionary containing song details or an error message.
    """
    if not song:
        return {"success": False, "error": "❌ Please provide a song name."}
    
    url = f"https://kaiz-apis.gleeze.com/api/lyrics?song={song}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        if "lyrics" in data:
            return {"success": True, "data": data}
        else:
            return {"success": False, "error": "🚨 No lyrics found for the provided song."}
    
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": f"🚨 Error fetching lyrics: {str(e)}"}

def get_image_bytes(image_url):
    """
    Fetches the image as bytes.
    
    :param image_url: URL of the image to fetch.
    :return: The image as BytesIO object or an error message.
    """
    try:
        response = requests.get(image_url)
        response.raise_for_status()
        return BytesIO(response.content)  # Return image as BytesIO
    except requests.exceptions.RequestException as e:
        return f"🚨 Failed to fetch image: {str(e)}"

def split_lyrics(lyrics):
    """
    Splits the lyrics into three parts.
    
    :param lyrics: The complete lyrics string.
    :return: A list containing three parts of the lyrics.
    """
    lines = lyrics.split('\n')
    part_size = len(lines) // 3
    return ['\n'.join(lines[i:i + part_size]) for i in range(0, len(lines), part_size)]

def display_song(data):
    """
    Returns the song's details in a formatted string.
    
    :param data: A dictionary containing song details.
    :return: A list of formatted strings with the song's details.
    """
    lyrics_parts = split_lyrics(data['lyrics'])
    song_details = [
        f"\n{'➖' * 5}\n"
        f"🎵 Title: {data['title']}\n"
        f"🎤 Artist: KORA AI\n"
        f"{'➖' * 5}\n\n"
        f"📋 Lyrics (Part {i+1}):\n\n{part}\n"
        f"{'➖' * 5}" for i, part in enumerate(lyrics_parts)
    ]
    return song_details

def execute(message):
    """
    Main function to fetch and display song details, including the album cover image.
    
    :param song_name: The name of the song to search for.
    :return: A tuple containing the image as BytesIO and a list of formatted strings with song details.
    """
    result = fetch_lyrics(message)
    if result["success"]:
        data = result["data"]
        image_bytes = get_image_bytes(data["image"])
        song_details = display_song(data)
        return image_bytes, song_details
    else:
        return None, result["error"]

