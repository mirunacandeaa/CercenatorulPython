import requests
from bs4 import BeautifulSoup

class Hike:
    def __init__(self, region, place, difficulty, km, hour):
        self.region = region
        self.place = place
        self.difficulty = difficulty
        self.km = km
        self.hour = hour

    @classmethod
    def from_lists(cls, regions, places, difficulties, distances_km, distances_hours, index):
        return cls(
            regions[index],
            places[index],
            difficulties[index],
            distances_km[index],
            distances_hours[index]
        )

def get_hikes(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    regions = soup.select('div.field-name-field-regions')
    region_names = [region.text.strip() for region in regions]

    places = soup.select('div.field-name-outer-title-or-title')
    places_names = [place.text.strip() for place in places]

    difficulty_elements = soup.select('div.field-name-field-difficulty a')
    difficulties = [difficulty.text.strip() for difficulty in difficulty_elements]

    distance_elements = soup.find_all('div', class_='distance-km')

    distances_km = []
    distances_hours = []

    for distance in distance_elements:
        text = distance.text.strip()
        if text.endswith('km'):
            distances_km.append(text)
        elif text.endswith('h'):
            distances_hours.append(text)

    if len(region_names) == len(places_names) == len(difficulties) == len(distances_km) == len(distances_hours):
        hikes = []

        for i in range(len(region_names)):
            hike_instance = Hike.from_lists(region_names, places_names, difficulties, distances_km, distances_hours, i)
            hikes.append(hike_instance)

        return hikes
    else:
        print("Listele nu au aceeasi lungime!")
        return []

def get_first_hikes(urls):
    first_hikes = []
    for url in urls:
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')

        region = soup.select_one('div.field-name-field-regions').text.strip()
        place = soup.select_one('div.field-name-outer-title-or-title').text.strip()
        difficulty = soup.select_one('div.field-name-field-difficulty a').text.strip()

        distance_element = soup.find('div', class_='distance-km')
        if distance_element:
            text = distance_element.text.strip()
            if text.endswith('km'):
                km = text
                hour = None
            elif text.endswith('h'):
                hour = text
                km = None
        else:
            km = None
            hour = None

        hike = Hike(region, place, difficulty, km, hour)
        first_hikes.append(hike)
    return first_hikes

def get_last_hikes(urls):
    last_hikes = []
    for url in urls:
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')

        regions = soup.select('div.field-name-field-regions')
        region = regions[-1].text.strip() if regions else None

        places = soup.select('div.field-name-outer-title-or-title')
        place = places[-1].text.strip() if places else None

        difficulty_elements = soup.select('div.field-name-field-difficulty a')
        difficulty = difficulty_elements[-1].text.strip() if difficulty_elements else None

        distance_elements = soup.find_all('div', class_='distance-km')
        distance_element = distance_elements[-1] if distance_elements else None

        if distance_element:
            text = distance_element.text.strip()
            if text.endswith('km'):
                km = text
                hour = None
            elif text.endswith('h'):
                hour = text
                km = None
        else:
            km = None
            hour = None

        hike = Hike(region, place, difficulty, km, hour)
        last_hikes.append(hike)

    return last_hikes

def filter_hikes_by_region(hikes, user_input):
    filtered_hikes = []
    for hike in hikes:
        if user_input.lower() in hike.region.lower():
            filtered_hikes.append(hike)
    return filtered_hikes

def filter_hikes_by_difficulty(hikes, user_input):
    filtered_hikes = []
    for hike in hikes:
        if user_input.lower() in hike.difficulty.lower():
            filtered_hikes.append(hike)
    return filtered_hikes

def filter_hikes_by_duration(hikes, user_input):
    filtered_hikes = []
    for hike in hikes:
        if hike.hour is not None:
            if user_input.lower() in hike.hour.lower():
                filtered_hikes.append(hike)
        else:
            # Convertim durata în ore
            try:
                duration = int(user_input)
                # Extragem durata în ore din stringul hike.hour
                hike_duration = int(hike.hour.split()[0])
                # Verificăm dacă durata traseului este mai mică decât durata introdusă de utilizator
                if hike_duration < duration:
                    filtered_hikes.append(hike)
            except ValueError:
                # Handle cases where hike.hour cannot be split or converted to an integer
                continue
    return filtered_hikes

def get_url_filtered_region_list(wanted_region, urls):
    first_hikes = get_first_hikes(urls)
    last_hikes = get_last_hikes(urls)
    matching_urls = []
    found_urls = set()  # Va conține URL-urile deja găsite din first_hikes

    for hike in first_hikes + last_hikes:
        if wanted_region.lower() in hike.region.lower():
            if hike in first_hikes and hike.place not in found_urls:
                index = first_hikes.index(hike)
                matching_urls.append(urls[index])
                found_urls.add(hike.place)
            elif hike in last_hikes and hike.place not in found_urls:
                index = last_hikes.index(hike)
                url = urls[len(urls) - len(last_hikes) + index]
                if url not in matching_urls:  # Verificați dacă URL-ul este deja în lista matching_urls
                    matching_urls.append(url)
                    found_urls.add(hike.place)

    return matching_urls


def filtered_regions(user_input, urls):
     # Initialize url_list with an empty list
    if user_input.lower() in ["bucegi", "leaota"]:
        url_filtered_region_list = get_url_filtered_region_list(user_input, urls)
    if user_input.lower() in ["piatra craiului"]:
        url_filtered_region_list=get_url_filtered_region_list(user_input, urls)


    return url_filtered_region_list






def webscrapper(regiune, dificultate, durata):
    # Input de la utilizator
    wanted_region = regiune
    wanted_difficulty = dificultate
    wanted_duration = durata

    urls = [
        'https://muntii-nostri.ro/en/routes',
        'https://muntii-nostri.ro/en/routes?field_tour_type_tid=20&page=1',
        'https://muntii-nostri.ro/en/routes?field_tour_type_tid=20&page=2',
        'https://muntii-nostri.ro/en/routes?field_tour_type_tid=20&page=3',
        'https://muntii-nostri.ro/en/routes?field_tour_type_tid=20&page=4',
        'https://muntii-nostri.ro/en/routes?field_tour_type_tid=20&page=5',
        'https://muntii-nostri.ro/en/routes?field_tour_type_tid=20&page=6',
        'https://muntii-nostri.ro/en/routes?field_tour_type_tid=20&page=7',
        'https://muntii-nostri.ro/en/routes?field_tour_type_tid=20&page=8',
        'https://muntii-nostri.ro/en/routes?field_tour_type_tid=20&page=9',
        'https://muntii-nostri.ro/en/routes?field_tour_type_tid=20&page=10',
    ]


    filtered_regions_urls_list = filtered_regions(wanted_region, urls)

    # Preia datele și creează instanțele Hike pentru fiecare URL
    all_hikes = []
    for url in filtered_regions_urls_list:
        hikes = get_hikes(url)
        all_hikes.extend(hikes)

    # Filtrare trasee de drumeție
    filtered_hikes_region = filter_hikes_by_region(all_hikes, wanted_region)
    filtered_hikes_difficulty = filter_hikes_by_difficulty(filtered_hikes_region, wanted_difficulty)
    filtered_hikes_durata = filter_hikes_by_duration(filtered_hikes_difficulty, wanted_duration)

    # Afiseaza lista de instanțe Hike
    for hike in filtered_hikes_durata:
        print("Region:", hike.region)
        print("Place:", hike.place)
        print("Difficulty:", hike.difficulty)
        print("Kilometers:", hike.km)
        print("Hours:", hike.hour)

    return filtered_hikes_durata
