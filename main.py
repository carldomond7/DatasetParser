from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import json

app = FastAPI()

class ParseRequest(BaseModel):
    text: str
    solution: str
    start_marker: str
    end_marker: str
    instruction: str

def parse_content(text: str, solution: str, start_marker: str, end_marker: str, instruction: str) -> list:
    entries = []
    current_entry = None
    is_input = False

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
            is_input = True
        elif line.startswith(end_marker):
            is_input = False
        elif current_entry and is_input:
            current_entry["input"] += line + "\n"

    if current_entry:
        entries.append(current_entry)
    
    # Clean up trailing newlines and assign solution to output
    for entry in entries:
        entry["input"] = entry["input"].strip()
        entry["output"] = solution.strip()  # Directly use solution for the output
    
    return entries

class ParseRequestList(BaseModel):
    requests: List[ParseRequest]

@app.post("/parse/")
async def parse_text(requests: ParseRequestList):
    try:
        all_entries = []
        for request in requests.requests:
            entries = parse_content(
                request.text, 
                request.solution, 
                request.start_marker, 
                request.end_marker,
                request.instruction
            )
            all_entries.extend(entries)
        # Format the entries as a JSON string
        formatted_json = json.dumps(all_entries, indent=2)
        return formatted_json
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
