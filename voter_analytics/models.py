## voter_analytics/models.py
## Author: William Fugate wfugate@bu.edu
## description: Database models and their logic for the voter_analytics app
from django.db import models

class Voter(models.Model):
    '''Model to represent a Voter.'''
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    residence_address_street_number = models.CharField(max_length=100)
    residence_address_street_name = models.CharField(max_length=100)
    residence_address_apt_number = models.CharField(max_length=100)
    residence_address_zip = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    date_of_registration = models.DateField()
    party_affiliation = models.CharField(max_length=10)
    precinct_number = models.CharField(max_length=10)
    v20state = models.BooleanField()
    v21town = models.BooleanField()
    v21primary = models.BooleanField()
    v22general = models.BooleanField()
    v23town = models.BooleanField()
    voter_score = models.IntegerField()

    def __str__(self):
        '''String representation of a voter.'''
        return f"{self.first_name} {self.last_name} - {self.residence_address_street_number} {self.residence_address_street_name}, Apt {self.residence_address_apt_number}, ZIP {self.residence_address_zip}"

def load_data():
    '''Loads voter data into the database models.'''
    filename = '/Users/willi/Downloads/newton_voters.csv'
    
    with open(filename, 'r') as f:
        next(f)  # skip header

        for line in f:

            line = line.strip()
            fields = line.split(',')
            try:
                voter = Voter(
                    last_name = fields[1],
                    first_name = fields[2],
                    residence_address_street_number = fields[3],
                    residence_address_street_name = fields[4],
                    residence_address_apt_number = fields[5],
                    residence_address_zip = fields[6],
                    date_of_birth = fields[7] or None,
                    date_of_registration = fields[8] or None,
                    party_affiliation = fields[9],
                    precinct_number = fields[10],
                    v20state = fields[11] == 'TRUE', #because the data is either TRUE or FALSE, this will evaluate correctly
                    v21town = fields[12] == 'TRUE',
                    v21primary = fields[13] == 'TRUE',
                    v22general = fields[14] == 'TRUE',
                    v23town = fields[15] == 'TRUE',
                    voter_score = int(fields[16])
                )
                voter.save()

            except Exception as e:
                print(f"Skipping line due to error: {e}")
                continue

