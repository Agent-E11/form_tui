from form_tui import Field, run_form

class ContactForm:
    name: str
    email: str
    phone_number: int | None

    def fields(self) -> list[Field]:
        return [
            Field("name", "Name", str),
            Field("email", "Email", str, validator=lambda s: "@" in s),
            Field("phone_number", "phone_number", int | None),
        ]

if __name__ == "__main__":
    contact_form = ContactForm()

    # Populate the form's fields
    run_form(contact_form)
