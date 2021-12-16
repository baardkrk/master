from loader import DataLoader
from random import shuffle
from target_maps import target_map
from tqdm import trange
from concurrent.futures import ProcessPoolExecutor, as_completed
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
    failed_count = 0
    total_maps = 0
    for sequence in sequences:
        loader = DataLoader(base_path, sequence)
        mi, ma = loader.min_max()
        ma = mi+25  # TODO : temporary
        for idx in trange(mi, ma-len(kinect_nodes), len(kinect_nodes)):

            shuffle(kinect_nodes)  # TODO : turn back on

            with ProcessPoolExecutor() as executor:
                results = [executor.submit(create_tmap, loader, edges, i, node, idx)
                           for i, node in enumerate(kinect_nodes)]
                for f in as_completed(results):
                    total_maps += 1
                    try:
                        tmap, jmap, d_im = f.result()
                        # 217088*8*(1+19+18)*10
                        # Accumulate enough maps for about 10GB, then save compressed
                        if tmap.size*tmap.itemsize > 10000000000:
                            # Save the map with savez_compressed
                            # Clear accumulation map
                            pass
                        # size*itemsize*(d, j, e)*numkin*(maxidx)
                        # print(f'size: {tmap.size}, items: {tmap.dtype} ({tmap.itemsize} bytes)')
                    except ValueError:
                        failed_count += 1
                        continue

            # for i, node in enumerate(kinect_nodes):
            #     d_im, bodies, camera = loader.frame(idx+i, node)
            #     total_maps += 1
            #     try:
            #         tmap, _ = target_map(bodies, edges, camera, d_im.shape)
            #     except ValueError:
            #         # Failed to get TMAP
            #         failed_count += 1
            #         continue

            # print(kinect_nodes)
    print(f'FAILED: {failed_count}, TOTAL MAPS: {total_maps}')


def create_tmap(loader, edges, i, node, idx):
    d_im, bodies, camera = loader.frame(idx + i, node)
    tmap, jmap = target_map(bodies, edges, camera, d_im.shape)
    return tmap, jmap, d_im


if __name__ == '__main__':
    sequences = ['160226_haggling1']
    base_path = '../data'
    start = time.time()
    run(sequences, base_path)
    end = time.time()
    print(f'Done in {end - start} seconds')
