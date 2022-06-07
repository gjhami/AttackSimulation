from pathlib import Path
import csv
import json

# Small business (sb) is any business with 1000 or fewer employees


class Incident:
    # Track breach vs. non-breach incidents for each actor in all incidents
    all_actor_fail = {}  # actor: {'success', 'fail', 'maybe', 'fail-rate'}
    all_actor_count = 0
    # Track all incidents for each actor if the victim is a small business
    sb_actor_prevalence = {}  # actor: {'count', 'prevalence-rate'}
    sb_incident_count = 0

    # target_employee_counts = ['1 to 10', '11 to 100', '101 to 1000', '1001 to 10000',
    #                           '10001 to 25000', '25001 to 50000', '50001 to 100000',
    #                           'Over 100000', 'Small', 'Large', 'Unknown']
    target_employee_counts = ['1 to 10', '11 to 100', '101 to 1000', 'Small']

    # target_actors = ['Guard', 'Doctor or nurse', 'Acquaintance', 'Call center', 'Customer',
    #                  'Manager', 'Cashier', 'State-affiliated', 'End-user', 'Executive',
    #                  'System admin', 'Developer', 'Human resources', 'Finance', 'Auditor',
    #                  'Former employee', 'Other', 'Competitor', 'Helpdesk', 'Unaffiliated',
    #                  'Nation-state', 'Organized crime', 'Unknown', 'Maintenance', 'Activist',
    #                  'Terrorist', 'Force majeure']
    target_actors = ['State-affiliated', 'Former employee', 'Competitor',
                     'Nation-state', 'Organized crime', 'Activist']

    # All disclosure values: ['Yes', 'No', 'Potentially', 'Unknown']

    # Saves actor names, overall fail rates, overall sample size, small business prevalence,
    # and small business sample size to a provided file as a csv
    @classmethod
    def save_stats(cls, outfile_name):
        csv_rows = []
        cls.update_aggregate_statistics()

        actor_header = 'Actor'
        fail_rate_header = 'Fail Rate'
        n_header = 'n'
        prevalence_rate_header = 'Prevalence Rate'

        csv_header = [actor_header, fail_rate_header, n_header, prevalence_rate_header, n_header]
        csv_rows.append(csv_header)

        for actor in cls.all_actor_fail:
            if (actor in cls.target_actors) and (actor in cls.sb_actor_prevalence):
                fail_rate = f'{cls.all_actor_fail[actor]["fail-rate"]:0.3}'
                fail_n = f'{cls.all_actor_fail[actor]["count"]}'
                prevalence_rate = f'{cls.sb_actor_prevalence[actor]["prevalence-rate"]:0.3}'
                prevalence_n = f'{cls.sb_actor_prevalence[actor]["count"]}'

                csv_row = [fail_rate, fail_n, prevalence_rate, prevalence_n]
                csv_rows.append(csv_row)

        outfile_path = Path(outfile_name)
        with outfile_path.open('w') as outfile:
            csv_writer = csv.writer(outfile)
            csv_writer.writerows(csv_rows)

    # Prints actor names, overall fail rates, overall sample size, small business prevalence, and
    # small business sample size to stdout
    @classmethod
    def print_stats(cls):
        cls.update_aggregate_statistics()

        actor_header = 'Actor'
        fail_rate_header = 'Fail Rate'
        n_header = 'n'
        big_n_header = 'N'
        prevalence_rate_header = 'Prevalence Rate'

        print(f'{actor_header:20s} {fail_rate_header:15s} {n_header:10s} ', end='')
        print(f'{big_n_header:10s} {prevalence_rate_header:17s} {n_header:5s} ', end='')
        print(f'{big_n_header:5s}')
        print(f'{"-" * 90}')

        for actor in cls.all_actor_fail:
            if (actor in cls.target_actors) and (actor in cls.sb_actor_prevalence):
                fail_rate = f'{cls.all_actor_fail[actor]["fail-rate"]:0.3}'
                fail_n = f'{cls.all_actor_fail[actor]["count"]}'
                fail_big_n = f'{cls.all_actor_count}'
                prevalence_rate = f'{cls.sb_actor_prevalence[actor]["prevalence-rate"]:0.3}'
                prevalence_n = f'{cls.sb_actor_prevalence[actor]["count"]}'
                prevalence_big_n = f'{cls.sb_incident_count}'

                print(f'{actor:20s} {fail_rate:15s} {fail_n:10s} {fail_big_n:10s}', end='')
                print(f'{prevalence_rate:17s} {prevalence_n:5s} {prevalence_big_n}')

    # Computes aggregate statistics about incidents using the class variables which track all
    # instances of the Incident class. This includes fail rate and prevalence rate, and should be
    # called after all instances of Incident have been created or before outputting statistics.
    @classmethod
    def update_aggregate_statistics(cls):
        # Compute fail rates based incidents with and without data breaches
        for actor in cls.all_actor_fail:
            success_count = cls.all_actor_fail[actor]['success']
            fail_count = cls.all_actor_fail[actor]['fail']
            cls.all_actor_fail[actor]['fail-rate'] = fail_count / (success_count + fail_count)
            cls.all_actor_fail[actor]['count'] = success_count + fail_count

        # Compute actor prevalence for small businesses
        for actor in cls.sb_actor_prevalence:
            actor_count = cls.sb_actor_prevalence[actor]['count']
            cls.sb_actor_prevalence[actor]['prevalence-rate'] = actor_count / cls.sb_incident_count

        cls.sort_actor_counts()

    # Sorts the aggregate lists tracking actor fail rate and prevalence in order of sample size
    @classmethod
    def sort_actor_counts(cls):
        cls.all_actor_fail = cls.sort_descending(cls.all_actor_fail, 'count')
        cls.sb_actor_prevalence = cls.sort_descending(cls.sb_actor_prevalence, 'count')

    # Returns dictionary with elements of dictionary of dictionaries d sorted by d[i][p]
    @staticmethod
    def sort_descending(dictionary, sort_parameter):
        sorted_tuple_list = sorted(dictionary.items(), key=lambda item: item[1][sort_parameter])
        sorted_tuple_list.reverse()
        return dict(sorted_tuple_list)

    def __init__(self, input_json):
        self.incident_json = input_json
        self.employee_count = self.incident_json['victim']['employee_count']

        self.is_sb = self.get_is_sb()
        self.is_breach = self.get_is_breach()
        self.actor_varieties = self.get_actor_varieties()

        self.update_statistics()

        # actor_to_investigate = 'Competitor'
        # if actor_to_investigate in self.actor_varieties:
        #     print(f'{self.incident_json["summary"]}\n')

    # Updates aggregate list to reflect the contents of the current incident and actors involved
    def update_statistics(self):
        # Update actor success for all breaches
        for actor_variety in self.actor_varieties:
            if self.is_breach is True:
                Incident.all_actor_count = Incident.all_actor_count + 1
                if actor_variety in Incident.all_actor_fail:
                    success_count = Incident.all_actor_fail[actor_variety]['success']
                    Incident.all_actor_fail[actor_variety]['success'] = success_count + 1
                else:
                    Incident.all_actor_fail[actor_variety] = {'success': 1, 'fail': 0, 'maybe': 0}

            elif self.is_breach is False:
                Incident.all_actor_count = Incident.all_actor_count + 1
                if actor_variety in Incident.all_actor_fail:
                    fail_count = Incident.all_actor_fail[actor_variety]['fail']
                    Incident.all_actor_fail[actor_variety]['fail'] = fail_count + 1
                else:
                    Incident.all_actor_fail[actor_variety] = {'success': 0, 'fail': 1, 'maybe': 0}

            elif self.is_breach is None:
                if actor_variety in Incident.all_actor_fail:
                    maybe_count = Incident.all_actor_fail[actor_variety]['maybe']
                    Incident.all_actor_fail[actor_variety]['maybe'] = maybe_count + 1
                else:
                    Incident.all_actor_fail[actor_variety] = {'success': 0, 'fail': 0, 'maybe': 1}

        # Update actor counts and total incidents for small business breaches
        if self.is_sb is True:
            Incident.sb_incident_count = Incident.sb_incident_count + 1

            for actor_variety in self.actor_varieties:
                if actor_variety in Incident.sb_actor_prevalence:
                    actor_count = Incident.sb_actor_prevalence[actor_variety]['count']
                    Incident.sb_actor_prevalence[actor_variety]['count'] = actor_count + 1
                else:
                    Incident.sb_actor_prevalence[actor_variety] = {'count': 1}

    # Returns True if the incident effected a small business and otherwise returns False
    def get_is_sb(self):
        is_sb = False
        if self.employee_count in Incident.target_employee_counts:
            is_sb = True

        return is_sb

    # Returns True if the incident involved confirmed data disclosure
    # False if the incident only involved only confirmed instances of data disclosure
    # None if the incident involved any instances of 'Unknown' or 'Potentially' data disclosure
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

    # Returns a list of actor varieties involved in the incident. May contain the same variety
    # multiple times.
    def get_actor_varieties(self):
        actor_categories = self.incident_json['actor'].values()
        actor_varieties = []
        for actor_category in actor_categories:
            if 'variety' in actor_category:
                actors = actor_category['variety']
                for actor in actors:
                    actor_varieties.append(actor)
        return actor_varieties


def main():
    # Get validated .json files of each incident
    data_folder = Path('../VCDB/data/json/validated/')
    file_paths = list(data_folder.glob('*.json'))

    # Create a new instance of Incident for each verified incident
    # Incidents are tracked in aggregate using class variables
    for file_path in file_paths:
        with file_path.open() as file:
            incident_json = json.load(file)
            Incident(incident_json)

    # Print statistics to console and save them to a csv
    Incident.print_stats()
    Incident.save_stats('output.csv')


if __name__ == "__main__":
    main()
