import cv2
import os
import argparse

visualization = False

path_to_obj_train_data = 'data/obj_train_data'
in_file_path = r'C:\Users\ASUS\darknet\build\darknet\x64\data\obj_train_data_testing'
out_file_path = r'C:\Users\ASUS\darknet\build\darknet\x64\data\obj_train_data_testing'
output_list = []
images = []
txts = []
mode = 'flip'
output_train_txt = 'train'+'_'+mode+'.txt'


def main():
    num_image_process=0
    get_path(in_file_path)
    for index, image in enumerate(images):
        num_image_process+=1
        BBoxes = []
        if len(txts) > 0:
            with open(txts[index], 'r') as lines:
                for line in lines:
                    line = line.strip()
                    BBox = line.split(' ')
                    BBoxes.append(BBox)

        image_name = image
        image = cv2.imread(image)

        image, BBoxes = hflip(image, BBoxes)

        if visualization:
            visualize(image, BBoxes)
        else:
            makefile(image, BBoxes, image_name, in_file_path, out_file_path,path_to_obj_train_data, mode)

    if not visualization:
        os.chdir(out_file_path)
        with open(output_train_txt, 'w') as file:
            file.writelines('%s\n' % path for path in output_list)
    print(num_image_process,'images had been processed!')


def get_path(_infile_path):
    os.chdir(_infile_path)
    for file in sorted(os.listdir()):
        if file.endswith('.jpg') or file.endswith('.jpeg') or file.endswith('.png'):
            images.append(file)
    for file in sorted(os.listdir()):
        if file.endswith('.txt'):
            txts.append(file)


def hflip(img, bboxes):
    flipped_bboxes = []
    img = cv2.flip(img, 1)
    for bbox in bboxes:
        x_centre = bbox[1]
        x_centre = '{:.6f}'.format(1 - float(x_centre))
        bbox[1] = x_centre

        flipped_bbox = bbox
        flipped_bboxes.append(flipped_bbox)

    return img, flipped_bboxes


def visualize(img, bboxes):
    for bbox in bboxes:
        x_centre, y_centre, width, height = bbox[1:]

        x_centre = float(x_centre) * img.shape[1]
        y_centre = float(y_centre) * img.shape[0]
        width = float(width) * img.shape[1]
        height = float(height) * img.shape[0]

        x_start = int(x_centre - (width / 2))
        y_start = int(y_centre - (height / 2))
        startpoint = (x_start, y_start)

        x_end = int(x_start + width)
        y_end = int(y_start + height)
        endpoint = (x_end, y_end)

        cv2.rectangle(img, startpoint, endpoint, [255, 0, 0], 1)
    cv2.imshow('visualization', img)
    cv2.waitKey(0)


def makefile(_image, _bboxes, _image_name, _infile_path, _outfile_path, _make_path, _mode):
    if _image_name.endswith('.jpg'):
        ext = '.jpg'
    elif _image_name.endswith('.jpeg'):
        ext = '.jpeg'
    elif _image_name.endswith('.png'):
        ext = '.png'
    else:
        print('file extension is not supported')
        return

    os.chdir(_outfile_path)
    file = _image_name.replace(ext, '_' + _mode + ext)
    output_list.append(_make_path + '/' + file)
    cv2.imwrite(file, _image)

    file = _image_name.replace(ext, '_' + _mode + '.txt')
    with open(file, 'w') as file:
        for _bbox in _bboxes:
            file.writelines('%s ' % word for word in _bbox)
            file.writelines('\n')

    os.chdir(_infile_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('input', type=str, help='path to images for processing')
    parser.add_argument('output', type=str, help='path to output images ')
    parser.add_argument('-v', '--visual', action='store_true',
                        help='put -v flag if only want to visualize the output images')
    parser.add_argument('-p', '--path', type=str, default=path_to_obj_train_data,
                        help='path to images for processed in term of darknet root directory.')

    args = parser.parse_args()

    in_file_path = args.input
    out_file_path = args.output
    path_to_obj_train_data = args.path

    if args.visual:
        visualization = True
    else:
        visualization = False

    main()
