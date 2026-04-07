from fastapi import APIRouter, HTTPException, Depends
from models.schemas import GenerateQuizRequest, APIResponse
from services.ai_service import generate_quiz_from_prompt
from core.db import get_session
from sqlmodel import Session
from crud.quiz_crud import save_ai_quiz_to_db, get_all_quizzes_formatted

router = APIRouter(
    prefix="/quizzes",
    tags=["Quizzes"],
)

@router.get("/", response_model=APIResponse)
async def get_quizzes(session: Session = Depends(get_session)):
    """
    Lấy toàn bộ Quiz từ Database trả về Frontend
    """
    try:
        quizzes_data = get_all_quizzes_formatted(session)
        return APIResponse(status="success", data={"quizzes": quizzes_data})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi lấy dữ liệu Database: {str(e)}")

@router.post("/generate", response_model=APIResponse)
async def generate_quiz(request: GenerateQuizRequest, session: Session = Depends(get_session)):
    """
    API endpoint that receives a prompt from the frontend and returns an AI-generated Quiz.
    The generated quiz is automatically saved to the database!
    """
    if not request.topic or len(request.topic.strip()) < 3:
         raise HTTPException(status_code=400, detail="Topic is too short or empty.")
         
    # 1. Gọi AI sinh ra JSON
    ai_response = await generate_quiz_from_prompt(request.topic, request.count)
    
    if ai_response.get("status") == "error":
        raise HTTPException(status_code=400, detail=ai_response.get("message", "AI refused to process this topic."))
        
    try:
        data = ai_response.get("data")
        
        # 2. Xé nhỏ JSON và thả xuống DB
        db_quiz = save_ai_quiz_to_db(session, data)
        
        # 3. Ép kiểu chuẩn hóa để trả về Frontend ngay lập tức
        # (Lấy luôn cái ID thật do DB vừa tạo ra gắn vào JSON)
        data["id"] = str(db_quiz.id)
        data["createdAt"] = db_quiz.created_time.strftime("%Y-%m-%d")
        data["questionCount"] = len(data.get("questions", []))
        
        return APIResponse(status="success", data=data)
    except Exception as e:
         raise HTTPException(status_code=500, detail=f"Lỗi cú pháp JSON hoặc lỗi lưu Database: {str(e)}")
