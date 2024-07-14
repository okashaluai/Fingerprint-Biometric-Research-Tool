"""General-purpose test script for image-to-image translation.

Once you have trained your model with train.py, you can use this script to test the model.
It will load a saved model from '--checkpoints_dir' and save the results to '--results_dir'.

It first creates model and dataset given the option. It will hard-code some parameters.
It then runs inference for '--num_test' images and save results to an HTML file.

Example (You need to train models first or download pre-trained models from our website):
    Test a CycleGAN model (both sides):
        python generator.py --dataroot ./datasets/maps --name maps_cyclegan --model cycle_gan

    Test a CycleGAN model (one side only):
        python generator.py --dataroot datasets/horse2zebra/testA --name horse2zebra_pretrained --model test --no_dropout

    The option '--model test' is used for generating CycleGAN results only for one side.
    This option will automatically set '--dataset_mode single', which only loads the images from one set.
    On the contrary, using '--model cycle_gan' requires loading and generating results in both directions,
    which is sometimes unnecessary. The results will be saved at ./results/.
    Use '--results_dir <directory_path_to_save_result>' to specify the results directory.

    Test a pix2pix model:
        python generator.py --dataroot ./datasets/facades --name facades_pix2pix --model pix2pix --direction BtoA

See options/base_options.py and options/test_options.py for more test options.
See training and test tips at: https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix/blob/master/docs/tips.md
See frequently asked questions at: https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix/blob/master/docs/qa.md
"""
import ntpath
import os
import sys

import matplotlib.pyplot as plt
import numpy as np
from skimage.draw import line_nd, disk

from Dev.FingerprintGenerator.data import create_dataset
from Dev.FingerprintGenerator.models import create_model
from Dev.FingerprintGenerator.options.test_options import TestOptions
from Dev.FingerprintGenerator.util import util

try:
    import wandb
except ImportError:
    print('Warning: wandb package cannot be found. The option "--use_wandb" will result in error.')


def generate(input_images_dir: str, output_images_dir: str):
    opt = TestOptions().parse(input_images_dir)  # get test options
    # hard-code some parameters for test
    opt.num_threads = 0  # test code only supports num_threads = 0
    opt.batch_size = 1  # test code only supports batch_size = 1
    opt.serial_batches = True  # disable data shuffling; comment this line if results on randomly chosen images are needed.
    opt.no_flip = True  # no flip; comment this line if results on flipped images are needed.
    opt.display_id = -1  # no visdom display; the test code saves the results to a HTML file.
    dataset = create_dataset(opt)  # create a dataset given opt.dataset_mode and other options
    model = create_model(opt)  # create a model given opt.model and other options
    model.setup(opt)  # regular setup: load and print networks; create schedulers

    if opt.eval:
        model.eval()
    for i, data in enumerate(dataset):
        if i >= opt.num_test:  # only apply our model to opt.num_test images.
            break
        model.set_input(data)  # unpack data from data loader
        model.test()  # run inference
        visuals = model.get_current_visuals()  # get image results
        img_path = model.get_image_paths()  # get image paths
        if i % 5 == 0:  # save images to an HTML file
            print('processing (%04d)-th image... %s' % (i, img_path))

        # save images
        short_path = ntpath.basename(img_path[0])
        name = os.path.splitext(short_path)[0]

        for label, im_data in visuals.items():
            im = util.tensor2im(im_data)
            image_name = '%s_%s.png' % (name, label)
            save_path = os.path.join(output_images_dir, image_name)
            util.save_image(im, save_path, aspect_ratio=opt.aspect_ratio)


def __parse_minute_file(mnt_file_path):
    mnt = np.loadtxt(mnt_file_path)[:, :4]
    mnt[:, -1] = mnt[:, -1] * np.pi / 180  # Convert orientation from degrees to radians
    os.remove(mnt_file_path)
    return mnt


def __create_minutiae_map(mnts, size=(768, 832)):
    minutiae_map = np.zeros(size, dtype=np.uint8)
    for x, y in zip(mnts[:, 1], mnts[:, 2]):
        radius = 2  # adjust radius as needed
        rr, cc = disk(center=(y, x), radius=radius, shape=size)
        minutiae_map[rr, cc] = 255
    return minutiae_map


def __create_orientation_map(mnts, size=(768, 832), ori_length=15):
    orientation_map = np.zeros(size)
    for x, y, ori in zip(mnts[:, 1], mnts[:, 2], mnts[:, 3]):
        x, y = int(x), int(y)
        x1, y1 = x, y
        x2, y2 = x + ori_length * np.cos(ori), y - ori_length * np.sin(ori)
        line_idx = line_nd((y1, x1), (y2, x2), endpoint=True)
        orientation_map[line_idx] = 255
    return orientation_map


def __create_map_scipy(mnts, size=(768, 832), num_of_maps=3, ori_length=15, mnt_sigma=9, ori_sigma=3,
                       mnt_gain=60, ori_gain=3, include_singular=True):
    maps = []
    if include_singular:  # include core and delta points
        types = [[1], [2], [4, 5]]
    else:
        types = [[1], [2], [-1]]

    for idx in range(num_of_maps):
        minutiae_map = __create_minutiae_map(mnts[mnts[:, 0] == types[idx][0]], size)
        orientation_map = __create_orientation_map(mnts[mnts[:, 0] == types[idx][0]], size, ori_length)
        maps.append(minutiae_map + orientation_map)

    output = np.array(maps)

    output[output > 255] = 255
    output = output.swapaxes(0, 1)
    output = output.swapaxes(1, 2)
    output = output.astype(np.uint8)

    return output


def __convert_minutiae_to_array_list(min_file_path, output_dir):
    with open(min_file_path, 'r') as min_file:
        lines = min_file.readlines()

        # Extract the name of the .min file
        file_name = os.path.splitext(os.path.basename(min_file_path))[0]
        output_file_path = os.path.join(output_dir, file_name + ".txt")

        # Create a new .txt file for minutiae data
        with open(output_file_path, 'w') as output_file:
            for line in lines[3:]:  # Skip first three lines (header)
                line = line.strip()
                if line:
                    # Split the line into fields based on colons
                    fields = line.split(':')
                    quality = float(fields[3].strip())
                    # Check if quality is above 0.2 before writing to the file
                    if quality >= 0.2:
                        # Extract relevant information
                        mn_type = fields[4].strip()
                        x, y = map(int, fields[1].strip().split(','))
                        direction_unit = int(fields[2].strip())
                        # Convert direction_unit to degrees (0-360)
                        orientation = (90 - (11.25 * direction_unit)) % 360
                        minutiae_type = 1 if 'BIF' in mn_type else 2

                        # min_array_list.append([minutiae_type, x, y, (orientation * np.pi / 180)])
                        output_file.write(f"{minutiae_type} {x} {y} {orientation}\n")

    mnt_array_list = __parse_minute_file(output_file_path)
    return mnt_array_list


def __get_centralized_width_height(mnt_array):
    x_min = sys.maxsize
    y_min = sys.maxsize
    x_max = -1
    y_max = -1

    for m in mnt_array:
        x = m[1]
        y = m[2]

        if x < x_min:
            x_min = x
        if y < y_min:
            y_min = y

        if x > x_max:
            x_max = x
        if y > y_max:
            y_max = y

    length = int(max(x_max + x_min, y_max + y_min))
    return length, length  # width, height


def create_minutiae_map_image(templates_dir_path: str, min_maps_dir_path: str):
    templates_files = os.listdir(templates_dir_path)
    for template_file_path in templates_files:
        if template_file_path.endswith('.min'):
            template_min_file_name = os.path.splitext(template_file_path)[0]
            mnt_array_list = __convert_minutiae_to_array_list(os.path.join(templates_dir_path, template_file_path),
                                                              templates_dir_path)
            width, height = __get_centralized_width_height(mnt_array_list)
            min_map = __create_map_scipy(mnt_array_list, include_singular=False, size=(height, width))
            map_filename = os.path.join(min_maps_dir_path, f"{os.path.splitext(template_min_file_name)[0]}.png")
            plt.imsave(map_filename, min_map)


def create_temp_minutiae_map_image(template_path: str, min_map_dir_path: str):
    if not template_path.endswith('.min'):
        raise Exception("Template file must end with .min")
    template_parent_dir = os.path.dirname(template_path)
    template_min_file_name = os.path.basename(template_path)
    mnt_array_list = __convert_minutiae_to_array_list(template_path, template_parent_dir)
    width, height = __get_centralized_width_height(mnt_array_list)
    min_map = __create_map_scipy(mnt_array_list, include_singular=False, size=(height, width))
    map_filename = os.path.join(min_map_dir_path, f"{os.path.splitext(template_min_file_name)[0]}.png")
    plt.imsave(map_filename, min_map)
    return map_filename


def generate_image(template_dir_path: str, min_map_dir_path: str, image_dir: str):
    create_minutiae_map_image(template_dir_path, min_map_dir_path)
    generate(min_map_dir_path, image_dir)


def generate_images(templates_dir_path: str, min_maps_dir_path: str, images_dir: str):
    create_minutiae_map_image(templates_dir_path, min_maps_dir_path)
    generate(min_maps_dir_path, images_dir)
