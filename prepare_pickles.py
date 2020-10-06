import os
import sys
import pickle

for module_dir in ['visionfuncs', 'EPypes', 'vcalib']:

    m_path = os.path.join('libraries', module_dir)
    if m_path not in sys.path:
        sys.path.append(m_path)

from vcalib import imsubsets
from visionfuncs.io import sorted_glob
from vcalib.pipelineclasses import CalibrationInput, CalibTriang, MeanDistInRows

DATA_DIR = 'data/images'
SAVE_DIR = 'data/pickles_new'

IM_WH = (1360, 1024)
PSIZE = (9, 7)
SQSIZE = 20.


def glob_images(data_dir, camera_idx):
    mask = os.path.join(data_dir, 'img_{}_*.jpg'.format(camera_idx))
    return sorted_glob(mask)


def pickle_object(obj, fname):
    
    with open(fname, 'wb') as f:
        pickle.dump(obj, f)


if __name__ == '__main__':

    imfiles_1 = glob_images(DATA_DIR, 1)
    imfiles_2 = glob_images(DATA_DIR, 2)

    calib_input = CalibrationInput(imfiles_1, imfiles_2, PSIZE, SQSIZE)
    calib_input.shuffle_indices()

    subsets = imsubsets.sample_subsets_different_size(calib_input.indices, 15, 30, n_subsets=200, seed=42)

    calib_triang = CalibTriang(calib_input, subsets)
    mdir = MeanDistInRows(calib_triang)

    if not os.path.exists(savedir):
        os.makedirs(savedir)

    pickle_object(subsets, os.path.join(SAVE_DIR, 'subsets.pkl'))
    pickle_object(calib_triang.triang, os.path.join(SAVE_DIR, 'triang.pkl'))
    pickle_object(mdir.metric_mat, os.path.join(SAVE_DIR, 'mdir.pkl'))