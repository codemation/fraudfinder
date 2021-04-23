from datetime import datetime
from easyadmin import Admin, buttons, forms, html_input, row, card, modal, admin
from fastapi.responses import HTMLResponse
from fastapi import HTTPException
from pydantic import ValidationError

from app import compare_persons
from models import Person

async def frontend_setup(server):

    server.admin = Admin(
        title='Fraud Detection',
        title_link = '/',
        side_bar_sections = [
            {
            'items':  [
                        {
                        'name':  'Calculate',
                        'href': '/',
                        'icon': 'calculator',
                        'items': []
                    },
                    {
                        'name':  'Scores',
                        'href': '/scores',
                        'icon': 'exclamation',
                        'items': []
                    },
                ]
            }
        ]
    )

    logout_modal = modal.get_modal(
        f'logoutModal',
        alert='Ready to Leave',
        body=buttons.get_button(
            'Go Back',
            color='success', 
            href=f'/'
        ) + 
        buttons.get_button(
            'Log out',
            color='danger',
            href='/logout'
        ),
        footer='',
        size='sm'
    )

    @server.get('/', response_class=HTMLResponse,  groups=['administrators'],  send_token=True, include_in_schema=False)
    async def root_page(access_token = None):

        compare_form = forms.get_form(
            f'Compare Persons',
            [
                row.get_row(
                    body=card.get_card(
                        name='Person1', 
                        body= card.get_card(
                            name='First and Last Name',
                            body=row.get_row(
                                body=html_input.get_text_input("first_name_p1") +
                                    html_input.get_text_input("last_name_p1")
                            ),
                            size=12
                            )+
                            card.get_card(
                                name='Date of Birth',
                                body=row.get_row(
                                    body=html_input.get_text_input("day_p1", size=4) +
                                        html_input.get_text_input("month_p1", size=4) +
                                        html_input.get_text_input("year_p1", size=4),
                                ),
                                size=12
                            )+
                            card.get_card(
                                name='ID Number',
                                body=row.get_row(
                                    body=html_input.get_text_input("id_number_p1", size=12)
                                ),
                                size=12
                            ),
                        size=6
                    )+
                    card.get_card(
                        name='Person2', 
                        body= card.get_card(
                            name='First and Last Name',
                            body=row.get_row(
                                body=html_input.get_text_input("first_name_p2") +
                                    html_input.get_text_input("last_name_p2")
                            ),
                            size=12
                            )+
                            card.get_card(
                                name='Date of Birth',
                                body=row.get_row(
                                    body=html_input.get_text_input("day_p2", size=4) +
                                        html_input.get_text_input("month_p2", size=4) +
                                        html_input.get_text_input("year_p2", size=4),
                                ),
                                size=12
                            )+
                            card.get_card(
                                name='ID Number',
                                body=row.get_row(
                                    body=html_input.get_text_input("id_number_p2", size=12)
                                ),
                                size=12
                            ),
                        size=6
                    )
                )
            ],
            submit_name='Screen Users',
            method='post',
            action=f'/compare'
        )
        compare_page = admin.get_admin_page(
            name='Screen Persons', 
            sidebar=server.admin.sidebar,
            body=compare_form,
            current_user=access_token['permissions']['users'][0],
            modals=logout_modal
        )
        return compare_page

    @server.post('/compare',  groups=['administrators'], include_in_schema=False)
    async def compare_from_gui(data: dict):
        birth_dates = {}
        for p in ['p1', 'p2']:
            birth_dates[p] = ''
            for date in ['day', 'month', 'year']:
                if data[f'{date}_{p}'] == '':
                    birth_dates[p] = 'unknown'
                    break
            day = data[f'day_{p}']
            month = data[f'month_{p}']
            year = data[f'year_{p}']
            birth_dates[p] = f"{day}-{month}-{year}"
        try:
            person1 = Person(
                first_name=data['first_name_p1'],
                last_name=data['last_name_p1'],
                date_of_birth=birth_dates['p1'],
                id_number='unknown' if data['id_number_p1'] == ''  else data['id_number_p1']
            )
            person2 = Person(
                first_name=data['first_name_p2'],
                last_name=data['last_name_p2'],
                date_of_birth=birth_dates['p2'],
                id_number='unknown' if data['id_number_p2'] == ''  else data['id_number_p2']
            )
        except ValidationError as e:
            return f"{repr(e)}"

        probability = compare_persons(person1, person2)
        await server.db.tables['scores'].insert(**{
            'date_detected': datetime.now().isoformat(),
            'full_name_p1': person1.first_name + ' ' + person1.last_name,
            'full_name_p2': person2.first_name + ' ' + person2.last_name,
            'score': probability
        })
        return probability

    @server.get('/scores', response_class=HTMLResponse,  groups=['administrators'], send_token=True, include_in_schema=False)
    async def scores(access_token=None):
        scores = await server.db.tables['scores'].select('*')
        return server.admin.table_page(
            'Risk Scores',
            scores if len(scores) > 0 else [
                {'date_detected': 'Nothing Checked Yet', 'full_name_p1': None, 'full_name_p2': None, 'score': None}
            ],
            current_user=access_token['permissions']['users'][0],
            above='',
            below=logout_modal
        )