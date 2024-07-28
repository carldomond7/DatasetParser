from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import json

app = FastAPI()

class ParseRequest(BaseModel):
    text: str
    start_marker: str
    end_marker: str
    instruction: str

class ParsedEntry(BaseModel):
    instruction: str
    input: str
    output: str

def parse_content(text: str, start_marker: str, end_marker: str, instruction: str) -> List[dict]:
    entries = []
    current_entry = None
    in_output = False
    
    for line in text.split('\n'):
        line = line.strip()
        if line.startswith(start_marker):
            if current_entry:
                entries.append(current_entry)
            current_entry = {
                "instruction": instruction,
                "input": "",
                "output": ""
            }
            in_output = False
        elif line == end_marker:
            in_output = True
        elif current_entry:
            if in_output:
                current_entry["output"] += line + "\n"
            else:
                current_entry["input"] += line + "\n"
    
    if current_entry:
        entries.append(current_entry)
    
    # Clean up trailing newlines
    for entry in entries:
        entry["input"] = entry["input"].strip()
        entry["output"] = entry["output"].strip()
    
    return entries

@app.post("/parse/")
async def parse_text(request: ParseRequest):
    try:
        entries = parse_content(
            request.text, 
            request.start_marker, 
            request.end_marker,
            request.instruction
        )
        # Format the entries as a JSON string
        formatted_json = json.dumps(entries, indent=2)
        return {"formatted_json": formatted_json}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
