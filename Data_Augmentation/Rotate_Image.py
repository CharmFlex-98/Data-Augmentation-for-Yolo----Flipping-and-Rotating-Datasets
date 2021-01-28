import os
import cv2
import numpy as np
import random
from Flip_Image import visualize, makefile, get_path, images, txts, output_list
import argparse

visualization = False
in_file_path = r'C:\Users\ASUS\darknet\build\darknet\x64\data\obj_train_data_testing'
out_file_path = r'C:\Users\ASUS\darknet\build\darknet\x64\data\obj_train_data_testing'
path_to_obj_train_data = 'data/obj_train_data'
mode = 'rotate'
output_train_txt = 'train' + '_' + mode + '.txt'
Min = 0
Max = 0


class yoloRotatebbox:
    def __init__(self, imagename, txtname, angle):

        self.imagename = imagename
        self.angle = angle
        self.txtname = txtname

        # Read image using cv2
        self.image = cv2.imread(self.imagename, 1)

        # create a 2D-rotation matrix
        rotation_angle = self.angle * np.pi / 180
        self.rot_matrix = np.array(
            [[np.cos(rotation_angle), -np.sin(rotation_angle)], [np.sin(rotation_angle), np.cos(rotation_angle)]])

    def rotate_image(self):
        """
        Rotates an image (angle in degrees) and expands image to avoid cropping
        """
        height, width = self.image.shape[:2]  # image shape has 3 dimensions
        image_center = (width / 2,
                        height / 2)  # getRotationMatrix2D needs coordinates in reverse order (width, height)
        # compared to shape

        rotation_mat = cv2.getRotationMatrix2D(image_center, self.angle, 1.)

        # rotation calculates the cos and sin, taking absolutes of those.
        abs_cos = abs(rotation_mat[0, 0])
        abs_sin = abs(rotation_mat[0, 1])

        # find the new width and height bounds
        bound_w = int(height * abs_sin + width * abs_cos)
        bound_h = int(height * abs_cos + width * abs_sin)

        # subtract old image center (bringing image back to origin) and adding the new image center coordinates
        rotation_mat[0, 2] += bound_w / 2 - image_center[0]
        rotation_mat[1, 2] += bound_h / 2 - image_center[1]

        # rotate image with the new bounds and translated rotation matrix
        rotated_mat = cv2.warpAffine(self.image, rotation_mat, (bound_w, bound_h))
        return rotated_mat

    def rotateYolobbox(self):

        new_height, new_width = self.rotate_image().shape[:2]

        f = open(self.txtname, 'r')

        f1 = f.readlines()

        new_bbox = []

        H, W = self.image.shape[:2]

        for x in f1:
            bbox = x.strip('\n').split(' ')
            if len(bbox) > 1:
                (center_x, center_y, bbox_width, bbox_height) = yoloFormattocv(float(bbox[1]), float(bbox[2]),
                                                                               float(bbox[3]), float(bbox[4]), H, W)

                # shift the origin to the center of the image.
                upper_left_corner_shift = (center_x - W / 2, -H / 2 + center_y)
                upper_right_corner_shift = (bbox_width - W / 2, -H / 2 + center_y)
                lower_left_corner_shift = (center_x - W / 2, -H / 2 + bbox_height)
                lower_right_corner_shift = (bbox_width - W / 2, -H / 2 + bbox_height)

                new_lower_right_corner = [-1, -1]
                new_upper_left_corner = []

                for i in (upper_left_corner_shift, upper_right_corner_shift, lower_left_corner_shift,
                          lower_right_corner_shift):
                    new_coords = np.matmul(self.rot_matrix, np.array((i[0], -i[1])))
                    x_prime, y_prime = new_width / 2 + new_coords[0], new_height / 2 - new_coords[1]
                    if new_lower_right_corner[0] < x_prime:
                        new_lower_right_corner[0] = x_prime
                    if new_lower_right_corner[1] < y_prime:
                        new_lower_right_corner[1] = y_prime

                    if len(new_upper_left_corner) > 0:
                        if new_upper_left_corner[0] > x_prime:
                            new_upper_left_corner[0] = x_prime
                        if new_upper_left_corner[1] > y_prime:
                            new_upper_left_corner[1] = y_prime
                    else:
                        new_upper_left_corner.append(x_prime)
                        new_upper_left_corner.append(y_prime)
                #             print(x_prime, y_prime)

                new_bbox.append([bbox[0], new_upper_left_corner[0], new_upper_left_corner[1],
                                 new_lower_right_corner[0], new_lower_right_corner[1]])

        return new_bbox


def main():
    num_image_process = 0
    get_path(in_file_path)
    for index, image in enumerate(images):
        num_image_process += 1
        instance = yoloRotatebbox(image, txts[index], random.randint(Min, Max))
        image_name = image
        image = instance.rotate_image()
        bboxes = []
        for bbox in instance.rotateYolobbox():
            coordinates = cvFormattoyolo(bbox, image.shape[0], image.shape[1])
            for num, i in enumerate(coordinates):
                bbox[num + 1] = i
            bboxes.append(bbox)
        if visualization:
            visualize(image, bboxes)
        else:
            makefile(image, bboxes, image_name, in_file_path, out_file_path, path_to_obj_train_data, mode)

    if not visualization:
        with open(output_train_txt, 'w') as file:
            file.writelines('%s\n' % path for path in output_list)

    print(num_image_process, 'images had been processed!')


def yoloFormattocv(centre_x, centre_y, width, height, image_height, image_width):
    centre_x *= image_width
    centre_y *= image_height
    width *= image_width
    height *= image_height

    voc = []

    voc.append(centre_x - (width / 2))
    voc.append(centre_y - (height / 2))
    voc.append(centre_x + (width / 2))
    voc.append(centre_y + (height / 2))

    return [int(v) for v in voc]


def cvFormattoyolo(bbox, image_height, image_width):
    width = bbox[3] - bbox[1]
    height = bbox[4] - bbox[2]
    centre_x = bbox[1] + (width / 2)
    centre_y = bbox[2] + (height / 2)

    centre_x = '{:.6f}'.format(centre_x / image_width)
    centre_y = '{:.6f}'.format(centre_y / image_height)
    width = '{:.6f}'.format(width / image_width)
    height = '{:.6f}'.format(height / image_height)

    return [centre_x, centre_y, width, height]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('input', type=str, help='path to images for processing')
    parser.add_argument('output', type=str, help='path to output images ')
    parser.add_argument('-v', '--visual', action='store_true',
                        help='put -v flag if only want to visualize the output images')
    parser.add_argument('-min', '--MinDegree', type=int, default=-90,
                        help='put -min flag if want to change minimum degree of rotation')
    parser.add_argument('-max', '--MaxDegree', type=int, default=90,
                        help='put -max flag if want to change maximum degree of rotation')
    parser.add_argument('-p', '--path', type=str, default=path_to_obj_train_data,
                        help='path to images for processed in term of darknet root directory.')

    args = parser.parse_args()

    in_file_path = args.input
    out_file_path = args.output
    path_to_obj_train_data = args.path

    Min = args.MinDegree

    Max = args.MaxDegree

    if args.visual:
        visualization = True
    else:
        visualization = False

    main()
