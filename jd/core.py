import os 

from dataclasses import dataclass
from itertools import chain
from pathlib import Path


@dataclass
class JohnDecimal:
    file_system_location:str

    def __post_init__(self):
        self.areas = sorted([Area(_) for _ in Path(self.file_system_location).iterdir() if _.is_dir() and _.name[0] != "."], key=lambda _: _.name)
        # self.areas = list(chain(*[_.areas for _ in self.area_groups]))
        # self.categories = list(chain(*[_.categories for _ in self.areas]))

    def search_johnny_decimal_category(self, search_term:str) -> str:
        results = []
        for area_group in self.area_groups:
            for area in area_group.areas:
                for category in area.categories:
                    if search_term in category.name:
                        print(f"Found {category.name} in {area.name}")
                        _result = f"{area.number}.{category.number} - {category.file_system_location}"
                        results.append(_result)
        output_string = ""
        for result in results:
            output_string = output_string + f"{result}\n"
        return output_string.rstrip()
    
    def search_johnny_decimal_identifier(self, search_term:str) -> str:
        results = []
        for area_group in self.area_groups:
            for area in area_group.areas:
                for category in area.categories:
                    for identifier in category.identifiers:
                        if search_term in identifier.name:
                            _result = f"{area.number}{category.number}{identifier.name} - {identifier.file_system_location}"
                            results.append([identifier])
        return results

    def add_johnny_decimal(self, jd:str) -> str:
        pass

    def __str__(self) -> str:
        output_string = ""
        for area in self.areas:
            output_string = output_string + f"{area_group.name}\n"
            for category in area_group.areas:
                output_string = output_string + f"    {area.name}\n"
                for category in area.categories:
                    output_string = output_string + f"        {category.name}\n"
                    for identifier in category.identifiers:
                        output_string = output_string + f"            {identifier.name}\n"
        return output_string

@dataclass
class Area:
    file_system_location:str

    def __post_init__(self):
        self.name = self.file_system_location.parts[-1]
        self.areas = sorted([Area(_) for _ in Path(self.file_system_location).iterdir() if _.is_dir() and _.name[0] != "."], key=lambda _: _.name)

# @dataclass
# class Category:
#     file_system_location:str

#     def __post_init__(self):
#         self.name = self.file_system_location.parts[-1]    
#         self.number = self.name.split(" ")[0]
#         self.categories = sorted([Category(_, self.number) for _ in Path(self.file_system_location).iterdir() if _.is_dir() and _.name[0] != "."], key=lambda _: _.name)


@dataclass
class Category:
    file_system_location:str
    area:str

    def __post_init__(self):
        self.name = self.file_system_location.parts[-1]
        self.number = self.name.split(" ")[0]
        self.identifiers = sorted([Identifier(_, self.number) for _ in Path(self.file_system_location).iterdir() if _.is_file() and _.name[0] != "."], key=lambda _: _.name)


@dataclass
class Identifier:
    file_system_location:str
    category:str

    def __post_init__(self):
        self.name = self.file_system_location.parts[-1]
        self.number = self.name.split(" ")[0]
        self.contents = self.list_files()

    def list_files(self):
        file_list = []
        for root, dirs, files in os.walk(self.file_system_location):
            for f in files:
                file_list.append(os.path.join(root, f))
        return file_list