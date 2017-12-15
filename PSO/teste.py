import os, sys

class FileManager:
    files = []
    to_create = []
    ignore_extensions = ['.mp4', '.MOV']
    ignore_folders = ['pasta', 'ignorar', 'Pré-Produção', 'Shared Life Live']
    new_folder_name = "pasta"

    exception_bits = 1000

    file_index = 0
    found_file = False

    def __init__(self, f1, f2):
        self.actual_directory = os.path.abspath('.')
        self.f1_directory = os.path.join(self.actual_directory, sys.argv[1])
        self.f2_directory = os.path.join(self.actual_directory, sys.argv[2])
        self.defineFiles(f1, self.f1_directory)
        self.findFiles(f2)

        self.createFiles()

    def findFiles(self, f2):
        for i in self.files:
            self.walkDir(i, f2, self.f2_directory)
            if not self.found_file:
                print("vai adicionar arquivo " + i[0])
                self.to_create.append(i)


    def defineFiles(self, dir_name, full_path):
        for filename in os.listdir(full_path):
            #print(filename)
            abs_path = os.path.join(full_path, filename)

            if (os.path.isdir(abs_path)):
                new_dir = os.path.join(dir_name, filename)
                self.defineFiles(new_dir, abs_path)
            else:
                file = open(abs_path, "rb")
                extension = os.path.splitext(filename)[1]
                if not any(extension in s for s in self.ignore_extensions):
                    info = [filename, file.read()]
                    self.files.append(info)


    def walkDir(self, file, dir_name, full_path):
        for filename in os.listdir(full_path):
            if self.found_file:
                return

            abs_path = os.path.join(full_path, filename)

            if (os.path.isdir(abs_path)):
                if (any(filename in s for s in self.ignore_folders)):
                    print ("ignorou pasta " + filename)
                    break
                else:
                    new_dir = os.path.join(dir_name, filename)
                    self.walkDir(file, new_dir, abs_path)
            else:
                self.found_file = self.checkFile(filename, abs_path, file)
                break

    def createFiles(self):

        new_folder_location = os.path.join(self.f2_directory, self.new_folder_name)
        print(new_folder_location)

        if not os.path.exists(new_folder_location):
            os.makedirs(new_folder_location, exist_ok=True)

        for f in self.to_create:
            file_location = os.path.join(new_folder_location, f[0])
            file = open(file_location, "wb")
            print("vai escrever arquivo " + f[0])
            file.write(bytearray(f[1]))



    def checkFile(self, filename, abs_path, file_to_check):
        file = open(abs_path, "rb")
        extension = os.path.splitext(filename)[1]

        if any(extension in s for s in self.ignore_extensions):
            return

        file_data = file.read()

        if file_to_check[1] == file_data:
            return True
        return False


def main():
    folder1 = "."
    folder2 = "."
    f = FileManager(folder1, folder2)






main()
