import os
import pandas as pd
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .utils import train_and_predict, generate_analysis, generateOverTimePlot


DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'processed_data')

@api_view(['POST'])
def predict(request):
    try:
        state = request.data.get('state')
        city = request.data.get('city')
        months_ahead = int(request.data.get('months_ahead', 1))
        analysis_field = request.data.get('analysis_field', 'adj_value')  # Default to 'adj_value'

        if not state or not city:
            return JsonResponse({'error': 'State and city must be provided'}, status=400)

        city_state = f"{city}{state}".replace(" ", "")  # Removing spaces just in case
        csv_path = os.path.join(DATA_DIR, f"{city_state}.csv")

        if not os.path.exists(csv_path):
            return JsonResponse({'error': f'CSV file not found: {csv_path}'}, status=404)

        data = pd.read_csv(csv_path)

        if analysis_field not in data.columns:
            return JsonResponse({'error': f'Invalid analysis field: {analysis_field}'}, status=400)

        prediction, accuracy = train_and_predict(data, months_ahead, analysis_field)

        formatted_predictions = [round(price, 2) for price in prediction]
        formatted_accuracy = round(accuracy, 2)

        analysis_results = generate_analysis(data, analysis_field)
        over_time_plot = generateOverTimePlot(data, analysis_field)

        return JsonResponse({
            'future_prices': formatted_predictions,
            'accuracy': formatted_accuracy,
            'analysis': analysis_results,
            'over_time': over_time_plot,
        })
    except Exception as e:
        return JsonResponse({'error': f'Internal server error: {str(e)}'}, status=500)

