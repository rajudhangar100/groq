from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from groq import Groq
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with your frontend's URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Update this api_key with your api_key, and to get the
# api key go to the console.groq.com 
client = Groq(
    api_key="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",
)

# Define input model
class ChatRequest(BaseModel):
    message: str

@app.post("/chat/")
async def chat_completion(request: ChatRequest):
    try:
        # Process the input message using Groq API
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": request.message}],
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=True,
            stop=None,
        )

        # Collect the streamed response
        response = ""
        for chunk in completion:
            response += chunk.choices[0].delta.content or ""

        return {"response": response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

