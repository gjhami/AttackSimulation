"""
This module is used to parse the VCDB incident .json files for data which is then used as inputs
for the likelihood a random attack is perpetrated by a given actor. Also,  the likelihood an attack
perpetrated by a given actor on a small business is likely to succeed or fail when the vitim is a
small to medium sized business. Success for an actor is a confirmed data breach, while failure is a
confirmed lack of a data breach. A small to medium sized business is defined as a business with
1000 or fewer employees. This convention stems from the definition of small business used in VCDB
reporting.
"""
from pathlib import Path
import csv
import json


class Incident:
    """
    This class is used to track incidents parsed from the .json file reports which make up the VCDB
    data. Each .json file is converted to an instance of the Incident class. Class variables are
    then used to track aggregate statistics across all incidents. Class methods are then used
    to print these statistics in a text-based table or output them to a .csv file.
    """
    # Track breach vs. non-breach incidents for each actor in all incidents
    # actor: {'success', 'fail', 'maybe', 'fail-rate'}... 'total': {'count'}
    all_actor_fail = {'total': {'count': 0}}

    # Track all incidents for each actor if the victim is a small business
    # actor: {'count', 'prevalence-rate'}... 'total': count
    sb_actor_prevalence = {'total': {'count': 0}}

    # target_employee_counts = ['1 to 10', '11 to 100', '101 to 1000', '1001 to 10000',
    #                           '10001 to 25000', '25001 to 50000', '50001 to 100000',
    #                           'Over 100000', 'Small', 'Large', 'Unknown']
    target_employee_counts = ['1 to 10', '11 to 100', '101 to 1000', 'Small']

    # target_actors = {'Guard', 'Doctor or nurse', 'Acquaintance', 'Call center', 'Customer',
    #                  'Manager', 'Cashier', 'State-affiliated', 'End-user', 'Executive',
    #                  'System admin', 'Developer', 'Human resources', 'Finance', 'Auditor',
    #                  'Former employee', 'Other', 'Competitor', 'Helpdesk', 'Unaffiliated',
    #                  'Nation-state', 'Organized crime', 'Unknown', 'Maintenance', 'Activist',
    #                  'Terrorist', 'Force majeure'}
    target_actors = {'State-affiliated', 'Former employee', 'Competitor', 'Nation-state',
                     'Organized crime', 'Activist'}

    all_years = []

    # All disclosure values: ['Yes', 'No', 'Potentially', 'Unknown']

    @classmethod
    def save_stats(cls, outfile_name):
        """
        save_stats(cls, outfile_name)

        :param str outfile_name: Name of the file to which to save Incident statistics as a CSV

        Saves actor names, overall fail rates, overall sample size, small business prevalence,
        and small business sample size to a provided file as a csv.
        Does not return anything.
        """
        csv_rows = []
        cls.update_aggregate_statistics()

        csv_header = ['Actor', 'Fail Rate', 'n', 'N', 'Prevalence Rate', 'n', 'N']
        csv_rows.append(csv_header)

        # Limit results to include only actors who appear in both the failure dictionary and the
        # prevalence dictionary and the set of target actors
        actors_with_complete_data = list(cls.all_actor_fail.keys() & cls.sb_actor_prevalence.keys()
                                         & cls.target_actors)

        for actor in actors_with_complete_data:
            fail_rate = f'{cls.all_actor_fail[actor]["fail-rate"]:0.3}'
            prevalence_rate = f'{cls.sb_actor_prevalence[actor]["prevalence-rate"]:0.3}'

            csv_row = [actor, fail_rate, cls.all_actor_fail[actor]["count"],
                       cls.all_actor_fail["total"]["count"], prevalence_rate,
                       cls.sb_actor_prevalence[actor]["count"],
                       cls.sb_actor_prevalence["total"]["count"]]
            csv_rows.append(csv_row)

        outfile_path = Path(outfile_name)

        with outfile_path.open('w', encoding="utf-8") as outfile:
            csv_writer = csv.writer(outfile)
            csv_writer.writerows(csv_rows)

    @classmethod
    def print_stats(cls):
        """
        print_stats(cls)

        Updates aggregate statistics being tracked across all instances of Incident. Then, prints
        the aggregate statistics in a text-based table for actors which appear in both the
        dictionary of all incidents used to track actor success rates as well as the
        dictionary used to track the prevalence of actors with small business victims.
        """
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

        # Limit results to include only actors who appear in both the failure dictionary and the
        # prevalence dictionary and the set of target actors
        actors_with_complete_data = list(cls.all_actor_fail.keys() & cls.sb_actor_prevalence.keys()
                                         & cls.target_actors)

        for actor in actors_with_complete_data:
            fail_rate = f'{cls.all_actor_fail[actor]["fail-rate"]:0.3}'
            fail_n = f'{cls.all_actor_fail[actor]["count"]}'
            fail_big_n = f'{cls.all_actor_fail["total"]["count"]}'
            prevalence_rate = f'{cls.sb_actor_prevalence[actor]["prevalence-rate"]:0.3}'
            prevalence_n = f'{cls.sb_actor_prevalence[actor]["count"]}'
            prevalence_big_n = f'{cls.sb_actor_prevalence["total"]["count"]}'

            print(f'{actor:20s} {fail_rate:15s} {fail_n:10s} {fail_big_n:10s}', end='')
            print(f'{prevalence_rate:17s} {prevalence_n:5s} {prevalence_big_n}')

    @classmethod
    def update_aggregate_statistics(cls):
        """
        update_aggregate_statistics(cls)

        Computes aggregate statistics about instances of Incident using class variables. Statistics
        include fail rate and prevalence rate. This method should be called after all instances of
        Incident have been created or before outputting statistics.
        """

        # Compute fail rates based incidents with and without data breaches
        for actor, actor_stats in cls.all_actor_fail.items():
            if actor != 'total':
                success_count = actor_stats['success']
                fail_count = actor_stats['fail']
                actor_stats['fail-rate'] = fail_count / (success_count + fail_count)
                actor_stats['count'] = success_count + fail_count

        # Compute actor prevalence for small businesses
        total = cls.sb_actor_prevalence["total"]["count"]
        for actor, actor_stats in cls.sb_actor_prevalence.items():
            if actor != 'total':
                actor_count = actor_stats['count']
                actor_stats['prevalence-rate'] = actor_count / total

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

    def update_statistics(self):
        """
        update_statistics(self)

        Updates class variables tracking the number of occurrences of actor successes, failures,
        and maybes. A success is an incident involving an actor which results in a data
        breach. A failure is an incident involving an actor which definitely did not result in a
        data breach. A maybe indicates the report does not conclusively indicate there was or was
        not a data breach. The total number of incidents as well as the total number of incidents
        in which a small business was the victim is also incremented. Lastly, counts for each actor
        involved in incidents where small businesses were the victim is also incremented.
        """
        # Update actor success for all breaches
        for actor_variety in self.actor_varieties:
            if self.is_breach is True:
                Incident.all_actor_fail["total"]["count"] += 1
                default_value = {'success': 1, 'fail': 0, 'maybe': 0}
                Incident.add_or_increment(actor_variety, default_value, 'success',
                                          Incident.all_actor_fail)

            elif self.is_breach is False:
                Incident.all_actor_fail["total"]["count"] += 1
                default_value = {'success': 0, 'fail': 1, 'maybe': 0}
                Incident.add_or_increment(actor_variety, default_value, 'fail',
                                          Incident.all_actor_fail)

            elif self.is_breach is None:
                default_value = {'success': 0, 'fail': 0, 'maybe': 1}
                Incident.add_or_increment(actor_variety, default_value, 'maybe',
                                          Incident.all_actor_fail)

        # Update actor counts and total incidents for small business breaches
        if self.is_sb is True:
            Incident.sb_actor_prevalence["total"]["count"] += 1

            for actor_variety in self.actor_varieties:
                default_value = {'count': 1}
                Incident.add_or_increment(actor_variety, default_value, 'count',
                                          Incident.sb_actor_prevalence)

    @classmethod
    def add_or_increment(cls, key, value, sub_key, dictionary):
        """
        add_or_increment(cls, key, value, sub_key, dictionary)

        :param str key: Key in dictionary where dictionary[key] is set to value if it does not exist
        :param dict value: dictionary[key] is set to value if it does not exist
        :param str sub_key: If dictionary[key] exists, then dictionary[key][sub_key] is incremented
        :param dict dictionary: Dictionary to be modified
        :return: Returns the updated dictionary
        :rtype: dict

        Increments dictionary[key][sub_key] if dictionary[key] exists. Otherwise, sets
        dictionary[key] to value.
        """
        if key in dictionary:
            dictionary[key][sub_key] = dictionary[key][sub_key] + 1
        else:
            dictionary[key] = value
        return dictionary

    def get_is_sb(self):
        """
        get_is_sb(self)

        :return: True if the victim in the incident was a small business, otherwise False
        :rtype: bool
        """
        is_sb = bool(self.employee_count in Incident.target_employee_counts)
        return is_sb

    def get_is_breach(self):
        """
        get_is_breach(self)

        :return: Boolean True if the incident was a breach, False if the incident was not a breach,
        and None if the incident may have been a breach.
        :rtype: bool

        Returns True if the incident involved confirmed data disclosure, False if the incident only
        involved only confirmed instances of data disclosure, or None if the incident involved any
        instances of 'Unknown' or 'Potentially' data disclosure.
        """
        attributes = self.incident_json['attribute'].values()
        is_breach = False
        is_uncertain = False
        for attribute in attributes:
            if ('data_disclosure' in attribute) and (attribute['data_disclosure'] == 'Yes'):
                is_breach = True
            elif ('data_disclosure' in attribute) and (attribute['data_disclosure'] in
                                                       ['Potentially', 'Unknown']):
                is_uncertain = True

        # Return none if there is no definite breach, but it's not all 'No's
        is_breach = None if (not is_breach) and is_uncertain else is_breach

        return is_breach

    def get_actor_varieties(self):
        """
        get_actor_varieties(self)

        :return: List of actor varieties involved in the incident. May contain the same variety
        multiple times or be empty if no actor varieties were included in the incident report.
        :rtype: list[str]
        """
        actor_varieties = []
        actor_variety_lists = [category['variety'] for category in
                               self.incident_json['actor'].values() if 'variety' in category]
        for actor_variety_list in actor_variety_lists:
            actor_varieties.extend(actor_variety_list)
        return actor_varieties


def main():
    """
    Main function called when the script is run
    """

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
