from fastapi import FastAPI, Request, File, UploadFile
from azure.cosmos import exceptions
import uvicorn
import uuid
from typing import List
from utils.services import hash_password, verify_password
from models import authenticate, register, chatbot
from db import db
from storage import storage


app = FastAPI(
    title = "Document Assistant",
    description = "This is a document assistant APIs for document chatbot",
)
sessions = {}
# blobfile = storage.BlobFile()

@app.post("/authenticate")
def authenticate_api(request: Request, user: authenticate.AuthenticateModel):
    """
    API to authenticate a user
    """
    authenticate_query = f'SELECT * FROM users WHERE user.email = "{user.email}"'
    existing_user = db.get_user_by_email(user.email)
    if existing_user and verify_password(user.password, existing_user[0]["password"]):
        sessions[request.client.host] = user.email
        return {"message": "user logged in successfully"}
    else:
        return {"message": "Invalid credentials"}


@app.post("/register")
def register_api(request: Request, user: register.RegisterModel):
    """
    API to register a new user
    """
    register_query = f'SELECT * FROM users WHERE user.email = "{user.email}"'

    existing_user = db.get_user_by_email(user.email)

    if existing_user:
        return {"message": "User already exists"}
    try:
        # Create a unique id for the user
        user_id = str(uuid.uuid4())
        # Hash the password
        hashed_pw = hash_password(user.password)

        # Define the user document to insert into Cosmos DB
        user_document = {
            "id": user_id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "password": hashed_pw
        }

        # Insert the new user document into Cosmos DB
        db.create_user_document(user_document)
    except exceptions.CosmosHttpResponseError as e:
        return {"message": "User already exists"}
    return {"message": "Register API"}, 200

@app.post("/upload-document")
def upload_pdf(request: Request, files: List[UploadFile] = File(...)):
    """
    API to Upload PDF documents
    """
    client_ip = request.client.host
    responses = []  # To store responses for each file upload

    for file in files:
        # Check if the uploaded file is a PDF
        if file.content_type != "application/pdf":
            responses.append({"filename": file.filename, "message": "Only PDF files are allowed"})
            continue
        try:
            # Upload the file to Azure Blob Storage
            storage.upload_to_blob(file.file, file.filename)  # Ensure upload_to_blob is asynchronous
            print(f"File uploaded: {file.filename}")
            responses.append({"filename": file.filename, "message": "PDF uploaded successfully"})
        except Exception as e:
            responses.append({"filename": file.filename, "message": f"File upload failed: {str(e)}"})
        finally:
            file.close()
        # try:
        #     # Upload the file to Azure Blob Storage
        #     upload_to_blob(file.file, file.filename)
        #     responses.append({"filename": file.filename, "message": "PDF uploaded successfully"})
        # except Exception as e:
        #     responses.append({"filename": file.filename, "message": f"File upload failed: {str(e)}"})
        # # try:
        # #     blobfile.ingest_data(file.filename)
        # #     responses.append({"filename": file.filename, "message": "File ingested successfully"})
        # # except Exception as e:
        # #     responses.append({"filename": file.filename, "message": f"File ingestion failed: {str(e)}"})
        # finally:
        #     file.file.close()  # Ensure the file is closed after processing

    return {"responses": responses}

@app.post("chatbot")
def chatbot(request: Request, query: chatbot.ChatbotModel):
    """
    API for chatbot
    """
    query = query.query
    if not query:
        return {"response": "Query is required"}
    if len(query) < 6:
        return {"response": "Query must be at least 6 characters"}
    response = "This is a response from the chatbot"
    return {"response": response}


