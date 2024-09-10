from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from groq import Groq
import uvicorn
import os

os.environ['GROQ_API_KEY'] = ''

app = FastAPI()

class PropertyDetails(BaseModel):
    type: str
    location: str
    bedrooms: int
    bathrooms: int
    square_footage: float
    features: str

async def generate_property_description(property_details):
    groq = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    prompt = f"""
    Générer une description détaillée, attrayante et optimisée pour le SEO d'un bien immobilier en Tunisie en fonction des détails suivants sans aucune note ou introduction:

    Type de propriété: {property_details.type}
    Emplacement: {property_details.location}
    Nombre de chambres: {property_details.bedrooms}
    Nombre de salles de bain: {property_details.bathrooms}
    Superficie: {property_details.square_footage}
    Caractéristiques spéciales: {property_details.features}
    """

    chat_completion = groq.chat.completions.create(
        #model='llama3-70b-8192',
        model='llama-3.1-70b-versatile',
        messages=[
            {
                "role": "system",
                "content": "You are an expert real estate agent and copywriter fluent in French, with a knack for crafting compelling and SEO-optimized descriptions for real estate listings in Tunisia."
            },
            {'role': 'user', 'content': prompt}
        ],
        temperature=0.2,
    )
   
    return chat_completion.choices[0].message.content

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post('/generate-description')
async def generate_description(property_details: PropertyDetails):
    try:
        description = await generate_property_description(property_details)
        return {'description': description}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5010)

