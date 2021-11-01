from loader import DataLoader
from random import shuffle
from target_maps import target_map
import time


def run(sequences, base_path):
    kinect_nodes = ['KINECTNODE1', 'KINECTNODE2', 'KINECTNODE3', 'KINECTNODE4',
                    'KINECTNODE5', 'KINECTNODE6', 'KINECTNODE7', 'KINECTNODE8',
                    'KINECTNODE9', 'KINECTNODE10']
    edges = [
        (0, 1), (0, 2), (1, 15), (15, 16), (0, 3), (3, 4), (4, 5),
        (2, 6), (6, 7), (7, 8), (1, 17), (17, 18), (0, 9), (9, 10),
        (10, 11), (2, 12), (12, 13), (13, 14)
    ]

    for sequence in sequences:
        loader = DataLoader(base_path, sequence)
        mi, ma = loader.min_max()
        ma = mi+25  # TODO : temporary
        for idx in range(mi, ma-len(kinect_nodes), len(kinect_nodes)):

            # shuffle(kinect_nodes)  # TODO : turn back on
            for i, node in enumerate(kinect_nodes):
                d_im, bodies, camera = loader.frame(idx+i, node)
                tmap = target_map(bodies, edges, camera, d_im.shape)

            # print(kinect_nodes)
    print('DONE')


if __name__ == '__main__':
    sequences = ['160226_haggling1']
    base_path = '../data'
    start = time.time()
    run(sequences, base_path)
    end = time.time()
    print(f'Done in {end - start} seconds')
