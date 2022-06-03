from pathlib import Path
import csv
import json

# Small business (sb) is any business with 1000 or fewer employees


class Incident:
    # Track breach vs. non-breach incidents for each actor in all incidents
    all_actor_success = {}  # actor: {'success', 'fail', 'maybe', 'success-rate'}

    # Track all incidents for each actor if the victim is a small business
    sb_actor_prevalence = {}  # actor: {'count', 'prevalence-rate'}
    sb_incident_count = 0

    # target_employee_counts = ['1 to 10', '11 to 100', '101 to 1000', '1001 to 10000', '10001 to 25000',
    #                           '25001 to 50000', '50001 to 100000', 'Over 100000', 'Small', 'Large', 'Unknown']
    target_employee_counts = ['1 to 10', '11 to 100', '101 to 1000', 'Small']

    # target_actors = ['Guard', 'Doctor or nurse', 'Acquaintance', 'Call center', 'Customer', 'Manager', 'Cashier',
    #                   'State-affiliated', 'End-user', 'Executive', 'System admin', 'Developer', 'Human resources',
    #                   'Finance', 'Auditor', 'Former employee', 'Other', 'Competitor', 'Helpdesk', 'Unaffiliated',
    #                   'Nation-state', 'Organized crime', 'Unknown', 'Maintenance', 'Activist', 'Terrorist',
    #                   'Force majeure']
    target_actors = ['Customer', 'State-affiliated', 'End-user', 'Former employee', 'Competitor', 'Nation-state',
                     'Organized crime', 'Activist']

    # All disclosure values: ['Yes', 'No', 'Potentially', 'Unknown']

    @classmethod
    def save_stats(cls, outfile_name):
        csv_rows = []
        cls.update_aggregate_statistics()

        actor_header = 'Actor'
        success_rate_header = 'Success Rate'
        n_header = 'n'
        prevalence_rate_header = 'Prevalence Rate'

        csv_header = [actor_header, success_rate_header, n_header, prevalence_rate_header, n_header]
        csv_rows.append(csv_header)

        for actor in cls.all_actor_success:
            if (actor in cls.target_actors) and (actor in cls.sb_actor_prevalence):
                success_rate = f'{cls.all_actor_success[actor]["success-rate"]:0.3}'
                success_n = f'{cls.all_actor_success[actor]["count"]}'
                prevalence_rate = f'{cls.sb_actor_prevalence[actor]["prevalence-rate"]:0.3}'
                prevalence_n = f'{cls.sb_actor_prevalence[actor]["count"]}'

                csv_row = [success_rate, success_n, prevalence_rate, prevalence_n]
                csv_rows.append(csv_row)

        outfile_path = Path(outfile_name)
        with outfile_path.open('w') as outfile:
            csv_writer = csv.writer(outfile)
            csv_writer.writerows(csv_rows)

    @classmethod
    def print_stats(cls):
        cls.update_aggregate_statistics()

        actor_header = 'Actor'
        success_rate_header = 'Success Rate'
        n_header = 'n'
        prevalence_rate_header = 'Prevalence Rate'

        print(f'{actor_header:20s} {success_rate_header:15s} {n_header:10s} {prevalence_rate_header:15s} {n_header:5s}')
        print(f'{"-" * 70}')

        for actor in cls.all_actor_success:
            if (actor in cls.target_actors) and (actor in cls.sb_actor_prevalence):
                success_rate = f'{cls.all_actor_success[actor]["success-rate"]:0.3}'
                success_n = f'{cls.all_actor_success[actor]["count"]}'
                prevalence_rate = f'{cls.sb_actor_prevalence[actor]["prevalence-rate"]:0.3}'
                prevalence_n = f'{cls.sb_actor_prevalence[actor]["count"]}'

                print(f'{actor:20s} {success_rate:15s} {success_n:10s} {prevalence_rate:15s} {prevalence_n:5s}')

    @classmethod
    def update_aggregate_statistics(cls):
        # Compute success rates based on all incidents
        for actor in cls.all_actor_success:
            success_count = cls.all_actor_success[actor]['success']
            fail_count = cls.all_actor_success[actor]['fail']
            maybe_count = cls.all_actor_success[actor]['maybe']
            cls.all_actor_success[actor]['success-rate'] = success_count / (success_count + fail_count + maybe_count)
            cls.all_actor_success[actor]['count'] = success_count + fail_count + maybe_count

        # Compute actor prevalence for small businesses
        for actor in cls.sb_actor_prevalence:
            actor_count = cls.sb_actor_prevalence[actor]['count']
            cls.sb_actor_prevalence[actor]['prevalence-rate'] = actor_count / cls.sb_incident_count

        cls.sort_actor_counts()

    @classmethod
    def sort_actor_counts(cls):
        cls.all_actor_success = cls.sort_descending(cls.all_actor_success, 'count')
        cls.sb_actor_prevalence = cls.sort_descending(cls.sb_actor_prevalence, 'count')

    # Returns dictionary with elements of dictionary of dictionaries d sorted by d[i][p]
    @staticmethod
    def sort_descending(d, p):
        sorted_tuple_list = sorted(d.items(), key=lambda item: item[1][p])
        sorted_tuple_list.reverse()
        return dict(sorted_tuple_list)

    def __init__(self, ij):
        self.incident_json = ij
        self.employee_count = self.incident_json['victim']['employee_count']

        self.is_sb = self.get_is_sb()
        self.is_breach = self.get_is_breach()
        self.actor_varieties = self.get_actor_varieties()

        self.update_statistics()

    def update_statistics(self):
        # Update actor success for all breaches
        for actor_variety in self.actor_varieties:
            if self.is_breach is True:
                if actor_variety in Incident.all_actor_success:
                    success_count = Incident.all_actor_success[actor_variety]['success']
                    Incident.all_actor_success[actor_variety]['success'] = success_count + 1
                else:
                    Incident.all_actor_success[actor_variety] = {'success': 1, 'fail': 0, 'maybe': 0}

            elif self.is_breach is False:
                if actor_variety in Incident.all_actor_success:
                    fail_count = Incident.all_actor_success[actor_variety]['fail']
                    Incident.all_actor_success[actor_variety]['fail'] = fail_count + 1
                else:
                    Incident.all_actor_success[actor_variety] = {'success': 0, 'fail': 1, 'maybe': 0}

            elif self.is_breach is None:
                if actor_variety in Incident.all_actor_success:
                    maybe_count = Incident.all_actor_success[actor_variety]['maybe']
                    Incident.all_actor_success[actor_variety]['maybe'] = maybe_count + 1
                else:
                    Incident.all_actor_success[actor_variety] = {'success': 0, 'fail': 0, 'maybe': 1}

        # Update actor counts and total incidents for small business breaches
        if self.is_sb is True:
            Incident.sb_incident_count = Incident.sb_incident_count + 1

            for actor_variety in self.actor_varieties:
                if actor_variety in Incident.sb_actor_prevalence:
                    actor_count = Incident.sb_actor_prevalence[actor_variety]['count']
                    Incident.sb_actor_prevalence[actor_variety]['count'] = actor_count + 1
                else:
                    Incident.sb_actor_prevalence[actor_variety] = {'count': 1}

    def get_is_sb(self):
        is_sb = False
        if self.employee_count in Incident.target_employee_counts:
            is_sb = True

        return is_sb

    def get_is_breach(self):
        attributes = self.incident_json['attribute'].values()
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

    def get_actor_varieties(self):
        actor_categories = self.incident_json['actor'].values()
        actor_varieties = []
        for actor_category in actor_categories:
            if 'variety' in actor_category:
                actors = actor_category['variety']
                for actor in actors:
                    actor_varieties.append(actor)
        return actor_varieties


# Get validated .json files of each incident
data_folder = Path('../VCDB/data/json/validated/')
file_paths = list(data_folder.glob('*.json'))

for file_path in file_paths:
    with file_path.open() as f:
        incident_json = json.load(f)
        incident = Incident(incident_json)

Incident.print_stats()
Incident.save_stats('output.csv')
