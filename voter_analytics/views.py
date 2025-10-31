## voter_analytics/views.py
## Author: William Fugate wfugate@bu.edu
## description: views.py for voter_analytics app

from django.views.generic import ListView, DetailView
from .models import Voter
import plotly
import plotly.graph_objs as go

class VoterListView(ListView):
    '''View to see the full list of voters.'''
    model = Voter
    template_name = 'voter_analytics/voter_list.html'
    context_object_name = 'voters'
    paginate_by = 100

    def get_queryset(self):
        '''Filters the Voters by specified search parameters from GET request'''
        queryset = Voter.objects.all() #get the voter objects

        #get the search parameters from the request (will be null if not present)
        party = self.request.GET.get('party_affiliation')
        min_year = self.request.GET.get('min_birth_year')
        max_year = self.request.GET.get('max_birth_year')
        voter_score = self.request.GET.get('voter_score')

        v20state = self.request.GET.get('v20state')
        v21town = self.request.GET.get('v21town')
        v21primary = self.request.GET.get('v21primary')
        v22general = self.request.GET.get('v22general')
        v23town = self.request.GET.get('v23town')

        #check each parameter and apply a filter for it if present, resulting in filtered a list
        if party:
            queryset = queryset.filter(party_affiliation=party.strip())

        if min_year:
            queryset = queryset.filter(date_of_birth__year__gte=int(min_year))
        
        if max_year:
            queryset = queryset.filter(date_of_birth__year__lte=int(max_year))
        
        if voter_score:
            queryset = queryset.filter(voter_score=int(voter_score))

        if v20state:
            queryset = queryset.filter(v20state=True)

        if v21town:
            queryset = queryset.filter(v21town=True)
        
        if v21primary:
            queryset = queryset.filter(v21primary=True)

        if v22general:
            queryset = queryset.filter(v22general=True)
        
        if v23town:
            queryset = queryset.filter(v23town=True)
        return queryset

    def get_context_data(self, **kwargs):
        '''Adds party affiliations and birth_years and voter_scores to VoterListView context'''
        context = super().get_context_data(**kwargs)

        parties = Voter.objects.values_list('party_affiliation', flat=True).distinct().order_by('party_affiliation') #get all party affiliations as a list (flat) then get distinct and order them 
        party_affiliations = []
        for p in parties: #stripping the whitespace
            if p:
                party_affiliations += [p.strip()] 
        context['party_affiliations'] = party_affiliations #assigning to context                                       
        context['birth_years'] = range(1900, 2025)
        context['voter_scores'] = range(0, 6)
        return context



class VoterDetailView(DetailView):
    '''View to see a single voters details'''
    model = Voter
    template_name = 'voter_analytics/voter_detail.html'
    context_object_name = 'voter'


class GraphsView(ListView):
    '''View to see the voter data graphs'''
    model = Voter
    template_name = 'voter_analytics/graphs.html'
    context_object_name = 'voters'
    
    def get_queryset(self):
        '''Filters the voters based on search parameters'''
        #same filtering logic from VoterListView
        queryset = Voter.objects.all()
        
        party = self.request.GET.get('party_affiliation')
        min_year = self.request.GET.get('min_birth_year')
        max_year = self.request.GET.get('max_birth_year')
        voter_score = self.request.GET.get('voter_score')

        v20state = self.request.GET.get('v20state')
        v21town = self.request.GET.get('v21town')
        v21primary = self.request.GET.get('v21primary')
        v22general = self.request.GET.get('v22general')
        v23town = self.request.GET.get('v23town')
        
        if party:
            queryset = queryset.filter(party_affiliation=party.strip())
        
        if min_year:
            queryset = queryset.filter(date_of_birth__year__gte=int(min_year))
        
        if max_year:
            queryset = queryset.filter(date_of_birth__year__lte=int(max_year))
        
        if voter_score:
            queryset = queryset.filter(voter_score=int(voter_score))
        
        if v20state:
            queryset = queryset.filter(v20state=True)

        if v21town:
            queryset = queryset.filter(v21town=True)
        
        if v21primary:
            queryset = queryset.filter(v21primary=True)

        if v22general:
            queryset = queryset.filter(v22general=True)
        
        if v23town:
            queryset = queryset.filter(v23town=True)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        '''Creates graphs based on Voter data and adds them to the context of the GraphsView'''
        context = super().get_context_data(**kwargs)
        
        voters = self.get_queryset() #getting the set of Voters
        
        #same as VoterListView
        parties = Voter.objects.values_list('party_affiliation', flat=True).distinct().order_by('party_affiliation')
        party_affiliations = []
        for p in parties: #stripping the whitespace
            if p:
                party_affiliations += [p.strip()] 
        context['party_affiliations'] = party_affiliations #assigning to context     
        context['birth_years'] = range(1900, 2010)
        context['voter_scores'] = range(0, 6)
        
        #birth year graph
        birth_years = []
        for voter in voters: #get all the voter year of births into a list
            if voter.date_of_birth:
                birth_years.append(voter.date_of_birth.year)

        year_counts = {}
        for year in birth_years: #find out how many of each year of birth there is
            year_counts[year] = year_counts.get(year, 0) + 1
        
        sorted_years = sorted(year_counts.keys()) #sort to put data in order
        counts = []
        for year in sorted_years: 
            counts += [year_counts[year]] #create a list of the sorted counts (to align with the years in order)
        
        figure1 = go.Bar(x=sorted_years, y=counts) #make the bar graph 

        title1='Distribution of Voters by Birth Year'
        birth_year_graph = plotly.offline.plot({"data": [figure1], #plot
                                         "layout_title_text": title1,
                                         }, 
                                         auto_open=False, 
                                         output_type="div")
        # send div as template context variable
        context['birth_year_graph'] = birth_year_graph
        
        #party affiliation graph
        party_counts = {}
        for voter in voters: #make a list that counts how many of each party we have
            party = voter.party_affiliation.strip()
            party_counts[party] = party_counts.get(party, 0) + 1

        figure2 = go.Pie( #make the graph 
                labels=list(party_counts.keys()), 
                values=list(party_counts.values()),
                textposition='inside'
            )
        title2='Distribution of Voters by Party Affiliation'
        party_affiliation_graph = plotly.offline.plot({"data": [figure2], #plot it
                                         "layout_title_text": title2,
                                         }, 
                                         auto_open=False, 
                                         output_type="div")
        # send div as template context variable
        context['party_affiliation_graph'] = party_affiliation_graph
        
        #election participation graph
        elections = ['v20state','v21town','v21primary','v22general', 'v23town']
        election_counts = {}
        for field in elections: #make a dict of the counts 
            count = voters.filter(**{field: True}).count()
            election_counts[field] = count
        
        figure3 = go.Bar(x=list(election_counts.keys()), y=list(election_counts.values())) #make the graph 

        title3='Voter Participation by Election'
        election_participation_graph = plotly.offline.plot({"data": [figure3], #plot
                                         "layout_title_text": title3,
                                         }, 
                                         auto_open=False, 
                                         output_type="div")
        # send div as template context variable
        context['election_participation_graph'] = election_participation_graph
        #return with all the graphs in the updated context
        return context