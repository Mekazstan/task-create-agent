from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ValidationError
import uvicorn
from agent_cohere import prompt_ai

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    role: str
    content: str

class RequestBody(BaseModel):
    messages: list[Message]
    
def process_messages(messages):
    processed_messages = []
    for message in messages:
        processed_message = {
            "role": message.role,
            "content": message.content
        }
        processed_messages.append(processed_message)
    return processed_messages

@app.post("/chat")
async def chat(body: RequestBody):
    """
    Endpoint to interact with the AI agent.
    Accepts a list of messages in the format required by the AI model.
    """
    try:
        messages = body.messages
        processed_messages = process_messages(messages)
        response = prompt_ai(processed_messages)
        return JSONResponse({"message": response})
    except ValidationError as ve:
        raise HTTPException(status_code=422, detail=ve.errors())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
