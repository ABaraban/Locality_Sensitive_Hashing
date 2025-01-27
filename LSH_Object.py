import scanpy as sc
import numpy as np
from pyproject.LSHMethods import insertToTable


class Hashing:
    def __init__(self, bucket_width, num_buckets, library, file, hash_vectors):
        self.bucket_width = bucket_width
        self.library = sc.read(library)
        self.file = sc.read(file)
        self.num_buckets = num_buckets
        self.hashtable = [[] for _ in range(num_buckets)]
        self.random_vector = None
        self.hash_vectors = sc.read(hash_vectors)

    def hash_LSH_Random_Vectors(self):
        self.random_vector = np.random.rand(1, self.file.n_obs)
        hashtable = [[] for _ in range(self.num_buckets)]
        library_indices = []
        for i in range(self.file.n_vars):
            vec = self.file.var_vector(i)
            insertToTable(self.hashtable, vec, self.random_vector, self.bucket_width)
        for i in range(self.library.n_vars):
            vec_lib = self.library.var_vector(i)
            index = insertToTable(self.hashtable, vec_lib, self.random_vector, self.bucket_width)
            library_indices.append(index)
        return hashtable, library_indices

    def hash_LSH_Chosen_Vector(self, hash_vector):
        hashtable = [[] for _ in range(self.num_buckets)]
        library_indices = []
        for i in range(self.file.n_vars):
            vec = self.file.var_vector(i)
            insertToTable(self.hashtable, vec, hash_vector, self.bucket_width)
        for i in range(self.library.n_vars):
            vec_lib = self.library.var_vector(i)
            index = insertToTable(self.hashtable, vec_lib, hash_vector, self.bucket_width)
            library_indices.append(index)
        return hashtable, library_indices

    def hash_multiple_times_Chosen(self, number_of_times):
        list_of_tables = []
        if number_of_times > self.hash_vectors.n_vars:
            number_of_times = self.hash_vectors.n_vars
        for i in range(number_of_times):
            hash_vector = self.hash_vectors.var_vector(i)
            list_of_tables.append(self.hash_LSH_Chosen_Vector(hash_vector))
        return list_of_tables

# I'm having some trouble figuring out how to do the intersection
    def hash_multiple_times_random(self, number_of_times):
        list_of_tables = []
        for i in range(number_of_times):
            list_of_tables.append(self.hash_LSH_Random_Vectors())
        return list_of_tables



