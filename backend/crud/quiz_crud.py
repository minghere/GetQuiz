from sqlmodel import Session, select
from models.database import Quizzes, Questions, Options, QuizDifficulties

def save_ai_quiz_to_db(session: Session, ai_data: dict, user_id: str = None) -> Quizzes:
    """
    Nhận JSON từ AI, xé lẻ ra 3 bảng và lưu vĩnh viễn xuống Supabase.
    """
    # 1. Tạo Bài Quiz gốc
    db_quiz = Quizzes(
        title=ai_data.get("title", "AI Generated Quiz"),
        difficulty=QuizDifficulties.EASY,
        user_id=user_id
    )
    
    # 2. Xé nhỏ Questions
    for q_data in ai_data.get("questions", []):
        db_question = Questions(
            content=q_data.get("text", "Không rõ nội dung"),
            explanation="",
            quiz=db_quiz # Ép dính vào quiz
        )
        
        # 3. Xé nhỏ Options
        correct_index = q_data.get("correctIndex", 0)
        options_list = q_data.get("options", [])
        
        # Nếu là câu hỏi True/False, AI có thể trả mảng option không chuẩn, ta ép lại
        if q_data.get("type") == "tf" and not options_list:
            options_list = ["True", "False"]
            correct_index = 0 if q_data.get("correct", True) else 1
            
        for idx, opt_text in enumerate(options_list):
            is_correct = (idx == correct_index)
            db_option = Options(
                content=opt_text,
                is_correct=is_correct,
                question=db_question # Ép dính vào question
            )
            session.add(db_option)
            
        session.add(db_question)

    session.add(db_quiz)
    
    # Bấm nút kích nổ: Xả thẳng xuống Database
    session.commit()
    session.refresh(db_quiz)
    
    return db_quiz

def get_all_quizzes_formatted(session: Session) -> list:
    """
    Vét toàn bộ Quiz dưới CSDL lên, và nặn lại y hệt cấu trúc JSON (MOCK_QUIZZES) 
    mà Frontend đang ngóng chờ.
    """
    # Lấy toàn bộ Quizzes
    quizzes = session.exec(select(Quizzes)).all()
    
    result = []
    for qz in quizzes:
        # Xử lý questions của bài quiz đó
        q_list = []
        for qtn in qz.question: # qz.question là mảng nhờ Relationship
            # Phân loại MCQ hay TF: Dựa vào số lượng đáp án
            q_type = "mcq" if len(qtn.option) > 2 else "tf"
            
            # Xếp lại thứ tự ID đáp án vì Database lấy lên có thể lộn xộn
            # Ta mặc định option nào is_correct = True thì lấy index của nó
            options_text = []
            correct_idx = 0
            correct_boolean = True
            
            # Để đảm bảo option ko dính lỗi, ta loop
            for idx, opt in enumerate(qtn.option):
                options_text.append(opt.content)
                if opt.is_correct:
                    correct_idx = idx
                    if opt.content.lower() == "false":
                        correct_boolean = False
            
            # Nặn 1 câu hỏi hoàn chỉnh để trả về
            fmt_qtn = {
                "id": str(qtn.id),
                "type": q_type,
                "text": qtn.content,
                "options": options_text,
                "correctIndex": correct_idx,
                "correct": correct_boolean
            }
            q_list.append(fmt_qtn)
            
        # Nặn bài Quiz lớn
        fmt_quiz = {
            "id": str(qz.id),
            "title": qz.title,
            "description": "Bài Quiz sinh ra từ Trí tuệ Nhân tạo hệ GetQuiz.",
            "createdAt": qz.created_time.strftime("%Y-%m-%d"),
            "tags": ["AI", "GetQuiz"],
            "questions": q_list
        }
        result.append(fmt_quiz)
        
    # Đảo ngược mảng để bài Quiz mới nhất lên đầu tiên
    return result[::-1]
