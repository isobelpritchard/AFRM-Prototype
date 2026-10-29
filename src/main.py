from validation import FIELDS, validate_inputs
import ui


def main() -> None:
    raw = {}
    fields_to_ask = list(FIELDS)

    while True:
        for field in fields_to_ask:
            raw[field] = ui.ask(field)

        inputs, errors = validate_inputs(raw)
        if not errors:
            break

        ui.show_errors(errors)
        fields_to_ask = list(errors)   # re-ask only the invalid fields

    ui.show_results(inputs)


if __name__ == "__main__":
    main()