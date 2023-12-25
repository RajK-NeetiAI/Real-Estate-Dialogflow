from utils import *
from database import *


def handle_user_provides_property_type(body: dict) -> dict:
    '''Get request parameters and session
    '''
    parameters = get_dialogflow_parameters(body, 'session-vars')
    session = body['session']

    '''No parameters found
    '''
    if len(parameters) == 0:
        return get_error_message()

    '''Format the property_name from the parameters
    '''
    property_name = parameters['property_name']
    number = int(parameters['number'])
    property_type = ''
    if number == 0:
        property_type += property_name
    else:
        property_type += f'{number}{property_name}'
    properties = get_property_from_type(property_type)

    '''If there is no properties
    '''
    if len(properties) == 0:
        # Get distinct properties and show suggestion
        distinct_property_types = get_distinct_property_types()
        suggestion_chip = create_suggection_chip(distinct_property_types)
        rich_contents = []
        rich_contents.append(suggestion_chip)
        return format_dialogflow_response(
            [
                f"We are sorry, we don't have {property_type} at this moment. However, \
we have the following types of properties."
            ],
            rich_contents
        )

    '''If properties found then show the property names for more info
    '''
    scheme_names = []
    for prop in properties:
        name = prop['name']
        if (len(name) > 20):
            name = name[:17]
            name += '...'
        scheme_names.append(name)
    suggestion_chip = create_suggection_chip(scheme_names)
    rich_contents = []
    rich_contents.append(suggestion_chip)
    output_contexts = []
    output_contexts.append(
        {
            'name': f'{session}/contexts/session-vars',
            'lifespanCount': 50,
            'parameters': {
                'properties': properties
            }
        }
    )
    output_contexts.append(
        {
            'name': f'{session}/contexts/await-property-name',
            'lifespanCount': 1
        }
    )
    return format_dialogflow_response(
        [
            'Here you go...',
            f'We have the following properties available that has {property_type}.',
            'Click on any one of them to get more information.'
        ],
        rich_contents,
        output_contexts
    )


def handle_user_provides_property_name(body: dict) -> dict:
    '''Get request parameters and session
    '''
    parameters = get_dialogflow_parameters(body, 'session-vars')
    session = body['session']

    '''No parameters found
    '''
    if len(parameters) == 0:
        return get_error_message()

    '''Get the properties and generate response
    '''
    selected_property = parameters['selected_property']
    properties = parameters['properties']
    found_property = []
    for prop in properties:
        if selected_property.lower() == prop['name'].lower():
            found_property.append(prop)
            break
    messages = []
    rich_contents = []
    output_contexts = []
    if len(found_property) == 0:
        messages.append(
            f"Sorry, we don't have a scheme with {selected_property} name.")
        messages.append('However, here are a few options.')
        scheme_names = []
        for prop in properties:
            name = prop['name']
            if (len(name) > 20):
                name = name[:17]
                name += '...'
            scheme_names.append(name)
        suggestion_chip = create_suggection_chip(scheme_names)
        rich_contents.append(suggestion_chip)
        output_contexts.append(
            {
                'name': f'{session}/contexts/await-property-name',
                'lifespanCount': 1
            }
        )
        return format_dialogflow_response(
            messages,
            rich_contents,
            output_contexts
        )

    messages.append(f"{found_property[0]['name']} is located in \
{found_property[0]['area']}, {found_property[0]['area']} near to {found_property[0]['nearby_area']}.")
    messages.append(
        f"It is {found_property[0]['possession']} and {found_property[0]['furnishing']}.")
    messages.append(f"{found_property[0]['name']} has {found_property[0]['total_towers']} tower/s, \
each tower has {found_property[0]['total_floors']} floors and {found_property[0]['lifts']} lifts, \
and total {found_property[0]['total_units']} units.")
    suggestion_chip = create_suggection_chip(
        ['Amenities', 'Price', 'Website', 'Images'])
    rich_contents.append(suggestion_chip)
    output_contexts.append(
        {
            'name': f'{session}/contexts/await-facility-type',
            'lifespanCount': 1
        }
    )
    return format_dialogflow_response(
        messages,
        rich_contents,
        output_contexts
    )


def handle_user_asks_for_facilities(body: dict) -> dict:
    '''Get request parameters and session
    '''
    parameters = get_dialogflow_parameters(body, 'session-vars')
    session = body['session']

    '''No parameters found
    '''
    if len(parameters) == 0:
        return get_error_message()

    '''Get the properties and generate response
    '''
    selected_property = parameters['selected_property']
    properties = parameters['properties']
    found_property = []
    for prop in properties:
        if selected_property.lower() == prop['name'].lower():
            found_property.append(prop)
            break
    if len(found_property) == 0:
        return get_error_message()

    facility_type = parameters['facility_type']

    messages = []
    rich_contents = []
    output_contexts = []

    suggestion_chip = create_suggection_chip(
        ['Amenities', 'Price', 'Website', 'Images', 'Get a callback', 'Find a Property'])

    facilities = ['amenities', 'website',
                  'price', 'contact', 'brochure', 'media']

    if facility_type in facilities:
        if facility_type == 'amenities':
            messages.append(
                f"Here is the information on Amenities of {found_property[0]['name']}."),
            messages.append(found_property[0]['amenities'])
        elif facility_type == 'website':
            messages.append(
                f"Here is the website of {found_property[0]['name']}.")
            button = [create_button(
                'public',
                'Website',
                found_property[0]['website']
            )]
            rich_contents.append(button)
        elif facility_type == 'price':
            messages.append(f"The price of the {found_property[0]['name']} property ranges from \
{found_property[0]['min_price']} INR to {found_property[0]['max_price']} INR.")
        elif facility_type == 'contact':
            messages.append(f"Here is the contact number of {found_property[0]['name']}. \
Call on - {found_property[0]['conatact_number']}.")
        elif facility_type == 'brochure':
            messages.append(
                f"Here is the brochure for {found_property[0]['name']}.")
            messages.append(f"{found_property[0]['broucher']}")
        elif facility_type == 'media':
            media = get_media_from_project_id(int(found_property[0]['id']))
            if len(media) == 0:
                messages.append(
                    f"Sorry, we don't have any media for {found_property[0]['name']}.")
            else:
                messages.append(
                    f"Here are the different media information for {found_property[0]['name']}.")
                for m in media:
                    messages.append(f"Type - {m['type']}, URL - {m['path']}.")
        rich_contents.append(suggestion_chip)
        output_contexts.append(
            {
                'name': f'{session}/contexts/await-facility-type',
                'lifespanCount': 1
            }
        )
        return format_dialogflow_response(
            messages,
            rich_contents,
            output_contexts
        )
    else:
        messages.append(f"Sorry, we don't have any information about {facility_type.capitalize()} \
in the {found_property[0]['name']}")
        rich_contents.append(suggestion_chip)
        return format_dialogflow_response(
            messages,
            rich_contents,
            output_contexts
        )


def handle_user_searches_by_location(body: dict) -> dict:

    custom_location = body['queryResult']['parameters']['custom_location']
    session = body['session']

    properties = get_property_from_location(custom_location)

    messages = []
    rich_contents = []
    output_contexts = []

    if custom_location == 'NO_LOCATION':
        # Get distinct properties and show suggestion
        distinct_property_locations = get_distinct_property_locations()
        suggestion_chip = create_suggection_chip(distinct_property_locations)
        messages.append(f"We have properties near the following area.")
        messages.append(f"Select one of the areas to learn more.")
        rich_contents.append(suggestion_chip)
        return format_dialogflow_response(
            messages,
            rich_contents,
            output_contexts
        )

    '''If there is no properties
    '''
    if len(properties) == 0:
        # Get distinct properties and show suggestion
        distinct_property_locations = get_distinct_property_locations()
        suggestion_chip = create_suggection_chip(distinct_property_locations)
        messages.append(f"We are sorry, we don't have any property near {custom_location.capitalize()} \
at this moment. However, we have properties near these area.")
        rich_contents.append(suggestion_chip)
        return format_dialogflow_response(
            messages,
            rich_contents,
            output_contexts
        )

    '''If properties found then show the property names for more info
    '''
    scheme_names = []
    for prop in properties:
        name = prop['name']
        if (len(name) > 20):
            name = name[:17]
            name += '...'
        scheme_names.append(name)
    suggestion_chip = create_suggection_chip(scheme_names)
    messages.append('Here you go...')
    messages.append(
        f'We have the following properties available near the area of {custom_location}.')
    messages.append('Click on any one of them to get more information.')
    rich_contents.append(suggestion_chip)
    output_contexts.append(
        {
            'name': f'{session}/contexts/session-vars',
            'lifespanCount': 50,
            'parameters': {
                'properties': properties
            }
        }
    )
    output_contexts.append(
        {
            'name': f'{session}/contexts/await-property-name',
            'lifespanCount': 1
        }
    )

    return format_dialogflow_response(
        messages,
        rich_contents,
        output_contexts
    )
