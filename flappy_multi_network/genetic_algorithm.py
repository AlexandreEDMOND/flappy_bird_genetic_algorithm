from game import *
from flappy import *
from copy import deepcopy
import matplotlib.pyplot as plt
from tqdm import tqdm

def training_loop():

    affichage_pyagme = True

    nmbr_generation = 10
    nmbr_population = 10
 
    pourcentage_selection = 0.3
    mutation_rate = 0.02

    nmbre_top_score = 5
    top_scores = []

    generation = [Flappy(150, 300) for _ in range(nmbr_population)]

    for gen in tqdm(range(nmbr_generation)):

        for flappy in generation:
            flappy.reset()

        jeu = Game(affichage_pyagme, generation)
        jeu.main_loop()
        score_generation = jeu.calcul_score()

        new_generation = []
        # print(f"Max génération {gen+1}: ", max(score_generation))
        top_scores.append(sorted(score_generation, reverse=True)[:nmbre_top_score])

        # Selection des meilleurs agents
        sorted_agents = [agent for _, agent in sorted(zip(score_generation, [i for i in range(nmbr_population)]), reverse=True)]
        for top_agent in sorted_agents[:int(nmbr_population*pourcentage_selection)]:
            new_generation.append(generation[top_agent])
        
        # Mutation des meilleurs agents
        for i in range(int(nmbr_population*pourcentage_selection)):
            for _ in range(1):
                new_game = deepcopy(new_generation[i])
                new_network = mutate(new_game.network, mutation_rate)
                new_game.network = new_network
                new_generation.append(new_game)
        
        # On complète avec des nouveaux agents
        for _ in range(2*int(nmbr_population*pourcentage_selection), nmbr_population):
            new_generation.append(Flappy(150, 300))
        
        generation = new_generation

        top_agents = generation[0].network
        torch.save(top_agents.state_dict(),f'network_trained/model_trained_gen_{gen+1}_score_{top_scores[gen][0]}.pth')
        

    # Affichage des entrainements
    print_top_scores(top_scores)

    return


def print_top_scores(top_score):
    # Transposer la matrice pour avoir les scores par génération
    scores_transposed = list(map(list, zip(*top_score)))

    # Générer le graphique
    plt.figure(figsize=(10, 6))
    for i, gen_scores in enumerate(scores_transposed):
        plt.plot(range(1, len(gen_scores) + 1), gen_scores, label=f"Top {i+1}")

    plt.xlabel('Génération')
    plt.ylabel('Score')
    plt.title('Évolution des scores par génération')
    plt.legend()
    plt.grid(True)
    plt.show()

def mutate(network, mutation_rate):
    for param in network.parameters():
        if len(param.shape) == 2:  # Vérifier si le paramètre est une matrice de poids
            mutation_mask = torch.rand_like(param) < mutation_rate
            param.data += torch.randn_like(param) * mutation_mask.float()
    return network