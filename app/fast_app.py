
from fastapi import FastAPI
from pydantic import BaseModel
import torch
from bot import NeomBot
from utililty import llm_load
from transformers import pipeline

app = FastAPI()

MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.1"
llm = llm_load(MODEL_NAME)

llm_ent = pipeline(
    "text-generation",
    model="Universal-NER/UniNER-7B-type",
    torch_dtype=torch.float16,
    device=0,
)

sessions = []

class MyData(BaseModel):
    sender: int
    text: str

@app.post("/neom_assistant/")
def neom_assistant(data: MyData):
    sender = data.sender
    text = data.text
    bot = NeomBot(llm, text, sender, llm_ent)
    response = bot.run()
    return response
