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
                    submitted_by TEXT,
                    file_url TEXT,
                    category TEXT
                )
            ''')

            await db.execute('''
                CREATE TABLE IF NOT EXISTS players (
                    id INTEGER PRIMARY KEY,
                    discord_id TEXT,
                    points INTEGER,
                    questions_submitted INTEGER,
                    times_double_points INTEGER
                )
            ''')

            await db.execute('''
                CREATE TABLE IF NOT EXISTS categories (
                    id INTEGER PRIMARY KEY,
                    category TEXT
                )
            ''')

            await db.commit()



    async def get_all_players(self) -> list[dict]:
        query = "SELECT * FROM players"
        players = []

        async with aiosqlite.connect(self.database_location) as db:
            response = await db.execute(query)
            response = await response.fetchall()

            for player in response:
                players.append({
                    'id': player[0],
                    'discord_id': player[1],
                    'points': player[2],
                    'questions_submitted': player[3],
                    'times_double_points': player[4]
                })
        return players
    

    async def get_all_questions(self, category:str = None) -> list[dict]:
        params = {}
        if category:
            query = "SELECT * FROM trivia WHERE category = :category"
            params = {"category": category}
        else:
            query = "SELECT * FROM trivia"
        questions = []
        async with aiosqlite.connect(self.database_location) as db:
            response = await db.execute(query, params)
            response = await response.fetchall()
            for question in response:
                questions.append({
                    'id': question[0],
                    'question': question[1],
                    'question_type': question[2],
                    'real_answer': question[3],
                    'fake_answer_one': question[4],
                    'fake_answer_two': question[5],
                    'fake_answer_three': question[6],
                    'submitted_by': question[7],
                    'file_url': question[8],
                    'shown': False,
                    'category': question[9]
                    })
        
        return questions
    
    async def get_all_categories(self):
        query = "SELECT * FROM categories"

        categories = []
        async with aiosqlite.connect(self.database_location) as db:
            response = await db.execute(query)
            response = await response.fetchall()
            for category in response:
                categories.append(category[1])

        return categories
    

    async def get_specific_player(self, discord_id):
        query = "SELECT * FROM players WHERE discord_id = :discord_id"
        params = {'discord_id': discord_id}

        results = {}

        async with aiosqlite.connect(self.database_location) as db:
            async with db.execute(query, params) as cursor:
                result = await cursor.fetchall()
            
            for player in result:
                results = {
                    'id': player[0],
                    'discord_id': player[1],
                    'points': player[2],
                    'questions_submitted': player[3],
                    'times_double_points': player[4]
                }
        
        return results
    async def get_specific_question(self, question_number):
        query = "SELECT * FROM trivia WHERE id = :question_number"
        params = {'question_number': question_number}

        results = {}

        async with aiosqlite.connect(self.database_location) as db:
            async with db.execute(query, params) as cursor:
                result = await cursor.fetchall()
            
            for r in result:
                results = {
                    'id': r[0],
                    'question': r[1],
                    'question_type': r[2],
                    'real_answer': r[3],
                    'fake_answer_one': r[4],
                    'fake_answer_two': r[5],
                    'fake_answer_three': r[6],
                    'submitted_by': r[7],
                    'file_url': r[8],
                    'category': r[9]
                    }

        return results
    
    async def add_category(self, category:str):
        query = "INSERT INTO categories (category) VALUES (:category)"
        params = {"category": category}

        async with aiosqlite.connect(self.database_location) as db:
            await db.execute(query, params)
            await db.commit()

        return True
    
    async def add_question(self, question, question_type, real_answer, fake_answer_one,fake_answer_two,fake_answer_three,
                           submitted_by, file_url, category) -> None:

        query = """INSERT INTO trivia 
        (question, question_type, real_answer, fake_answer_one,fake_answer_two,fake_answer_three, submitted_by, file_url, category) 
        VALUES 
        (:question, :question_type, :real_answer, :fake_answer_one,:fake_answer_two,:fake_answer_three, :submitted_by, :file_url, :category)"""

        params = {
                    'question': question,
                    'question_type': question_type,
                    'real_answer': real_answer,
                    'fake_answer_one': fake_answer_one,
                    'fake_answer_two': fake_answer_two,
                    'fake_answer_three': fake_answer_three,
                    'submitted_by': submitted_by,
                    'file_url': file_url,
                    'category': category
                    }

        async with aiosqlite.connect(self.database_location) as db:
            await db.execute(query, params)
            await db.commit()
        
        await self.update_player(discord_id=submitted_by, add_question=True)
        return True
    

    async def update_player(self, discord_id, add_point=False, add_question=False, add_double=False):
        
        
        updates = []
        player = await self.get_specific_player(discord_id=discord_id)
        params = {'discord_id': discord_id}
        if not player:
            await self.add_player(discord_id=discord_id)
            
        #Build our query
        if add_point:
            if add_double:
                updates.append("points = points + 2")
            else:
                updates.append("points = points + 1")
        if add_question:
            updates.append("questions_submitted = questions_submitted + 1")
        if add_double:
            updates.append("times_double_points = times_double_points + 1")

        if updates:  # Ensure there's at least one update
            query = f"UPDATE players SET {', '.join(updates)} WHERE discord_id = :discord_id"
        else:
            query = None  # No update needed

        if not query:
            return
        
        async with aiosqlite.connect(self.database_location) as db:
                await db.execute(query, params)
                await db.commit()

    async def add_player(self, discord_id):
        query = """INSERT INTO players 
            (discord_id, points, questions_submitted, times_double_points)
            VALUES
            (:discord_id, 0, 0, 0)"""

        params = {'discord_id': discord_id}

        async with aiosqlite.connect(self.database_location) as db:
            await db.execute(query, params)
            await db.commit()