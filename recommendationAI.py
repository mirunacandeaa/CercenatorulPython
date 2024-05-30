
import firebase_admin
from firebase_admin import credentials, firestore
import numpy as np

class Hike:
    def __init__(self, place, region, difficulty, kilometers, duration):
        self.place = place
        self.region = region
        self.difficulty = difficulty
        self.kilometers = kilometers
        self.duration = duration

class Project:
    def __init__(self, name, trails):
        self.name = name
        self.trails = trails

def get_unique_hikes(projects_list):
    unique_hikes = []
    for project in projects_list:
        for hike in project.trails:
            if not any(existing_hike.place == hike.place for existing_hike in unique_hikes):
                unique_hikes.append(hike)
    return unique_hikes

def get_projects_and_hikes():
    cred = credentials.Certificate("C:/Users/Miru/Desktop/licenta/cercenatorul3000-5c8d6-9cabc90abaa0.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    collection = db.collection('Proiecte')
    project_docs = collection.stream()
    projects_list = []
    for project_doc in project_docs:
        project_name = project_doc.id
        hikes_collection = project_doc.reference.collection('Trasee')
        hike_docs = hikes_collection.stream()
        hikes_list = []
        for doc in hike_docs:
            hike_data = doc.to_dict()
            hike_instance = Hike(place=hike_data['place'], region=hike_data['region'],
                                 difficulty=hike_data['dificultate'], kilometers=hike_data['kilometers'],
                                 duration=hike_data['durata'])
            hikes_list.append(hike_instance)
        project_instance = Project(name=project_name, trails=hikes_list)
        projects_list.append(project_instance)
    return projects_list

def initialize_interaction_matrix(projects_list, unique_hikes):
    interaction_matrix = np.zeros((len(projects_list), len(unique_hikes)), dtype=int)
    for i, project in enumerate(projects_list):
        for j, hike in enumerate(unique_hikes):
            if hike.place in [trail.place for trail in project.trails]:
                interaction_matrix[i][j] = 1
    return interaction_matrix

def save_recommendation_to_firestore(project, hike):
    db = firestore.client()
    project_doc_ref = db.collection('Proiecte').document(project.name)
    doc_ref = project_doc_ref.collection('Recomandari').document(hike.place)
    doc_ref.set({
        'place': hike.place,
        'region': hike.region,
        'difficulty': hike.difficulty,
        'kilometers': hike.kilometers,
        'duration': hike.duration
    })

def collaborative_filtering():
    projects_list = get_projects_and_hikes()
    unique_hikes = get_unique_hikes(projects_list)
    interaction_matrix = initialize_interaction_matrix(projects_list, unique_hikes)
    current_project = projects_list[-1]
    current_project_index = len(projects_list) - 1
    project_similarities = {}
    for i, project in enumerate(projects_list):
        if i != current_project_index:
            other_project_hikes = [hike.place for hike in project.trails]
            common_hikes = [hike.place for hike in current_project.trails if hike.place in other_project_hikes]
            if common_hikes:
                similarity = len(common_hikes) / len(current_project.trails)
                project_similarities[project.name] = similarity

    recommendations = {}
    for i, hike in enumerate(unique_hikes):
        if interaction_matrix[current_project_index][i] == 0:
            hike_similarities = []
            for j, project in enumerate(projects_list):
                if interaction_matrix[j][i] == 1:
                    if project.name in project_similarities:
                        hike_similarities.append(project_similarities[project.name])
                    else:
                        hike_similarities.append(0)  # Sau o altă valoare default
            recommendations[hike] = sum(hike_similarities)

    sorted_recommendations = {k: v for k, v in sorted(recommendations.items(), key=lambda item: item[1], reverse=True)}
    print("\nRecommendations:")
    for hike, score in sorted_recommendations.items():
        if score != 0:
            print(f"{hike.place}: {score}")
            save_recommendation_to_firestore(current_project, hike)

def main():
    collaborative_filtering()

if __name__ == "__main__":
    main()
