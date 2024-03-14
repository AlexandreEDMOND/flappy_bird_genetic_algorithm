from game import *
import matplotlib.pyplot as plt

def print_data(data_collect):
    # Transposer la matrice pour avoir les scores par génération
    scores_transposed = list(map(list, zip(*data_collect)))

    # Générer le graphique
    plt.figure(figsize=(10, 6))
    for i, gen_scores in enumerate(scores_transposed):
        plt.plot(range(1, len(gen_scores) + 1), gen_scores, label=f"Info {i+1}")

    plt.legend()
    plt.grid(True)
    plt.show()

def main():
    jeu = Game(True)
    score_jeu = jeu.main_loop()
    print(f"Score obtenue : {score_jeu}")
    print_data(jeu.data_collect)


if __name__ == "__main__":
    main()

