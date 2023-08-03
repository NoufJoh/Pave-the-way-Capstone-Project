# -*- coding: utf-8 -*-
"""
Created on Thu Aug 3 2023

@author: NoufJOH
"""

import os
import random
from shutil import copyfile

# train, valid, test

def split_data(data_dir, output_dir, split=(0.7, 0.1, 0.2)):
    # Create the output directories if they don't exist
    train_dir = os.path.join(output_dir, 'train')
    test_dir = os.path.join(output_dir, 'test')
    valid_dir = os.path.join(output_dir, 'valid')
    for d in [train_dir, test_dir, valid_dir]:
        os.makedirs(os.path.join(d, 'images'), exist_ok=True)
        os.makedirs(os.path.join(d, 'labels'), exist_ok=True)

    # Get all image and label file paths
    img_paths = [os.path.join(data_dir, f) for f in os.listdir(data_dir) if f.endswith('.jpg')]
    txt_paths = [os.path.join(data_dir, f) for f in os.listdir(data_dir) if f.endswith('.txt')]

    # Extract the class labels from the file names
    labels = [0 if 'verypoor' in f else 1 for f in img_paths]

    # Shuffle the data while preserving the class distribution (making sure the split is balanced)
    data = list(zip(img_paths, txt_paths, labels))
    random.shuffle(data) # shuffle data
    img_paths, txt_paths, labels = zip(*data)

    # Split the data into train, validation, and test sets using stratified sampling
    n_train = int(len(img_paths) * split[0])
    n_valid = int(len(img_paths) * split[1])
    train_img_paths = img_paths[:n_train]
    train_txt_paths = txt_paths[:n_train]
    valid_img_paths = img_paths[n_train:n_train+n_valid]
    valid_txt_paths = txt_paths[n_train:n_train+n_valid]
    test_img_paths = img_paths[n_train+n_valid:]
    test_txt_paths = txt_paths[n_train+n_valid:]

    # Copy the files to the output directories
    print("Copying training data")
    for src_img, src_txt in zip(train_img_paths, train_txt_paths):
        dst_img = os.path.join(train_dir, 'images', os.path.basename(src_img))
        dst_txt = os.path.join(train_dir, 'labels', os.path.basename(src_txt))
        copyfile(src_img, dst_img)
        copyfile(src_txt, dst_txt)
        
    print("copying validation data")
    for src_img, src_txt in zip(valid_img_paths, valid_txt_paths):
        dst_img = os.path.join(valid_dir, 'images', os.path.basename(src_img))
        dst_txt = os.path.join(valid_dir, 'labels', os.path.basename(src_txt))
        copyfile(src_img, dst_img)
        copyfile(src_txt, dst_txt)
        
    print("copying testing data")    
    for src_img, src_txt in zip(test_img_paths, test_txt_paths):
        dst_img = os.path.join(test_dir, 'images', os.path.basename(src_img))
        dst_txt = os.path.join(test_dir, 'labels', os.path.basename(src_txt))
        copyfile(src_img, dst_img)
        copyfile(src_txt, dst_txt)

# split the data
data_dir = './data_annote'
output_dir = './op'
split_data(data_dir, output_dir)
print('Finshed!')