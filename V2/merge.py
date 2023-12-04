"""
Merge the file name from pan_url.json to Thread.json
"""
import json

from colorama import Fore


class stored_data:
    def __init__(self, json_file):
        self.json_file = json_file

    def write(self, data):
        """
        This function write data into json file
        :param data: dictionary or list of dictionary
        :return: None
        """
        with open(self.json_file, 'w') as f:
            json.dump(data, f)

    def read(self):
        """
        This function get the data from JSON file
        :return: dictionary or list of dictionary
        """
        with open(self.json_file, 'r') as f:
            data = json.load(f)
        return data


file_name_file = stored_data("Saved_data/pan_url.json")
file_name_dict = file_name_file.read()
# {"link" : "name"}

stored_file = stored_data("Thread.json")
stored_data_list = stored_file.read()
# [{title:'xxx}]

for i in file_name_dict.keys():
    for j in range(len(stored_data_list)):
        if stored_data_list[j]['file_name'] is not None:
            break
        elif stored_data_list[j]['pan_link'] == i:
            stored_data_list[j]['file_name'] = file_name_dict[i]
            print(Fore.GREEN + "Link", Fore.BLUE + stored_data_list[j]['title'], Fore.YELLOW + "<---->",
                  Fore.CYAN + file_name_dict[i] + Fore.RESET)
        else:
            print(Fore.RED + stored_data_list[j]['title'], Fore.MAGENTA + "already link with",
                  Fore.RED + file_name_dict[i] + Fore.RESET)

stored_file.write(stored_data_list)
print(Fore.GREEN + "Complete!" + Fore.RESET)
