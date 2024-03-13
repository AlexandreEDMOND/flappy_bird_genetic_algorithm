from game import *

def main():
    jeu = Game(False, 100)
    score_jeu = jeu.main_loop()
    print(f"Score obtenue : {score_jeu}")


if __name__ == "__main__":
    main()