from sqlmodel import Session
from core.db import engine
from models.database import Quizzes, Questions, Options, QuizDifficulties

print(">> Bắt đầu bài Test: Lưu thử một cục dữ liệu đẻ lồng nhau xuống Supabase...")
try:
    with Session(engine) as session:
        # 1. Tạo 1 Bài Quiz gốc
        test_quiz = Quizzes(
            title="[Bài Test Chống Đạn] Lịch sử Việt Nam", 
            difficulty=QuizDifficulties.EASY
        )
        
        # 2. Tạo Câu Hỏi lồng vào Quiz
        test_question = Questions(
            content="Vua Hùng vương thứ mấy đã nhường ngôi cho Thục Phán?", 
            explanation="Kiểm tra kiến thức lịch sử",
            quiz=test_quiz
        )
        
        # 3. Tạo 2 Hộp Đáp án lồng vào Câu hỏi
        opt1 = Options(content="Đời thứ 18", is_correct=True, question=test_question)
        opt2 = Options(content="Đời thứ 1", is_correct=False, question=test_question)
        
        # 4. Ném hết vào Giỏ
        session.add(opt1)
        session.add(opt2)
        session.add(test_question)
        session.add(test_quiz)
        
        # 5. KÍCH NỔ LƯU (Đẩy cái rẹt xuống Supabase)
        session.commit()
        
        # Tải lại để lấy ID do Supabase cấp phát
        session.refresh(test_quiz)
        
        print("\n" + "="*50)
        print(f"✅ THÀNH CÔNG VANG DỘI! Database của bạn hoạt động cực mạnh mẽ!")
        print(f"✅ ID Bài Quiz được sinh ra từ máy chủ Mỹ: {test_quiz.id}")
        print("="*50 + "\n")
        
except Exception as e:
    print("\n" + "="*50)
    print("❌ LỖI VỠ MẶT! Code có vấn đề rồi:")
    print(e)
    print("="*50 + "\n")
