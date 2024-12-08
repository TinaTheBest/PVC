from flask import Flask, render_template, request, jsonify
import time
from tsp import solve_tsp_heuristic, solve_tsp_exact, create_distance_matrix, solve_tsp_greedy
import math

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/solve', methods=['POST'])
def solve():
    # Récupérer les données en JSON
    data = request.get_json()

    # Récupérer les arêtes et la ville de départ
    edges = data['edges']
    start_city = data['start_city']
    
    # Parsing des arêtes et des coûts
    edges_list = parse_edges(edges)
    
    # Créer la matrice de distances à partir des arêtes
    cities = list(set([v for edge in edges_list for v in edge[:2]]))
    distance_matrix = create_distance_matrix(cities, edges_list)
    
    # Calculer la solution heuristique
    start_time = time.perf_counter()  # Utilisation de perf_counter pour une meilleure précision
    heuristic_cycle, heuristic_cost = solve_tsp_heuristic(cities, start_city, distance_matrix)
    heuristic_time = (time.perf_counter() - start_time) * 1e6  # Temps en microsecondes

    # Calcul de la solution greedy
    start_time = time.perf_counter()
    greedy_cycle, greedy_cost = solve_tsp_greedy(cities, start_city, distance_matrix)
    greedy_time = (time.perf_counter() - start_time) * 1e6  # Temps en microsecondes

    # Calcul de la solution exacte
    start_time = time.perf_counter()
    exact_cycle, exact_cost = solve_tsp_exact(cities, start_city, distance_matrix)
    exact_time = (time.perf_counter() - start_time) * 1e6  # Temps en microsecondes
    
    # Remplacer les valeurs infinies ou NaN par null (ou autre valeur valide)
    heuristic_cost = sanitize_value(heuristic_cost)
    exact_cost = sanitize_value(exact_cost)
    
    return jsonify({
        'heuristic_cycle': heuristic_cycle,
        'heuristic_cost': heuristic_cost,
        'heuristic_time': round(heuristic_time, 2),  # Temps en microsecondes, arrondi à 2 décimales
        'greedy_cycle': greedy_cycle,
        'greedy_cost': greedy_cost,
        'greedy_time': round(greedy_time, 2),  # Temps en microsecondes, arrondi à 2 décimales
        'exact_cycle': exact_cycle,
        'exact_cost': exact_cost,
        'exact_time': round(exact_time, 2)  # Temps en microsecondes, arrondi à 2 décimales
    })

def sanitize_value(value):
    # Si la valeur est infinie ou NaN, on la remplace par None
    if isinstance(value, float) and (math.isinf(value) or math.isnan(value)):
        return None  # ou une autre valeur valide, comme 0
    return value

def parse_edges(edges):
    edges = edges.replace(' ', '')  # Supprimer les espaces
    edges_list = []
    for edge in edges.split('),'):
        edge = edge.strip('()')
        parts = edge.split(',')
        if len(parts) != 3:
            raise ValueError(f"Edge format error: {edge}. Expected format: (v1, v2, cost).")
        v1, v2, cost = parts
        try:
            cost = int(cost)
        except ValueError:
            raise ValueError(f"Cost must be an integer. Got: {cost}")
        edges_list.append((v1, v2, cost))
    return edges_list


if __name__ == '__main__':
    app.run(debug=True)
