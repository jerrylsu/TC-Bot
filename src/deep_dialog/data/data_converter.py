# -*- coding: utf-8 -*-
"""
# 将.p文件转为.json文件
"""
import os
import json
import cPickle as pickle


def pFile_to_jsonFile(pFile_path='movie_kb.v2.p', jsonFile_path='movie_kb.v2_.json'):
    with open(pFile_path, mode='rb') as fp:
        content = pickle.load(fp)
    # with open(jsonFile_path, mode='w') as fw:
    #     content_str = json.dumps(content)
    #     fw.write(content_str)
    json.dump(content, open(jsonFile_path, mode='w'))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(".p file to .json file")

    parser.add_argument('--pFile_path', dest='pFile',
                        type=str, default='user_goals_first_turn_template.part.movie.v1.p',
                        help='origin .p file path.')
    parser.add_argument('--jsonFile_path', dest='jsonFile',
                        type=str, default='user_goals_first_turn_template.part.movie.v1.json',
                        help='output .json file path.')

    args = parser.parse_args()

    # file_origin = 'user_goals_first_turn_template.part.movie.v1.p'
    # file_output = 'user_goals_first_turn_template.part.movie.v1.json'
    pFile_to_jsonFile(args.pFile, args.jsonFile)
