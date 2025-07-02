#!/usr/bin/env python3
import os
import uvicorn
import logging

# 設置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    # 安全地讀取 PORT 環境變量
    port_str = os.getenv("PORT", "8000")
    try:
        port = int(port_str)
        logger.info(f"Starting server on port {port}")
    except ValueError:
        logger.error(f"Invalid PORT value: {port_str}, using default port 8000")
        port = 8000
    
    uvicorn.run("langgraph_app.main:app", host="0.0.0.0", port=port) 