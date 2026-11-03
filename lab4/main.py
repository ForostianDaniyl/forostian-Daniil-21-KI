from func_pyfiglet import show_banner
from func_colorama import print_colored
from func_numpy import numpy_matrix_demo
from func_pandas import pandas_demo
from func_matplotlib import make_plot
from func_tqdm import progress_demo
from func_faker import fake_person
from func_dateutil import date_demo
from func_requests import build_request_url
from func_yaml import yaml_demo
from func_json import json_demo
from func_math import math_demo
from func_statistics import stats_demo
from func_collections import counter_demo
from func_hashlib import hash_demo


def main():
    show_banner("Lab 4")
    print_colored("Старт демонстрації бібліотек", "green")

    print("numpy:", numpy_matrix_demo())
    print("pandas:\n", pandas_demo())
    print("matplotlib:", make_plot())
    progress_demo()
    print("faker:", fake_person())
    print("dateutil:", date_demo())
    print("requests:", build_request_url())
    print("yaml:", yaml_demo())

    print("json:", json_demo())
    print("math:", math_demo())
    print("statistics:", stats_demo())
    print("collections:", counter_demo())
    print("hashlib:", hash_demo())

    print_colored("Готово!", "cyan")


if __name__ == "__main__":
    main()