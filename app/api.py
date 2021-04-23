from datetime import datetime
from models import Person
from app import compare_persons

async def api_setup(server):

    @server.post('/api/v1/compare', groups=['administrators'], tags=['Validation'])
    async def compare_persons_api(person1: Person, person2: Person):
        probability = compare_persons(person1, person2)
        await server.db.tables['scores'].insert(**{
            'date_detected': datetime.now().isoformat(),
            'full_name_p1': person1.first_name + ' ' + person1.last_name,
            'full_name_p2': person2.first_name + ' ' + person2.last_name,
            'score': probability
        })
        return {"probability": probability}
