class CSVParser_Locations:
    """
    # Example usage:

    """
    def __init__(self, file_path):
        # Try to open the file to check if it exists
        try:
            file = open(file_path, 'r')
            file.close()
        except FileNotFoundError:
            raise Exception(f"The file at path {file_path} does not exist.")

        self.file_path = file_path

    def get_unique_location_strings(self):
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
