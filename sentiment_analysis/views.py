from django.shortcuts import render
from django.views.generic import TemplateView
from sentiment_analysis.twitter_analysis import TwitterAnalysis

analyizer = TwitterAnalysis()

class SearchView(TemplateView):
    template_name = 'sentiment_analysis/search.html'

def sentiment_view(request):
    if request.method != 'POST':
        return render(request, 'sentiment_analysis/search.html', {'error': 'Error getting context query data'})
    
    query = request.POST['query']
    if query is None:
        return render(request, 'sentiment_analysis/search.html', {'error': 'Error getting query'})
    
    sentiment_data = analyizer.analyze_query(query)
    if sentiment_data is None:
        context = {'error': 'Error getting query sentiment data'}
        return render(request, 'sentiment_analysis/search.html', context)
    
    context = {'preview_tweets': sentiment_data['preview_tweets'], 'sentiment': sentiment_data['sentiment']}
    return render(request, 'sentiment_analysis/sentiment.html', context)
