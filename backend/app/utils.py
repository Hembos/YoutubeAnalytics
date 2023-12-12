def remove_empty_values(data, keep_keys):
    cleaned_data = {}
    for key, value in data.items():
        if isinstance(value, dict):
            cleaned_value = remove_empty_values(value, keep_keys)
            if cleaned_value:
                cleaned_data[key] = cleaned_value
        elif value is not None and value != "" or key in keep_keys:
            cleaned_data[key] = value
    return cleaned_data