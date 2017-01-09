from __future__ import print_function
import argparse
from cascade import Cascade


def main():
    args = parse_args()
    p = args['p']

    g = Cascade.create_random_graph(1000)
    model = Cascade(g, p)
    model.generate_cascade_result(5)
    model.save(open("dump.p", "wb"))

    return


def parse_args():
    """Input arguments"""
    program_description = "Cascade mode grid search"
    parser = argparse.ArgumentParser(description=program_description)
    parser.add_argument('p', type=float, help='Immitation parameter')
    args = vars(parser.parse_args())
    return args


if __name__ == "__main__":
    main()
