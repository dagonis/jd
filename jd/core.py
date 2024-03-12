import os 

from dataclasses import dataclass
from itertools import chain
from pathlib import Path


@dataclass
class JohnDecimal:
    """
    This represents the whole of a Johnny Decimal library. 
    All you need to give it is a file system location and it will build the whole library.
    All the fun methods related to searching and adding Johnny Decimals are here.

    The implied format of a JD ID is AC.ID where AC is area/category and ID is the identifier.
    """
    file_system_location:str

    def __post_init__(self) -> None:
        self.areas = sorted([Area(_) for _ in Path(self.file_system_location).iterdir() if _.is_dir() and _.name[0] != "."], key=lambda _: _.area_name)
        self.categories = list(chain(*[area.categories for area in self.areas]))
        self.identifiers = list(chain(*[category.identifiers for category in self.categories]))
        self.files = list(chain(*[identifier.files for identifier in self.identifiers]))

    """ 
    These Methods are for searching and printing the Johnny Decimal library.
    Think of this as the "read" part of the CRUD operations.
    """

    def search_johnny_decimal(self, search_term:str, include_category=True, include_files=False) -> str:
        results = []
        normalized_search_term = search_term.lower()
        for category in self.categories:
            if normalized_search_term in category.category_name.lower():
                results.append(str(category))
            for identifier in category.identifiers:
                if normalized_search_term in identifier.full_name.lower():
                    if include_category:
                        results.append(f"{category} -> {identifier}")
                    else:
                        results.append(str(identifier))
                if include_files:
                    for jdfile in identifier.files:
                        if normalized_search_term in jdfile.file_system_location.name.lower():
                            results.append(str(jdfile))
        if len(results) == 0:
            return f"No results found for {search_term}"
        return "\n".join(results)
    
    def print_johnny_decimal_tree(self, space_len = 4, tabs = False, print_files = False) -> str:
        output = ""
        spaces = " " * space_len if not tabs else "\t"
        for area in self.areas:
            output += f"{area}\n"
            for category in area.categories:
                output += f"{spaces}{category}\n"
                for identifier in category.identifiers:
                    output += f"{spaces}{spaces}{identifier}\n"
                    if print_files:
                        for jdfile in identifier.files:
                            output += f"{spaces}{spaces}{spaces}{jdfile}\n"
                    else:
                        pass
        return output
    
    def get_johnny_decimal_category(self, category_id:str) -> str:
        output = ""
        for category in self.categories:
            if category.category_number == category_id:
                output += f"{str(category)}\n"
                for identifier in category.identifiers:
                    output += f"    {str(identifier)}\n"
                return output.rstrip()
        return f"No category found for {category_id}"

    def __str__(self) -> str:
        return str(self.identifiers)    

    """
    These methods are for adding Johnny Decimal items.
    Think of this as the "create" part of the CRUD operations.
    """

    def add_johnny_decimal_category(self, area_id:str, new_category_name:str, dry_run=False) -> bool:
        for area in self.areas:
            if area.area_number_range.startswith(area_id):
                for i in range(int(area_id), int(area_id) + 10):
                    if not any(category.category_number == str(i).zfill(2) for category in area.categories):
                        _new_category = f"{i} {new_category_name}"
                        new_category_path = Path(area.file_system_location) / _new_category
                        if not dry_run:
                            os.mkdir(Path(new_category_path))
                            print(f"Created - {new_category_path}")
                            return True
                        print(f"Would have created - {new_category_path}")
                        return False
                    
    def add_johnny_decimal_identifier(self, category_id:str, identifier_name:str, placeholder:bool=False, dry_run:bool=False) -> bool:
        for category in self.categories:
            if category.category_number == category_id:
                for i in range(1, 100):
                    if not any(identifier.id_number == str(i).zfill(2) for identifier in category.identifiers):
                        new_identifier = f"{str(i).zfill(2)} {identifier_name}"
                        new_identifier_path = Path(category.file_system_location) / new_identifier
                        if not dry_run:
                            os.mkdir(Path(new_identifier_path))
                            if placeholder:
                                Path(new_identifier_path / f"{identifier_name}.md").touch()
                            print(f"Created - {new_identifier_path}")
                            return True
                        print(f"Would have created - {new_identifier_path}")
                        return False


@dataclass
class Area:
    """
    This represents a Johnny Decimal area.
    This is usually created by the JohnDecimal class.
    This is in the format of: 00-09 Admin or 80-89 Unused
    It is somewhat unlikely you will ever deal with this yourself, you are probably more interested in
    categories and identifiers.
    """
    file_system_location:str

    def __post_init__(self) -> None:
        self.area_name = self.file_system_location.parts[-1]
        self.area_number_range, self.area_short_name = self.area_name.split(" ", maxsplit=1)
        self.categories = sorted([Category(_, self.area_name) for _ in Path(self.file_system_location).iterdir() if _.is_dir() and _.name[0] != "."], key=lambda _: _.category_name)

    def __str__(self) -> str:
        return f"[{self.area_number_range}] {self.area_short_name}"

@dataclass
class Category:
    """
    This represents a Johnny Decimal category.
    This is usually created by the Area class.
    This will be the most common class you will deal with.
    The format is Category and will look like ##
    In a whole ID, it would be like Category.Identifier e.g. 11.01
    """
    file_system_location:str
    area:str

    def __post_init__(self):
        self.category_name = self.file_system_location.parts[-1]    
        self.category_number, self.category_short_name = self.category_name.split(" ", maxsplit=1)
        self.identifiers = sorted([Identifier(_, self.area, self.category_number) for _ in Path(self.file_system_location).iterdir() if _.is_dir() and _.name[0] != "."], key=lambda _: _.full_name)

    def __str__(self) -> str:
        return f"[{self.category_number}] {self.category_short_name}"

@dataclass
class Identifier:
    """
    This represents a Johnny Decimal identifier.
    This is usually created by the Category class.
    This is the most part of the JD structure and contains files.
    The format is Identifier and will look like ##
    In a whole ID, it would be like Category.Identifier e.g. 11.01
    """
    file_system_location:str
    area:str
    category:str

    def __post_init__(self) -> None:
        self.full_name = self.file_system_location.parts[-1]
        self.id_number, self.short_name = self.full_name.split(" ", maxsplit=1)
        self.files = [JohnnyDecimalFile(_, self.area, self.category, self.id_number) for _ in Path(self.file_system_location).iterdir() if _.is_file() and _.name[0] != "."]
    
    def __str__(self) -> str:
        return f"[{self.category}.{self.id_number}] {self.short_name}"
    
@dataclass
class JohnnyDecimalFile:
    """
    This represents a file in a Johnny Decimal identifier.
    This is usually created by the Identifier class.
    """
    file_system_location:str
    area:str
    category:str
    identifier:str

    def __post_init__(self) -> None:
        self.file_name = self.file_system_location.parts[-1]

    def __str__(self) -> str:
        return f"[{self.category}.{self.identifier}] {self.file_name}"
    