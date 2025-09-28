BASE_WIDGET_ATTRS = {
    "class": "form-control input-register",
    "autocomplete": "off"
}

ERROR_MESSAGES = {
    "email": {
        "required": "Email is required",
        "min_length": "Email must be at least 5 characters",
        "max_length": "Email cannot exceed 66 characters",
    },

    "first_name": {
        "required": "First name is required",
        "min_length": "First name must be at least 2 characters long",
        "max_length": "First name cannot exceed 50 characters",
    },

    "last_name": {
        "required": "Last name is required",
        "min_length": "Last name must be at least 2 characters long",
        "max_length": "Last name cannot exceed 50 characters",
    },

    "username": {
        "required": "Username is required",
        "min_length": "Username must be at least 2 characters long",
        "max_length": "Username cannot exceed 50 characters",
    },

    "password": {
        "required": "Password is required",
        "min_length": "Password must be at least 8 characters long",
        "max_length": "Password cannot exceed 66 characters",
    }
}
