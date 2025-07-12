from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.schemas.chat import ChatRequest, ChatResponse
from app.schemas.user import User
from app.services.auth_service import get_current_user
from app.services.chat_service import chat_service

router = APIRouter(prefix="/chat", tags=["chat"])

@router.get("/models")
async def get_available_models():
    """Get available models and default model."""
    return {
        "available_models": chat_service.get_available_models(),
        "default_model": chat_service.get_default_model()
    }

@router.post("/message", response_model=ChatResponse)
async def send_message(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Send a chat message and get a response."""
    try:
        user_id = 1  # For demo purposes, using a fixed user_id
        response = await chat_service.process_chat_message(request, user_id, db)
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing message: {str(e)}"
        )

@router.get("/conversations")
async def get_conversations(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get all conversations for the current user."""
    try:
        user_id = 1  # For demo purposes
        conversations = chat_service.get_user_conversations(user_id, db)
        return {"conversations": conversations}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving conversations: {str(e)}"
        )

@router.get("/conversations/{conversation_id}/history")
async def get_conversation_history(
    conversation_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get the history of a specific conversation."""
    try:
        messages = chat_service.get_conversation_history(conversation_id, db)
        return {"messages": messages, "conversation_id": conversation_id}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving conversation history: {str(e)}"
        )

@router.delete("/conversations/{conversation_id}")
async def delete_conversation(
    conversation_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a conversation."""
    try:
        user_id = 1  # For demo purposes
        success = chat_service.delete_conversation(conversation_id, user_id, db)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found or access denied"
            )
        return {"message": "Conversation deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting conversation: {str(e)}"
        )

@router.put("/conversations/{conversation_id}/rename")
async def rename_conversation(
    conversation_id: str,
    new_title: str = Body(..., embed=True),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Rename a conversation."""
    try:
        user_id = 1  # For demo purposes
        success = chat_service.rename_conversation(conversation_id, user_id, new_title, db)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found or access denied"
            )
        return {"message": "Conversation renamed successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error renaming conversation: {str(e)}"
        ) 