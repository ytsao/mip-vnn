from typing import List, Tuple
from functools import partial

import numpy as np
from jax import jit
import jax.numpy as jnp
from jax.experimental.host_callback import call

from util import read_dataset
from util.parameters_networks import NetworksStructure
from util.parameters_networks import DataSet


class Similarity:

    # // Example of using jit and jnp.ndarray to compute distance matrix and print it out.
    # // [20240703] this function is not used in this project.
    # //            it is replaced by generate_distance_matrix() function.
    # @staticmethod
    # @jit
    # def _generate_l1_distance_matrix(all_data: List[jnp.ndarray]) -> jnp.ndarray:
    #     """
    #     generate L1-norm distance matrix between all data points.
    #     """

    #     num_data: int = len(all_data)
    #     all_data: jnp.ndarray = jnp.array(all_data)

    #     # # * all_data.shape() := (971, 784)
    #     # # * all_data[:, None, :].shape := (971, 1, 784)
    #     # # * all_data[None, :, :].shape := (1, 971, 784)
    #     # difference: jnp.ndarray = all_data[:, None, :] - all_data[None, :, :]
    #     # print("difference: ")
    #     # distance_matrix = jnp.sum(jnp.abs(difference), axis=-1)
    #     # print("sum")
    #     # # distance_matrix = distance_matrix.at[jnp.diag_indices(num_data)].set(0)
    #     A: jnp.ndarray = all_data[:, None, :]
    #     B: jnp.ndarray = all_data[None, :, :]
    #     # distance_matrix: jnp.ndarray = jnp.einsum('ijk', 'ijk->ij', A-B, A-B)

    #     # ? how to print the distance_matrix?
    #     # * solution : https://stackoverflow.com/questions/71548823/how-to-print-with-jax
    #     # call(lambda x: print(x), distance_matrix)

    #     # assert distance_matrix.shape == (num_data, num_data), "L1-norm distance matrix shape is wrong"

    #     distance_matrix: jnp.ndarray = jnp.zeros((len(all_data), len(all_data)))

    #     return distance_matrix

    @staticmethod
    def generate_distance_matrix(all_data: List[jnp.ndarray], distance_type: str = "l1", chunk_size: int = 100) -> jnp.ndarray:

        # TODO: add more distance types.
        @jit
        def compute_l0_distance(difference: jnp.ndarray) -> jnp.ndarray:
            return jnp.count_nonzero(difference, axis=-1)

        @jit
        def compute_l1_distance(difference: jnp.ndarray) -> jnp.ndarray:
            return jnp.sum(jnp.abs(difference), axis=-1)

        @jit
        def compute_l2_distance(difference: jnp.ndarray) -> jnp.ndarray:
            return jnp.sqrt(jnp.sum(jnp.square(difference), axis=-1))

        @jit
        def compute_linf_distance(difference: jnp.ndarray) -> jnp.ndarray:
            return jnp.max(jnp.abs(difference), axis=-1)

        num_data: int = len(all_data)
        distance_matrix: np.ndarray = np.zeros((num_data, num_data))
        all_data: jnp.ndarray = jnp.array(all_data)

        for i in range(0, num_data, chunk_size):
            for j in range(0, num_data, chunk_size):
                chunk_dataA: jnp.ndarray = all_data[i: i + chunk_size]
                chunk_dataB: jnp.ndarray = all_data[j: j + chunk_size]

                differences: jnp.ndarray = chunk_dataA[:,
                                                       None, :] - chunk_dataB[None, :, :]

                if distance_type == "l1":
                    distance: jnp.ndarray = compute_l1_distance(differences)
                elif distance_type == "l2":
                    distance: jnp.ndarray = compute_l2_distance(differences)
                elif distance_type == "linf":
                    distance: jnp.ndarray = compute_linf_distance(differences)
                else:
                    raise ValueError("distance type is not supported")

                distance_matrix[i:i+chunk_size, j:j +
                                chunk_size] = np.array(distance)
        np.fill_diagonal(distance_matrix, 0)

        return jnp.array(distance_matrix)
    

    @staticmethod
    def greedy(distance_matrix: jnp.ndarray, num_clusters: int = 2) -> List[int]:
        """
        greedy algorithm to cluster data points.

        this version:
            - find the closest two data points and merge them into one cluster.
            - default data is first one.
        """
        reference_data: int = 0
        similarity_data = jnp.argsort(distance_matrix[reference_data])

        return similarity_data.tolist()