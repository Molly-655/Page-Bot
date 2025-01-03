import requests
from io import BytesIO

def execute(message=None):
    """
    Generate images using the ClashAI DALL-E-3 API.

    Args:
        message (str): The prompt for image generation.

    Returns:
        dict: A dictionary containing success status and either the images or an error message.
    """
    if not message:
        return {
            "success": False,
            "data": {"type": "text", "content": "🚨 No prompt provided. Please provide a valid prompt for image generation."}
        }

    # Inform the user that the image is being generated
    awaiting_message = {
        "success": True,
        "data": {"type": "text", "content": "⏳ Generating your image, please wait..."}
    }

    url = "https://api.clashai.eu/v1/images/generations"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer YOUR_API_KEY"
    }
    data = {
        "model": "dall-e-3",
        "prompt": message,
        "n": 1,  # Generate 1 image for now
        "size": "256x256"
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            result = response.json()
            image_data = []
            for img_data in result.get('data', []):
                img_url = img_data.get('url')
                if img_url:
                    img_response = requests.get(img_url)
                    if img_response.status_code == 200:
                        img = BytesIO(img_response.content)
                        image_data.append(img)
                    else:
                        return {
                            "success": False,
                            "data": {"type": "text", "content": f"🚨 Failed to fetch image from URL: {img_url}"}
                        }
            
            # Once the image is generated, we can send the attachment ID (after upload) back to the user
            # We assume the `upload_image_to_graph` function will return an attachment ID that can be sent back
            if image_data:
                upload_response = upload_image_to_graph(image_data[0])  # Upload the first image
                if upload_response.get("success"):
                    return {
                        "success": True,
                        "data": {"type": "image", "content": upload_response["attachment_id"]}
                    }
                else:
                    return {
                        "success": False,
                        "data": {"type": "text", "content": "🚨 Failed to upload the image."}
                    }
            else:
                return {
                    "success": False,
                    "data": {"type": "text", "content": "🚨 No image generated."}
                }

        else:
            return {
                "success": False,
                "data": {"type": "text", "content": f"🚨 Error from API. Status code: {response.status_code}, Response: {response.text}"}
            }
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "data": {"type": "text", "content": f"🚨 Request failed: {str(e)}"}
        }
