class Dataset:
    """
    The data loader class provides functionality for finding and loading the data
    from the test and validation sets.
    """
    def __init__(self, data_root_path, training_sequences, validation_sequences):
        self.data_root_path = data_root_path
        self.training_sequences = training_sequences
        self.validation_sequences = validation_sequences

    def get_training_batch(self, size):
        return self.__get_batch(self.training_sequences, size)

    def get_validation_batch(self, size):
        return self.__get_batch(self.validation_sequences, size)

    def __get_batch(sequence_array, size):
        pass

    def __calculate_average_training_input():
        pass

    def __get_training_sample(sequence, idx, kinect_n):
        """
        Returns a tuple with the depth image for the specified kinect and index, 
        and the ground truth body-part maps for the image.
        """
        
        pass
