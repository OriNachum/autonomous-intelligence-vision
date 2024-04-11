import uvicorn
import asyncio

if __name__ == "__main__":
    #uvicorn.run(app, host="0.0.0.0", port=8000)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(uvicorn.run("tau_ext:app", host="0.0.0.0", port=8000, reload=True))

