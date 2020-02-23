import os
import PySimpleGUI as sg 
import re

sg.ChangeLookAndFeel('Dark')

class Gui:
    def __init__(self):
        self.layout = [[sg.Text('Expression'), sg.Input()],
                        [sg.Text('Root Path'), sg.Input(), sg.FolderBrowse('Browse'), sg.Button('Search', bind_return_key=True)],
                        [sg.Output(size=(100, 20))]
        ]
        self.window = sg.Window('In File Search Engine').Layout(self.layout)


def negate(var):
    if var == 1:
        return 0
    else:
        return 1


def evaluate(string, lst):
    replace = ""
    cnt = 0
    ok = 1
    c = "~()|&!"
    for it in string:
        if it in c:
            replace = replace + it
            ok = 1
        elif ok == 1:
            replace = replace + lst[cnt]
            cnt += 1
            ok = 0
    replace = replace.replace("!", "negate")
    if replace != "":
        ans = eval(replace)
    else:
        print("Introduce an expression first")
        ans = 0
    return ans


class SearchEngine:
    def __init__(self):
        self.files = []
        self.results = []
        self.index = {}

    def get_files(self, path):
        self.files.clear()
        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                where = os.path.join(path, name)
                self.files.append(where)


    def search(self, string):
        copy  = string
        string = string.replace("||", "|")
        string = string.replace("&&", "&")
        string = string.replace(" ", "")
        chars = "&|!()"
        for it in chars:
            copy = copy.replace(it, " ")
        words = copy.split()
        self.results.clear()
        for it in range(len(self.files)):
            lst = ""
            for word in words:
                if word.lower() not in self.index.keys():
                    lst += "0"
                elif self.index[word.lower()][it] == '1':
                    lst += "1"
                else:
                    lst += "0"
            
            value = evaluate(string, lst)
            if value != 0:
                result = self.files[it].replace("\\","/")
                self.results.append(os.path.splitext(result)[0])

    def indexate(self):
        self.index.clear()
        zero = []
        count = 0
        zero = ['0'] * len(self.files)
        for file in self.files:
            with open(file, "r") as f:
                words = re.findall(r"([a-zA-Z\-0-9]+)", f.read())
                for word in words:
                    if word.lower() in self.index.keys():
                        self.index[word.lower()][count] = '1'
                    else:
                        self.index[word.lower()] = []
                        self.index[word.lower()].extend(zero)
                        self.index[word.lower()][count] = '1'
            count += 1

def main():

    g = Gui()
    path = ""
    sch = SearchEngine()
    while True:
        event, values = g.window.Read()
        sch.get_files(values[1])
        if len(sch.files) > 500:
            print("Way too many files")
            continue
        if path != values[1]:
            sch.indexate()
        path = values[1]
        string = values[0]
        sch.search(string)
        print("Search Complete")
        print(f'We have found: {len(sch.results)} results')
        if len(sch.results) > 0:
            print("The files that satisfy the expression are:")
            for it in sch.results:
                print(it)
        print()


if __name__ == '__main__':
    main()










