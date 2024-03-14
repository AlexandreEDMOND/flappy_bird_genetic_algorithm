from game import *

def main():
    path_network = 'network_trained/model_trained_gen_31_score_28003.pth'
    jeu = Game(True, path_network)
    score_jeu = jeu.main_loop()
    print(f"Score obtenue : {score_jeu}")


if __name__ == "__main__":
    main()