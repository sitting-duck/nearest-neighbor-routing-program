class CSVParser_Distances:
    """
    A class for parsing distance data from a CSV file and converting it into an adjacency matrix.

    Example usage:
    file_path = "path_to_your_csv_file.csv"
    parser = CSVParser_Distances(file_path)
    matrix = parser.create_adjacency_matrix(parser.get_unique_location_strings())
    for row in matrix:
        print(row)
    """

    def __init__(self, file_path):
        """
        Initialize the CSV parser with the path to the CSV file containing distance data.

        Parameters:
        - file_path (str): The path to the CSV file containing distance data.

        Raises:
        - Exception: If the file at the given path does not exist.
        """
        # Try to open the file to check if it exists
        try:
            file = open(file_path, 'r')
            file.close()
        except FileNotFoundError:
            raise Exception(f"The file at path {file_path} does not exist.")

        self.file_path = file_path

    def get_unique_location_strings(self):
        """
        Extracts unique location strings from the CSV file.

        Returns:
        - list: A list of unique location strings found in the CSV file.
        """
        location_strings = []

        with open(self.file_path, 'r') as file:
            current_str = ""
            inside_quotes = False

            # read the file character by character
            while (char := file.read(1)):

                # numbers inside quotes are part of an address. Numbers outside of quotes are a distance
                if char == '"':
                    inside_quotes = not inside_quotes
                # if the character is a comma, save the current string into the list of location strings
                if char == ',' and not inside_quotes:
                    if self.is_number(current_str) == False:
                        # only store if it's an address (distances in another structure later)
                        location_strings.append(current_str)
                    current_str = ""
                else:
                    current_str += char
            if current_str:
                # save the last string if it's not empty
                location_strings.append(current_str)

            location_strings.remove("DISTANCE BETWEEN HUBS IN MILES")
            location_strings.remove("")
            location_strings.remove("HUB")
            return location_strings

    def create_adjacency_matrix(self, locations):
        """
        Creates an adjacency matrix from the CSV file using the provided locations.

        Parameters:
        - locations (list): A list of locations.

        Returns:
        - list of lists: An adjacency matrix representing distances between locations.
        """
        current_str = ""
        current_row = []  # we will construct a 2D matrix row by row
        list_of_rows = []  # and add to this list of rows (ultimately forming columns in a 2D matrix)
        num_locations = len(locations)

        with open(self.file_path, 'r') as file:
            while (char := file.read(1)):
                if char == ',':
                    try:
                        distance = float(current_str)
                    except ValueError:
                        raise ValueError(f"The given string '{current_str}' cannot be converted to a float")

                    current_row.append(distance)
                    current_str = ""

                    if len(current_row) == num_locations:
                        list_of_rows.append(current_row)
                        current_row = []
                else:
                    current_str += char

        return list_of_rows
