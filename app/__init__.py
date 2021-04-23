from models import Person
from app.python_parser import NameDenormalizer

dimunitives = NameDenormalizer()

def get_missing_percentage(person1: Person, person2: Person):
    fn_len = len(person1.first_name)
    sn_len = len(person2.first_name)
    missing = 0
    if fn_len <= sn_len:
        for char in person1.first_name:
            if not char in person2.first_name:
                missing+=1
        return missing / fn_len * 100
    else:
        for char in person2.first_name:
            if not char in person1.first_name:
                missing+=1
        return missing / sn_len * 100


def get_firstname_probability(person1: Person, person2: Person):
    # first name equal
    if person1.first_name == person2.first_name:
        return 20

    person1_initial = None
    person2_initial = None
    # initial checks
    if '.' in person1.first_name:
        person1_initial = person1.first_name.split('.')[0]
    if '.' in person2.first_name:
        person2_initial = person2.first_name.split('.')[0]

    if person1_initial:
        if person2_initial and person1_initial == person2_initial:
            return 20
        if person1_initial == person2.first_name[0]:
            return 15

    if person2_initial:
        if person2_initial == person1.first_name[0]:
            return 15
    
    # check diminutives
    if person1.first_name in dimunitives:
        if person2.first_name in dimunitives[person1.first_name]:
            return 15
    
    if person2.first_name in dimunitives:
        if person1.first_name in dimunitives[person2.first_name]:
            return 15

    # check for typos & un-tracked dimunitives
    missing = get_missing_percentage(person1, person2)

    if missing <= 25.0:
        return 15

    return 0
def normalize_names(person1: Person, person2: Person):
    """
    returns persons with lower case names
    """
    person1.first_name = person1.first_name.lower()
    person1.last_name = person1.last_name.lower()

    person2.first_name = person2.first_name.lower()
    person2.last_name = person2.last_name.lower()

    return person1, person2

def compare_persons(person1: Person, person2: Person):
    """
    provided two persons, return probability that two persons 
    are the same individuals
    """
    person1, person2 = normalize_names(person1, person2)

    probability = 0
    if person1.id_number and person2.id_number:
        if person1.id_number == 'unknown' or person2.id_number == 'unknown':
            pass
        elif person1.id_number == person2.id_number:
            return 100

    probability+= get_firstname_probability(person1, person2)

    # last name comparison
    if person1.last_name == person2.last_name:
        probability+= 40
    
    # DOB - comparison
    if person1.date_of_birth and person2.date_of_birth:
        if person1.date_of_birth == person2.date_of_birth:
            probability+= 40

    return probability