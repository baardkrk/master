from matplotlib import pyplot as plt
from data_loader import DataLoader


def show_depth_frame(kinect_node, idx, loader: DataLoader):
    array = loader.load_depth_frame(kinect_node, idx)
    plt.imshow(array, interpolation='nearest')
    plt.show()


def display_skeleton():
    pass


if __name__ == '__main__':
    loader = DataLoader('../data', '160226_haggling1')
    show_depth_frame('KINECTNODE6', 4592, loader)
