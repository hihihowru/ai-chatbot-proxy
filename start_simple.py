#!/usr/bin/env python3
import os
import uvicorn

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("langgraph_app.main:app", host="0.0.0.0", port=port) 