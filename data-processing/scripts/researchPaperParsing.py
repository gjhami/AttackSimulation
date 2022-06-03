from pathlib import Path
import json

# Small business is any business with 1000 or fewer employees

def descending_dict(d):
    sorted_tuple_list = sorted(d.items(), key=lambda item: item[1])
    sorted_tuple_list.reverse()
    return dict(sorted_tuple_list)


def get_top_actors(actor_counts, num):
    sorted_tuple_list = sorted(actor_counts.items(), key=lambda item: item[1])
    sorted_tuple_list.reverse()
    num = len(sorted_tuple_list) if len(sorted_tuple_list) < num else num
    top_10 = []
    for i in range(num):
        top_10.append(sorted_tuple_list[i])
    return dict(top_10)


def get_actor_varieties(actor_categories):
    actor_varieties = []
    for actor_category in actor_categories:
        if 'variety' in actor_category:
            actors = actor_category['variety']
            for actor in actors:
                actor_varieties.append(actor)
    return actor_varieties


def get_actor_incident_details(incident, target_actor):
    actor_varieties = []
    actor_categories = incident['actor'].values()
    for actor_category in actor_categories:
        if 'variety' in actor_category:
            actors = actor_category['variety']
            for actor in actors:
                actor_varieties.append(actor)

    if target_actor in actor_varieties:
        print(f'{incident["summary"]}\n')


def get_is_breach(attributes):
    is_breach = False
    is_uncertain = False
    for attribute in attributes:
        if 'data_disclosure' in attribute:
            data_disclosure = attribute['data_disclosure']

            if data_disclosure == 'Yes':
                is_breach = True
            elif data_disclosure in ['Potentially', 'Unknown']:
                is_uncertain = True

    # Return none if there is no definite breach, but it's not all 'No's
    if (not is_breach) and is_uncertain:
        is_breach = None

    return is_breach


# sb is a boolean indicating if the incident pertains to a small business.
def increment_actor_variety(is_breach, actor_varieties, sb):
    if is_breach:
        if sb is True:
            for actor_variety in actor_varieties:
                if actor_variety in sb_breach_actor_counts:
                    sb_breach_actor_counts[actor_variety] = sb_breach_actor_counts[actor_variety] + 1
                else:
                    sb_breach_actor_counts[actor_variety] = 1

                if actor_variety in sb_actor_counts:
                    sb_actor_counts[actor_variety] = sb_actor_counts[actor_variety] + 1
                else:
                    sb_actor_counts[actor_variety] = 1
        else:
            for actor_variety in actor_varieties:
                if actor_variety in all_breach_actor_counts:
                    all_breach_actor_counts[actor_variety] = all_breach_actor_counts[actor_variety] + 1
                else:
                    all_breach_actor_counts[actor_variety] = 1

                if actor_variety in all_actor_counts:
                    all_actor_counts[actor_variety] = all_actor_counts[actor_variety] + 1
                else:
                    all_actor_counts[actor_variety] = 1

    elif is_breach is not None:
        if sb is True:
            for actor_variety in actor_varieties:
                if actor_variety in sb_non_breach_actor_counts:
                    sb_non_breach_actor_counts[actor_variety] = sb_non_breach_actor_counts[actor_variety] + 1
                else:
                    sb_non_breach_actor_counts[actor_variety] = 1

                if actor_variety in sb_actor_counts:
                    sb_actor_counts[actor_variety] = sb_actor_counts[actor_variety] + 1
                else:
                    sb_actor_counts[actor_variety] = 1
        else:
            for actor_variety in actor_varieties:
                if actor_variety in all_non_breach_actor_counts:
                    all_non_breach_actor_counts[actor_variety] = all_non_breach_actor_counts[actor_variety] + 1
                else:
                    all_non_breach_actor_counts[actor_variety] = 1

                if actor_variety in all_actor_counts:
                    all_actor_counts[actor_variety] = all_actor_counts[actor_variety] + 1
                else:
                    all_actor_counts[actor_variety] = 1


def print_sb_stats():
    print(f'### Small Business Stats ###')
    print(f'Total Incidents: {sb_incident_count}')
    print(f'\tTotal Breaches: {sb_breach_count}')
    print(f'\tTotal Non-Breaches: {sb_non_breach_count}')
    print(f'\tTotal Maybe-Breaches: {sb_maybe_breach_count}\n')

    print(f'Total: {get_top_actors(sb_actor_counts, 20)}')
    print(f'Breaches: {get_top_actors(sb_breach_actor_counts, 20)}')
    print(f'Non-Breaches: {get_top_actors(sb_non_breach_actor_counts, 20)}\n\n')


def print_unfiltered_stats():
    print(f'### Unfiltered Stats ###')
    print(f'Total Incidents: {all_incident_count}')
    print(f'\tTotal Breaches: {all_breach_count}')
    print(f'\tTotal Non-Breaches: {all_non_breach_count}')
    print(f'\tTotal Maybe-Breaches: {all_maybe_breach_count}\n')

    print(f'Total: {get_top_actors(all_actor_counts, 20)}')
    print(f'Breaches: {get_top_actors(all_breach_actor_counts, 20)}')
    print(f'Non-Breaches: {get_top_actors(all_non_breach_actor_counts, 20)}\n\n')


def print_all_stats():
    print_unfiltered_stats()
    print_sb_stats()


# Get validated .json files of each incident
data_folder = Path('data/json/validated/')
file_paths = list(data_folder.glob('*.json'))

# Filters
# target_employee_counts = ['1 to 10', '11 to 100', '101 to 1000', '1001 to 10000', '10001 to 25000', '25001 to 50000',
#                           '50001 to 100000', 'Over 100000',
#                           'Small', 'Large', 'Unknown']
target_employee_counts = ['1 to 10', '11 to 100', '101 to 1000', 'Small']

# All disclosure values: ['Yes', 'No', 'Potentially', 'Unknown']


# Track metrics for all incidents
all_incident_count          = 0
all_breach_count            = 0
all_non_breach_count        = 0
all_maybe_breach_count      = 0
all_actor_counts            = {}
all_breach_actor_counts     = {}
all_non_breach_actor_counts = {}


# Track actor metrics for small business incidents
sb_incident_count           = 0
sb_breach_count             = 0
sb_non_breach_count         = 0
sb_maybe_breach_count       = 0
sb_actor_counts             = {}
sb_breach_actor_counts      = {}
sb_non_breach_actor_counts  = {}


for file_path in file_paths:
    with file_path.open() as f:
        incident = json.load(f)

        employee_count = incident['victim']['employee_count']
        actor_varieties = get_actor_varieties(incident['actor'].values())
        is_breach = get_is_breach(incident['attribute'].values())

        if employee_count in target_employee_counts:
            sb_incident_count = sb_incident_count + 1

            if is_breach is None:
                sb_breach_count = sb_breach_count + 1
            elif is_breach is True:
                sb_breach_count = sb_breach_count + 1
            elif is_breach is False:
                sb_non_breach_count = sb_non_breach_count + 1

            increment_actor_variety(is_breach, actor_varieties, True)

        else:
            all_incident_count = all_incident_count + 1

            if is_breach is None:
                all_maybe_breach_count = all_maybe_breach_count + 1
            elif is_breach is True:
                all_breach_count = all_breach_count + 1
            elif is_breach is False:
                all_non_breach_count = all_non_breach_count + 1

            increment_actor_variety(is_breach, actor_varieties, False)

print_all_stats()


