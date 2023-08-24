import requests
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.conf import settings

# Replace these values with your actual Instagram API credentials
INSTAGRAM_CLIENT_ID = '1248213715843678'
INSTAGRAM_CLIENT_SECRET = '235c2abc2998db2d62953c356ba6a9f4'
INSTAGRAM_REDIRECT_URI = 'http://localhost:8000/instagram_oauth/callback/'

@csrf_exempt
def increase_reels_views(request):
    if request.method == 'POST':
        try:
            reels_link = request.POST.get('reels_link')  # Use get() for safer dictionary access
            
            # Check if the access token is in the session
            if 'access_token' in request.session:
                access_token = request.session['access_token']
            else:
                return redirect('instagram_oauth')  # Redirect to Instagram OAuth
            
            # Make a request to Instagram API to increment views
            response = requests.get(f'https://graph.instagram.com/{reels_link}',
                                    params={'fields': 'id,media_type', 'access_token': access_token})
            
            if response.status_code == 200:
                data = response.json()
                media_id = data.get('id')
                media_type = data.get('media_type')
                
                if media_type == 'VIDEO':
                    # Make a request to the Insights API to increment views
                    insights_response = requests.post(f'https://graph.instagram.com/{media_id}/insights',
                                                      params={'metric': 'engagement'},
                                                      headers={'Authorization': f'Bearer {access_token}'})
                    
                    if insights_response.status_code == 200:
                        message = 'Reels views increased successfully.'
                    else:
                        message = 'Failed to increase Reels views.'
                else:
                    message = 'The provided link is not a video.'
            else:
                message = 'Failed to retrieve media information.'
            
            return render(request, 'increase_views.html', {'message': message, 'reels_link': reels_link})
            
        except KeyError:
            return JsonResponse({'message': 'Invalid request parameters.'}, status=400)
        
    elif request.method == 'GET':
        return render(request, 'increase_views.html')

    return HttpResponse('Method not allowed.', status=405)

def instagram_oauth(request):
    # Redirect user to Instagram authorization URL
    redirect_url = f'https://api.instagram.com/oauth/authorize?client_id={INSTAGRAM_CLIENT_ID}&redirect_uri={INSTAGRAM_REDIRECT_URI}&response_type=code'
    return redirect(redirect_url)

# Callback for Instagram OAuth
def instagram_oauth_callback(request):
    if 'code' in request.GET:
        code = request.GET['code']
        
        # Exchange the authorization code for an access token
        access_token = get_access_token(code)
        
        if access_token:
            # Store the access token in the session
            request.session['EAADlzevV4IcBO1VCwitL1npCTacE4wi85xgKZB4ADtrPiTW4PHriJmAg9wZAtbuDLaTsaZC2ILZBbjSswrtkvpwjR5qIxx7ueB9BstlDX8p35buEaaPHISM7ZCDpR3SX5KPkfQZBgv8NZCMXtVerHridBeAPxjtFk03E4UWs1VtGOkTRuhXs55M0eEY20HZA2KYmUZBQ3g7Vfr0R3Pqoh3eRNB4iwZCqjfjwUAZCOaCtTlFJOQWqcrcUmifPA6EQxYwGWFxkc8OkjQJZCwAZD'] = access_token
            return redirect('increase_reels_views')
        else:
            return HttpResponse('Failed to obtain access token.', status=500)
    else:
        return HttpResponse('Missing authorization code.', status=400)

def get_access_token(code):
    # Exchange the authorization code for an access token
    response = requests.post('https://api.instagram.com/oauth/access_token', data={
        'client_id': INSTAGRAM_CLIENT_ID,
        'client_secret': INSTAGRAM_CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'redirect_uri': INSTAGRAM_REDIRECT_URI,
        'code': code
    })
    
    if response.status_code == 200:
        return response.json().get('EAADlzevV4IcBO1VCwitL1npCTacE4wi85xgKZB4ADtrPiTW4PHriJmAg9wZAtbuDLaTsaZC2ILZBbjSswrtkvpwjR5qIxx7ueB9BstlDX8p35buEaaPHISM7ZCDpR3SX5KPkfQZBgv8NZCMXtVerHridBeAPxjtFk03E4UWs1VtGOkTRuhXs55M0eEY20HZA2KYmUZBQ3g7Vfr0R3Pqoh3eRNB4iwZCqjfjwUAZCOaCtTlFJOQWqcrcUmifPA6EQxYwGWFxkc8OkjQJZCwAZD')
    else:
        return None
