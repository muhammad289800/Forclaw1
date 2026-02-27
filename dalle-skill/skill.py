import openai

def generate_image(prompt):
    openai.api_key = ""  # Removed sensitive information

    print(f"Current prompt: {{prompt}}")  # Debug statement
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="1024x1024"  # Adjust as needed
    )

    return response['data'][0]['url']

# Example usage
if __name__ == "__main__":
    prompt = "Enter your custom prompt here"
    print(f"Prompt being used: {{prompt}}")  # Debug statement
    image_url = generate_image(prompt)
    print(image_url)  # Print the generated image URL