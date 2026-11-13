import requests

# Configuration
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5-coder:7b"
# MODEL_NAME = "qwen3:4b"

# Step 1: Read transcript file
def read_transcript(file_path):

    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

def analyze_transcript(transcript):

    prompt = f"""
        You are a technical video content analyst.

        Find the most valuable educational segments (programming concepts,
        coding examples, technical explanations, interview Q&A, architecture)
        in the timestamped transcript below.

        RULES:
            - Use only timestamps that appear in the transcript. Never invent them.
            - "start" = start of the first selected entry; "end" = end of the last.
            - Each segment must be 30-90 seconds and cover one complete topic.
            - Select consecutive transcript entries only.
            - No overlapping segments.
            - Identify ALL valuable educational segments; do not impose a maximum number.
            - Prioritize programming concepts, coding examples, technical explanations, interview Q&A, and architecture.
            - Skip greetings, breaks, small talk, and non-educational content.
            - Avoid splitting one complete explanation into multiple segments.
            - Base everything strictly on the transcript; add no outside content.
            - If no suitable segments exist, return an empty list.

        TRANSCRIPT START:
        {transcript}
        TRANSCRIPT END:

        Return ONLY valid JSON in this shape, no other text:
        {{
        "segments": [
            {{"title": "Python decorators explained", "start": "00:03:12,000", "end": "00:04:05,500", "reason": "Complete explanation with live example"}}
        ]
        }}
        If nothing suitable: {{"segments": []}}
    """

    payload = {
    "model": MODEL_NAME,
    "prompt": prompt,
    "stream": False,
    "format": "json",
    "think": False,
    "options": {
        "temperature": 0,
        "num_predict": 2000,
        "num_ctx": 16384
    }
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=600
    )

    response.raise_for_status()

    result = response.json()

    # print("LLM Response:")s
    # print(result["response"])

    return result["response"]

# Step 3: Main execution
if __name__ == "__main__":

    transcript = read_transcript("/Users/praveen/Downloads/captions/captions1.sbv")
    chunk_transcript =  [transcript[i:i + 5000] for i in range(0, len(transcript), 5000)]
    print(f"total {len(chunk_transcript)}")
    for part_transcript in chunk_transcript:
        print("Transcript characters:", len(part_transcript))
        result = analyze_transcript(part_transcript)
        print("\nLLM Response:")
        print(result)