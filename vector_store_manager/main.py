import dotenv
dotenv.load_dotenv()
from fastapi import FastAPI

app = FastAPI()

from vector_store_manager.routes.files import router as router_files

app.include_router(router=router_files)
