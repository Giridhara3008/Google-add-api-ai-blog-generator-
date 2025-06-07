# seo_fetcher.py
import os
from google.ads.googleads.errors import GoogleAdsException
from google.ads.googleads.client import GoogleAdsClient
GOOGLE_ADS_YAML_PATH = "/Users/giridharasrikarchittem/Desktop/ai-blog-generator-interview-srikar chittem/google-ads.yaml"
customer_id="8929909292"
# Initialize client once
client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML_PATH)



# A mapping from the API's enum to a user-friendly string.
COMPETITION_LEVELS = {
    1: 'UNKNOWN',
    2: 'LOW',
    3: 'MEDIUM',
    4: 'HIGH'
}

def fetch_seo_data(client, customer_id, keyword):
    """
    Fetches keyword ideas and historical metrics from the Google Ads API.

    Args:
        client: An initialized GoogleAdsClient instance.
        customer_id: The ID of the customer account to use for the request.
        keyword: The keyword to get ideas for.

    Returns:
        A list of dictionaries, where each dictionary contains data for a
        keyword idea, or None if an error occurs.
    """
    try:
        keyword_plan_idea_service = client.get_service("KeywordPlanIdeaService")
        
        # 1. Configure the request
        request = client.get_type("GenerateKeywordIdeasRequest")
        request.customer_id = customer_id
        
        # Set language (1000 is for English)
        request.language = "languageConstants/1000"  # English

        
        # Set geo-targeting (2840 is for United States)
        # To find other codes: https://developers.google.com/google-ads/api/reference/data/geotargets
        request.geo_target_constants.append("geoTargetConstants/2840")
        
        # Include historical metrics
        request.include_adult_keywords = False
        request.historical_metrics_options.year_month_range.start.year = 2022
        request.historical_metrics_options.year_month_range.start.month = 1
        request.historical_metrics_options.year_month_range.end.year = 2022
        request.historical_metrics_options.year_month_range.end.month = 12
        
        # Set the keyword seed
        request.keyword_seed.keywords.append(keyword)

        # 2. Make the API call
        response = keyword_plan_idea_service.generate_keyword_ideas(request=request)

        # 3. Process the results
        seo_results = []
        for idea in response:
            metrics = idea.keyword_idea_metrics
            competition_level = COMPETITION_LEVELS.get(metrics.competition, 'UNKNOWN')
            
            seo_results.append({
                "keyword": idea.text,
                "avg_monthly_searches": metrics.avg_monthly_searches,
                "competition": competition_level,
                # Bids are in micros (1,000,000 micros = 1 unit of currency)
                "low_top_of_page_bid": metrics.low_top_of_page_bid_micros / 1_000_000 if metrics.low_top_of_page_bid_micros else 0,
                "high_top_of_page_bid": metrics.high_top_of_page_bid_micros / 1_000_000 if metrics.high_top_of_page_bid_micros else 0
            })
            
        return seo_results

    except GoogleAdsException as ex:
        print(f'Request with ID "{ex.request_id}" failed with status '
              f'"{ex.error.code().name}" and includes the following errors:')
        for error in ex.failure.errors:
            print(f'\tError with message "{error.message}".')
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print(f'\t\tOn field: {field_path_element.field_name}')
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None