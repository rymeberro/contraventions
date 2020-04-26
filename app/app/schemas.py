user_insert_schema = {
    'type': 'object',
    'required': ['fullname', 'email'],
    'properties': {
        'fullname': {
            'type': 'string'
        },
        'email': {
            'type': 'string'
        }
    },
    'additionalProperties': False
}

person_update_schema = {
    'type': 'object',
    'required': ['fullname', 'email', 'id'],
    'properties': {
        'id': {
            'type': 'number'
        },
        'fullname': {
            'type': 'string'
        },
        'email': {
            'type': 'string'
        }
    },
    'additionalProperties': False
}