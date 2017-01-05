import json
from w2v import W2V
import argparse
import os
import sys
import scipy.spatial.distance as d
from operator import itemgetter


def game(state, w2v, filename, threshold):
    """
    The main game loop
    """
    def similarity_fun(a, b):
        return 1 - abs(d.braycurtis(a, b))

    while True:
        print("Unlocked elements: {}".format(", ".join(state["unlocked"])))
        line = input("Enter a sum of two elements: ")
        parts = [x.strip().lower() for x in line.split("+")]
        if len(parts) == 2:
            for x in parts:
                if x not in state["unlocked"]:
                    print("{} is not available.".format(x))
                    break
            else:
                a, b = parts
                va, vb = w2v[a], w2v[b]
                vsum = va + vb
                similarities = ((x, similarity_fun(vsum, w2v[x])) for x in state["available"] if x not in state["unlocked"])
                result, similarity = max(similarities, key=itemgetter(1))
                if similarity > threshold and result not in state["unlocked"]:
                    print("Result is \033[0;32m{}\033[0m with similarity {}".format(result, similarity))
                    state["unlocked"].append(result)
                elif similarity > threshold:
                    print("Result is {} with similarity {} (was already unlocked)".format(result, similarity))
                else:
                    print("\033[0;31mNo result was found\033[0m (best similarity was {} with value {})".format(result, similarity))
        else:
            print("Invalid input.")
        print()
        with open(filename, "w") as fp:
            json.dump(state, fp)


def prepare_state(state, w2v):
    """
    Removes unknown words from the available words and invalid unlocked words
    """
    unknown_words = [word for word in state["available"] if word not in w2v]
    if len(unknown_words) > 0:
        print("Unknown words: {}".format(", ".join(unknown_words)))
    state["available"] = [word for word in state["available"] if word in w2v]
    # in case you want to filter words that are in unlocked but not in available, uncomment these lines:
    # invalid_unlocked = [word for word in state["unlocked"] if word not in state["available"]]
    # if len(invalid_unlocked) > 0:
    #     print("Invalid unlocked words: {}".format(", ".join(invalid_unlocked)))
    # state["unlocked"] = [word for word in state["unlocked"] if word in state["available"]]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--word2vec", type=str, default="GoogleNews.h5", help="The Word2Vec table file to use (defaults to GoogleNews.h5)")
    parser.add_argument("-c", "--config", type=str, default="game_start.json", help="The game init json file to use for new games (defaults to game_start.json)")
    parser.add_argument("-t", "--threshold", type=float, default=0.2, help="The threshold value for accepted cosine distance of combination result")
    parser.add_argument("gamefile", type=str, help="The game file to use, the progress will be stored in this file")

    args = parser.parse_args()

    w2v = W2V(fn=args.word2vec)
    state = None
    # Load an existing game or start from config
    with open(args.gamefile if os.path.isfile(args.gamefile) else args.config, "r") as f:
        state = json.load(f)
    prepare_state(state, w2v)

    game(state, w2v, args.gamefile, args.threshold)


if __name__ == '__main__':
    main()
