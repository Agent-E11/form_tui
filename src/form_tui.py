from typing import Protocol, Callable, get_args
from types import NoneType, UnionType

class Field:
    """
    Represents a field in a form. Contains the id,
    name, and type of the field.

    Here is an example contact form:

    ```
    class ContactForm:
        name: str
        phone_number: int
    ```

    The corresponding `Field`s for this form would
    probably be something like this:

    ```
    Field("name", "Name", str)
    Field("phone_number", "Phone Number", int)
    #     ^^^^^^^^^^^^^^  ^^^^^^^^^^^^^^  ^^^
    #     |               |               + Type
    #     |               + Vanity name
    #     + Attribute name
    ```
    """
    id: str
    """
    Name of the field on the form class. This must
    exactly match the corresponding attribute's name.
    """
    name: str
    """
    Nice name of the field. This name is what will be
    displayed to the user.
    """
    t: type | UnionType
    """
    Type(s) of the field value.
    """
    validator: Callable[[str], bool] | None
    """
    Function to validate a string input.
    E.g. a rudimentary email validator could be something
    like `lambda s: s.contains("@")`
    """

    def __init__(self, id: str, name: str, t: type | UnionType, validator: Callable[[str], bool] | None = None):
        self.id = id
        self.name = name
        self.t = t
        self.validator = validator

    def validate(self, s: str) -> bool:
        """
        Validate the given string using this field's validator.
        If the validator is `None`, then it will simply return True.
        """
        return self.validator is None or self.validator(s)

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
            # Validate the input
            if not field.validate(ans):
                raise Exception(f"custom validator failed")

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
    middle_initial: str | None
    last_name: str
    favorite_value: int

    def fields(self) -> list[Field]:
        return [
            Field("first_name", "First Name", str),
            Field("middle_initial", "Middle Initial", str | None, lambda ans: ans is None or len(ans) == 1),
            Field("last_name", "Last Name", str),
            Field("favorite_value", "Favorite Value", int | str),
        ]

if __name__ == "__main__":
    f = MyForm()
    run_form(f)
    print()

    for field in f.fields():
        print(f"id: {field.id}, name: {field.name}, type: {field.t}, validator: {field.validator}")

    for var, val in vars(f).items():
        print(f"{var}: {type(val)} = {val}")
