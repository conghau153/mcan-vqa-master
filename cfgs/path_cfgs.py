# --------------------------------------------------------
# mcan-vqa (Deep Modular Co-Attention Networks)
# Licensed under The MIT License [see LICENSE for details]
# Written by Yuhao Cui https://github.com/cuiyuhao1996
# --------------------------------------------------------

import os


class PATH:
    def __init__(self):

        # vqav2 dataset root path
        self.DATASET_PATH = './datasets/vqa-en/'

        # bottom up features root path
        self.FEATURE_PATH = './datasets/coco_extract/'

        self.init_path()

    def init_path(self):

        self.IMG_FEAT_PATH = {
            'train': self.FEATURE_PATH + 'train/',
            'val': self.FEATURE_PATH + 'val/',
            'test': self.FEATURE_PATH + 'test/',
        }

        self.QUESTION_PATH = {
            'train': self.DATASET_PATH + 'questions_train.json',
            'val': self.DATASET_PATH + 'questions_val.json',
            'test': self.DATASET_PATH + 'questions_test.json',
            'vg': self.DATASET_PATH + 'VG_questions.json',
        }

        self.ANSWER_PATH = {
            'train': self.DATASET_PATH + 'annotations_train.json',
            'val': self.DATASET_PATH + 'annotations_val.json',
            'vg': self.DATASET_PATH + 'VG_annotations.json',
        }

        self.RESULT_PATH = './results/result_test/'
        self.PRED_PATH = './results/pred/'
        self.CACHE_PATH = './results/cache/'
        self.LOG_PATH = './results/log/'
        self.CKPTS_PATH = './ckpts/'

        if 'result_test' not in os.listdir('./results'):
            os.mkdir('./results/result_test')

        if 'pred' not in os.listdir('./results'):
            os.mkdir('./results/pred')

        if 'cache' not in os.listdir('./results'):
            os.mkdir('./results/cache')

        if 'log' not in os.listdir('./results'):
            os.mkdir('./results/log')

        if 'ckpts' not in os.listdir('./'):
            os.mkdir('./ckpts')

    def check_path(self):
        print('Checking dataset ...')

        for mode in self.IMG_FEAT_PATH:
            if not os.path.exists(self.IMG_FEAT_PATH[mode]):
                print(self.IMG_FEAT_PATH[mode] + 'NOT EXIST')
                exit(-1)

        for mode in self.QUESTION_PATH:
            if not os.path.exists(self.QUESTION_PATH[mode]):
                print(self.QUESTION_PATH[mode] + 'NOT EXIST')
                exit(-1)

        for mode in self.ANSWER_PATH:
            if not os.path.exists(self.ANSWER_PATH[mode]):
                print(self.ANSWER_PATH[mode] + 'NOT EXIST')
                exit(-1)

        print('Finished')
        print('')

