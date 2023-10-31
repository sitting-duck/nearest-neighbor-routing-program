def extract_submatrix(matrix, indices):
    # print(f"extract_submatrix() indices: {indices}")
    submatrix = []
    for i in indices:
        row = []
        for j in indices:
            # print(f"i: {i} j: {j} matrix_ij: {matrix[i - 1][j - 1]}")
            row.append(matrix[i][j])
        submatrix.append(row)
    return submatrix

def get_submatrix(matrix, start_row, end_row, start_col, end_col):
    return [row[start_col:end_col + 1] for row in matrix[start_row:end_row + 1]]

def get_indices_for_locations(unique_locations, location_strings):
    # now get the list of location coordinates that match these addresses in the original adj_matrix
    indices = []
    for unique_location in unique_locations:
        for lstring in location_strings:
            if lstring == unique_location:
                new_index = location_strings.index(unique_location)
                # print(f"adding index {new_index} for location: {unique_location}")
                indices.append(new_index)
    return indices