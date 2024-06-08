from typing import Protocol, get_args
from types import NoneType, UnionType

class Field:
    """
    Represents a field in a form. Contains the id, name, and type
    of the field.
    """
    id: str
    name: str
    t: type | UnionType

    def __init__(self, id: str, name: str, t: type | UnionType):
        self.id = id
        self.name = name
        self.t = t

class Form(Protocol):
    """
    Protocol that all user defined forms must satisfy.
    """
    def fields(self) -> list[Field]:
        """
        Returns the id and type of the different fields of the form
        """
        ...

def run_form(form: Form) -> None:
    """
    Run tui for form to get input for fields.
    """
    for field in form.fields():
        # Get all possible types
        all_types: list[type] = []
        if isinstance(field.t, UnionType):
            all_types.extend(get_args(field.t))
        else:
            all_types.append(field.t)

        required = NoneType not in all_types

        # Set initial value, get input
        v = None
        ans = input(field.name + ("" if required else " (optional)") + ": ")
        if ans == "" and required:
            # If the answer wasn't provided and it is required, raise an exception
            raise Exception("required value was not supplied")
        elif ans != "":
            # Loop through the possible types
            for t in all_types:
                if t is NoneType: # If it is NoneType, ignore it
                    continue

                try: # Try to convert to the type
                    v = t(ans)
                    break # If successful, break out of the loop
                except ValueError:
                    continue # If unsuccessful, try next type

            if v == None: # If the value is still None, then the answer was not able to be converted
                raise Exception(f"value \"{ans}\" was not able to be converted to any of these types: {all_types}")

        setattr(form, field.id, v)


# -- Extra -- #  TODO: Delete this

class MyForm:
    first_name: str
    middle_name: str | None
    last_name: str
    favorite_value: int

    def fields(self) -> list[Field]:
        return [
            Field("first_name", "First Name", str),
            Field("middle_name", "Middle Name", str | None),
            Field("last_name", "Last Name", str),
            Field("favorite_value", "Favorite Value", int | str),
        ]

if __name__ == "__main__":
    f = MyForm()
    run_form(f)
    print()

    for var, val in vars(f).items():
        print(f"{var}: {type(val)} = {val}")
