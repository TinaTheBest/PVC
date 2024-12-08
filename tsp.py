import itertools
import random
import string
import time

# Fonction pour créer la matrice de distances à partir des arêtes
def create_distance_matrix(cities, edges_list):
    """
    Crée une matrice de distances à partir des arêtes spécifiées.
    """
    distance_matrix = {city: {other_city: float('inf') for other_city in cities} for city in cities}
    
    for city1, city2, cost in edges_list:
        distance_matrix[city1][city2] = cost
        distance_matrix[city2][city1] = cost  
    
    return distance_matrix

# Fonction Heuristique : Plus proche voisin O(n^2)
def solve_tsp_heuristic(cities, start_city, distance_matrix):
    """
    Résout le problème du voyageur de commerce (TSP) en utilisant l'heuristique du plus proche voisin.
    """
    unvisited = set(cities)
    current_city = start_city
    path = [current_city]
    total_cost = 0
    
    unvisited.remove(current_city)
    
    while unvisited:
        # Trouver la ville non visitée la plus proche
        nearest_city = min(unvisited, key=lambda city: distance_matrix[current_city][city])
        total_cost += distance_matrix[current_city][nearest_city]
        current_city = nearest_city
        path.append(current_city)
        unvisited.remove(current_city)
    
    # Retourner à la ville de départ
    total_cost += distance_matrix[current_city][start_city]
    path.append(start_city)
    
    return path, total_cost

# Fonction Exacte : Branch and Bound (optimisé par élimination de branches) O(n!)
def solve_tsp_exact(cities, start_city, distance_matrix):
    """
    Résout le problème du voyageur de commerce (TSP) en utilisant la méthode Brute Force.
    """
    # Générer toutes les permutations possibles des villes restantes
    remaining_cities = [city for city in cities if city != start_city]
    all_permutations = itertools.permutations(remaining_cities)

    min_cost = float('inf')
    best_path = []

    # Parcourir chaque permutation et calculer le coût du chemin
    for perm in all_permutations:
        # Calculer le coût du chemin pour cette permutation
        current_cost = 0
        current_path = [start_city] + list(perm)

        # Calculer le coût total de ce chemin (de la ville de départ jusqu'à la dernière ville, puis retour à la ville de départ)
        for i in range(len(current_path) - 1):
            current_cost += distance_matrix[current_path[i]][current_path[i + 1]]
        
        # Retour à la ville de départ
        current_cost += distance_matrix[current_path[-1]][start_city]

        # Mettre à jour le coût minimal et le meilleur chemin si nécessaire
        if current_cost < min_cost:
            min_cost = current_cost
            best_path = current_path + [start_city]  # Ajouter le retour à la ville de départ

    return best_path, min_cost

def solve_tsp_greedy(cities, start_city, distance_matrix):
    """
    Résout le problème du voyageur de commerce (TSP) en utilisant l'heuristique Greedy.
    Cette méthode choisit la ville la plus proche parmi celles non visitées, mais avec une approche différente.
    """
    unvisited = set(cities)
    current_city = start_city
    path = [current_city]
    total_cost = 0
    
    unvisited.remove(current_city)
    
    while unvisited:
        # Choisir la ville avec le coût le plus faible parmi celles non visitées
        nearest_city = min(unvisited, key=lambda city: distance_matrix[current_city][city])
        total_cost += distance_matrix[current_city][nearest_city]
        current_city = nearest_city
        path.append(current_city)
        unvisited.remove(current_city)
    
    # Retourner à la ville de départ
    total_cost += distance_matrix[current_city][start_city]
    path.append(start_city)
    
    return path, total_cost