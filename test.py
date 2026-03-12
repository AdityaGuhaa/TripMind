from google import genai

client = genai.Client(api_key="Gemini Api Key")

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Plan a 2 day trip to Goa"
)

print(response.text)