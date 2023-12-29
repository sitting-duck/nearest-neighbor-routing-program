class CSVParser_Locations:
    """
    A class for parsing location data from a CSV file.

    This class is designed to extract unique location strings from a given CSV file.
    It is useful in scenarios where location data needs to be extracted and processed.

    Example usage:
        file_path = "path_to_your_locations_csv_file.csv"
        parser = CSVParser_Locations(file_path)
        location_strings = parser.get_unique_location_strings()
        for location in location_strings:
            print(location)
    """
    def __init__(self, file_path):
        """
        Initialize the CSV parser with the path to the CSV file containing location data.

        Parameters:
        - file_path (str): The path to the CSV file containing location data.

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
                    current_str = current_str.replace('"', '')
                    location_strings.append(current_str.replace('\n', ''))
                    current_str = ""
                else:
                    current_str += char
            return location_strings
