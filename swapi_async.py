import asyncio
import aiohttp
import datetime
from more_itertools import chunked
from models import engine, Session, Base, SwapiPeople


async def get_people(people_id):

    session = aiohttp.ClientSession()
    response = await session.get(f'https://swapi.dev/api/people/{people_id}')
    json_data = await response.json()
    print(f'Collect: {json_data.get("name", "Unknow")}')

    species = []
    if 'species' in json_data.keys():
        for spec in json_data['species']:
            async with session.get(spec) as response_detail:
                json_scpecies_data = await response_detail.json()
                species.append(json_scpecies_data['name'])
        json_data['species'] = ', '.join(species)

    starships = []
    if 'starships' in json_data.keys():
        for starship in json_data['starships']:
            async with session.get(starship) as response_detail:
                json_starships_data = await response_detail.json()
                starships.append(json_starships_data['name'])
        json_data['starships'] = ', '.join(starships)

    vehicles = []
    if 'vehicles' in json_data.keys():
        for vehicle in json_data['vehicles']:
            async with session.get(vehicle) as response_detail:
                json_vehicles_data = await response_detail.json()
                vehicles.append(json_vehicles_data['name'])
        json_data['vehicles'] = ', '.join(vehicles)

    films = []
    if 'films' in json_data.keys():
        for film in json_data['films']:
            async with session.get(film) as response_detail:
                json_film_data = await response_detail.json()
                films.append(json_film_data['title'])
        json_data['films'] = ', '.join(films)

    await session.close()
    return json_data


async def paste_to_db(persons_json):
    async with Session() as session:
        orm_objects = [SwapiPeople(name=item.get('name', 'unknown'),
                                   birth_year=item.get('birth_year', 'unknown'),
                                   gender=item.get('gender', 'unknown'),
                                   mass=item.get('mass', 'unknown'),
                                   height=item.get('height', 'unknown'),
                                   eye_color=item.get('eye_color', 'unknown'),
                                   hair_color=item.get('hair_color', 'unknown'),
                                   skin_color=item.get('skin_color', 'unknown'),
                                   homeworld=item.get('homeworld', 'unknown'),
                                   species=item.get('species', 'unknown'),
                                   starships=item.get('starships', 'unknown'),
                                   vehicles=item.get('vehicles', 'unknown'),
                                   films=item.get('films', 'unknown'),) for item in persons_json]
        session.add_all(orm_objects)
        await session.commit()
        for orm in orm_objects:
            print(f'Paste to db: {orm}')


async def main():
    async with engine.begin() as con:
        await con.run_sync(Base.metadata.create_all)

    person_coros = (get_people(i) for i in range(1, 83))
    person_coros_chunked = chunked(person_coros, 5)

    for person_coros_chunk in person_coros_chunked:
        persons = await asyncio.gather(*person_coros_chunk)
        asyncio.create_task(paste_to_db(persons))
    
    tasks = asyncio.all_tasks() - {asyncio.current_task()}
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    start = datetime.datetime.now()
    asyncio.run(main())
    print(datetime.datetime.now() - start)
