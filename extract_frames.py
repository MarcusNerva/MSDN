#!/usr/bin/env python
# coding=utf-8
import os
import shutil
import subprocess
import glob
from tqdm import tqdm

def extract_frames(video, dir_path):
    with open(os.devnull, 'w') as ffmpeg_log:
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
        os.mkdir(dir_path)
        video_id = video.split('/')[-1].split('.')[0]
        video_id = video_id[5:]
        video_id = '%06d' % int(video_id)
        video_to_frames_command = ['ffmpeg', '-y', '-i', video, '-r', '5', '-vf', 'scale=400:300', '-qscale:v', '2',
                                   '{dir_path}/{vid}_%06d.jpg'.format(dir_path=dir_path, vid=video_id)]
        subprocess.call(video_to_frames_command)

        ret = glob.glob('{dir_path}/{vid}_*.jpg'.format(dir_path=dir_path, vid=video_id))
        ret = sorted(ret)

        return ret

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--output_dir', dest='output_dir', type=str, 
                        default='/disks/lilaoshi666/hanhua.ye/MSDN/MSRVTT_image',
                       help='directory to store images')
    parser.add_argument('--temp_dir', dest='temp_dir', type=str,
                       default='/disks/lilaoshi666/hanhua.ye/MSDN/MSRVTT_image/temp',
                       help='a cache to store images')
    parser.add_argument('--video_path', dest='video_path', type=str,
                       default='/disks/lilaoshi666/hanhua.ye/temp_data',
                       help='path to video dataset')

    args = parser.parse_args()
    params = vars(args)
    video_list = glob.glob(os.path.join(params['video_path']), '*.mp4')

    for video in tqdm(video_list):
        images = extract_frames(video, params['temp_dir'])
        samples = np.round(np.linspace(0, len(images) - 1, 20)).astype(np.int32)
        choosed = images[samples]

        for image_path in choosed:
            shutil.move(image_path, params['output_dir'])

    print('=============Done!==============')
