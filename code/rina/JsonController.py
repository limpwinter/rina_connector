import ast


class JsonController:
    def dict_to_str(self, dictionary):
        return str(dictionary)

    def str_to_dct(self, string):
        return ast.literal_eval(string)
