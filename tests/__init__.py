from unittest import TestCase
from models import Person
from app import compare_persons
from datetime import datetime
from pydantic import ValidationError

class TestPerson(TestCase):
    def test_person_creation(self):
        p = Person(
            first_name = 'Joe',
            last_name = 'Doe',
            date_of_birth = '30-01-2020',
            id_number=123456
        )

    def test_invalid_person_creation(self):
        try:
            p = Person(
                first_name = 'Joe',
                last_name = 'Doe',
                date_of_birth = '33-01-2020',
                id_number=123456
            )
        except ValidationError:
            return
        assert False, f"Model Error - Expected ValidationError for invalid DOB '33-01-2020"
        
class TestComparison(TestCase):
    def test_person_comparison(self):
        pairs = [
            {
                'person1': {
                    'first_name': 'Andrew',
                    'last_name': 'Craw',
                    'date_of_birth': '20-02-1985',
                    'id_number':  931212312
            },
                'person2': {
                    'first_name': 'Petty',
                    'last_name': 'Smith',
                    'date_of_birth': '20-02-1985',
                    'id_number':  931212312
                },
                'expected': 100
            },
            {
                'person1': {
                    'first_name': 'Andrew',
                    'last_name': 'Craw',
                    'date_of_birth': '20-02-1985',
                    'id_number':  'unknown'
            },
                'person2': {
                    'first_name': 'A.',
                    'last_name': 'Craw',
                    'date_of_birth': '20-02-1985',
                    'id_number':  'unknown'
                },
                'expected': 95
            },
            {
                'person1': {
                    'first_name': 'Andrew',
                    'last_name': 'Craw',
                    'date_of_birth': '20-02-1985',
                    'id_number':  'unknown'
            },
                'person2': {
                    'first_name': 'Petty',
                    'last_name': 'Smith',
                    'date_of_birth': '20-02-1985',
                    'id_number':  'unknown'
                },
                'expected': 40
            },
            {
                'person1': {
                    'first_name': 'Andrew',
                    'last_name': 'Craw',
                    'date_of_birth': '20-02-1985',
                    'id_number':  'unknown'
            },
                'person2': {
                    'first_name': 'Andrew',
                    'last_name': 'Craw',
                    'id_number':  'unknown'
                },
                'expected': 60
            },
            {   # Typo check
                'person1': {
                    'first_name': 'Andrew',
                    'last_name': 'Craw',
                    'date_of_birth': '20-02-1985',
                    'id_number':  1234
            },  
                'person2': {
                    'first_name': 'Andew', 
                    'last_name': 'Craw',
                    'date_of_birth': '20-02-1985',
                    'id_number':  5678
                },
                'expected': 95
            }
        ]

        for pair in pairs:
            person1 = Person(**pair['person1'])
            person2 = Person(**pair['person2'])
            probability = compare_persons(person1, person2)
            assert pair['expected'] == compare_persons(person1, person2), (
                f"Incorrect probability determined, expected {pair['expected']} but computed {probability} \n" +
                f"{person1}\n" +
                f"{person2}"
            )