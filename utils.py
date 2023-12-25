import config


def format_dialogflow_response(messages: list[str], rich_contents: list = [], output_contexts: list[dict] = []) -> dict:
    response_data = {}
    response_data['fulfillmentMessages'] = []
    response_data['fulfillmentMessages'].append(
        {
            'text': {
                'text': messages
            }
        }
    )
    if (len(rich_contents) > 0):
        payload = {}
        payload['payload'] = {}
        payload['payload']['richContent'] = rich_contents
        response_data['fulfillmentMessages'].append(payload)
    if (len(output_contexts) > 0):
        response_data['outputContexts'] = output_contexts
    return response_data


def get_dialogflow_parameters(body: dict, context_name: str) -> dict:
    parameters = {}
    output_contexts = body['queryResult']['outputContexts']
    for oc in output_contexts:
        if context_name in oc['name']:
            parameters = oc['parameters']
    return parameters


def get_error_message():
    error_message = format_dialogflow_response([
        config.ERROR_MESSAGE
    ])
    return error_message


def create_suggection_chip(chips: list[str]) -> list[dict]:
    formated_chips = [{
        'type': 'chips'
    }]
    options = []
    for chip in chips:
        options.append({
            'text': chip
        })
    formated_chips[0]['options'] = options
    return formated_chips


def create_button(icon_name: str, text: str, link: str) -> dict:
    formated_button = {
        'type': 'button',
        'icon': {
            'type': icon_name,
            'color': config.ICON_COLOR
        },
        'text': text,
        'link': link
    }
    return formated_button
