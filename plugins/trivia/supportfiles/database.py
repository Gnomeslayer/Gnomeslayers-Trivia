import aiosqlite

class trivia_database():
    def __init__(self):
        self.database_location = "./plugins/trivia/supportfiles/database.db"

    async def create_table(self) -> None:
        async with aiosqlite.connect(self.database_location) as db:
            await db.execute('''
                CREATE TABLE IF NOT EXISTS trivia (
                    id INTEGER PRIMARY KEY,
                    question TEXT,
                    question_type TEXT,
                    real_answer TEXT,
                    fake_answer_one TEXT,
                    fake_answer_two TEXT,
                    fake_answer_three TEXT,
                    fake_answer_four TEXT,
                    submitted_by TEXT,
                    file_url TEXT
                )
            ''')

            await db.commit()

    
    async def get_all_questions(self) -> list[dict]:
        query = "SELECT * FROM trivia"
        questions = []
        async with aiosqlite.connect(self.database_location) as db:
            response = await db.execute(query)
            response = await response.fetchall()
            for question in response:
                questions.append({
                    'question': question[1],
                    'question_type': question[2],
                    'real_answer': question[3],
                    'fake_answer_one': question[4],
                    'fake_answer_two': question[5],
                    'fake_answer_three': question[6],
                    'fake_answer_four': question[7],
                    'submitted_by': question[8],
                    'file_url': question[9]
                    })
        
        return questions

    
    async def get_specific_question(self, question_number):
        query = "SELECT * FROM trivia WHERE id = :question_number"
        params = {'question_number': question_number}

        results = {}

        async with aiosqlite.connect(self.database_location) as db:
            async with db.execute(query, params) as cursor:
                result = await cursor.fetchall()
            
            for r in result:
                results = {
                    'question': r[1],
                    'question_type': r[2],
                    'real_answer': r[3],
                    'fake_answer_one': r[4],
                    'fake_answer_two': r[5],
                    'fake_answer_three': r[6],
                    'fake_answer_four': r[7],
                    'submitted_by': r[8],
                    'file_url': r[9]
                    }

        return results
         
    async def add_question(self, question, question_type, real_answer, fake_answer_one,fake_answer_two,fake_answer_three,
                           fake_answer_four, submitted_by, file_url) -> None:

        query = """INSERT INTO trivia 
        (question, question_type, real_answer, fake_answer_one,fake_answer_two,fake_answer_three,fake_answer_four, submitted_by, file_url) 
        VALUES 
        (:question, :question_type, :real_answer, :fake_answer_one,:fake_answer_two,:fake_answer_three, :fake_answer_four, :submitted_by, :file_url)"""

        params = {
                    'question': question,
                    'question_type': question_type,
                    'real_answer': real_answer,
                    'fake_answer_one': fake_answer_one,
                    'fake_answer_two': fake_answer_two,
                    'fake_answer_three': fake_answer_three,
                    'fake_answer_four': fake_answer_four,
                    'submitted_by': submitted_by,
                    'file_url': file_url
                    }

        async with aiosqlite.connect(self.database_location) as db:
            await db.execute(query, params)
            await db.commit()
        
        return True