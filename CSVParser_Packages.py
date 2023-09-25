class CSVParser_Packages:
    """
    # Usage
    parser = CSVParser_Packages("packages.csv")
    package_tuples = parser.parse()
    for package in package_tuples:
        print(package)

    """
    def __init__(self, file_path):
        # Try to open the file to check if it exists
        try:
            file = open(file_path, 'r')
            file.close()
        except FileNotFoundError:
            raise Exception(f"The file at path {file_path} does not exist.")

        self.file_path = file_path

    def parse(self):
        with open(self.file_path, 'r') as file:
            lines = file.readlines()
            tuples_list = []

            for line in lines:
                # Splitting by comma and stripping whitespace and newline characters
                values = [value.strip() for value in line.split(',')]

                # Handling quotes for fields that contain commas
                corrected_values = []
                temp = []
                inside_quotes = False
                for value in values:
                    if '"' in value:
                        if inside_quotes:
                            temp.append(value.replace('"', ''))
                            corrected_values.append(','.join(temp))
                            temp = []
                            inside_quotes = False
                        else:
                            temp.append(value.replace('"', ''))
                            inside_quotes = True
                    else:
                        if inside_quotes:
                            temp.append(value)
                        else:
                            corrected_values.append(value)

                tuples_list.append(tuple(corrected_values))

        return tuples_list


