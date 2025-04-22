#!/usr/bin/env python
"""
Script to run the WeatherVibesAgent with a sample request.
This demonstrates how to call the agent directly.

Usage:
    python run_agent.py [location]
    python run_agent.py --location "New York" --units imperial --mood chill
"""
import asyncio
import argparse
import json
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Run the Weather Vibes Agent")
    parser.add_argument("location", nargs="?", default=None, help="Location to get weather for (e.g., 'New York', 'Tokyo')")
    parser.add_argument("--location", "-l", dest="location_opt", help="Alternative way to specify location")
    parser.add_argument("--units", "-u", choices=["metric", "imperial"], default="metric", 
                        help="Units for temperature (metric=Celsius, imperial=Fahrenheit)")
    parser.add_argument("--mood", "-m", help="Optional mood for the YouTube video (e.g., 'relaxing', 'upbeat')")
    parser.add_argument("--recommendations", "-r", type=int, default=5, 
                        help="Maximum number of recommendations to show")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show detailed weather information")
    
    return parser.parse_args()

# Ensure all required API keys are set
required_keys = ["OPENAI_API_KEY", "OPENWEATHER_API_KEY", "YOUTUBE_API_KEY"]
missing_keys = [key for key in required_keys if not os.getenv(key)]
if missing_keys:
    print(f"Error: Missing required environment variables: {', '.join(missing_keys)}")
    print("Make sure they are set in your environment or in a .env file")
    sys.exit(1)

# Add the project root to system path for imports
current_dir = Path(__file__).resolve().parent
project_root = current_dir.parent  # this is 02-weather-vibes-agent directory
sys.path.insert(0, str(project_root))

# Import the agent
from weather_vibes.agent.weather_vibes_agent import WeatherVibesAgent

async def main():
    """Run the agent with command-line arguments"""
    # Parse command-line arguments
    args = parse_args()
    
    # Determine the location (prioritize positional argument, then named argument, then prompt)
    location = args.location or args.location_opt
    if not location:
        location = input("Enter a location (default: New York): ") or "New York"
    
    print("Initializing WeatherVibesAgent...")
    
    # Create the agent
    agent = WeatherVibesAgent()
    
    # Create a request based on command-line arguments
    request = {
        "input": {
            "location": location,
            "units": args.units
        },
        "config": {
            "verbose": args.verbose,
            "max_recommendations": args.recommendations,
            "video_mood": args.mood
        },
        "metadata": {
            "user_id": "demo_user",
            "session_id": "demo_session"
        }
    }
    
    print(f"\nProcessing request for location: {location}")
    print("Request details:", json.dumps(request, indent=2))
    
    # Process the request
    try:
        response = await agent.process_acp_request(request)
        
        # Format and display the response
        print("\n=== RESPONSE ===")
        if "error" in response:
            print(f"Error: {response['message']}")
        else:
            output = response["output"]
            
            # Display weather information
            weather = output["weather"]
            temp_unit = "°F" if args.units == "imperial" else "°C"
            speed_unit = "mph" if args.units == "imperial" else "m/s"
            
            print(f"\n🌤️  WEATHER FOR {weather['location']} 🌤️")
            print(f"Temperature: {weather['temperature']}{temp_unit}")
            print(f"Condition: {weather['condition']}")
            print(f"Humidity: {weather['humidity']}%")
            print(f"Wind Speed: {weather['wind_speed']} {speed_unit}")
            
            if args.verbose and "feels_like" in weather:
                print(f"Feels Like: {weather['feels_like']}{temp_unit}")
                print(f"Description: {weather.get('description', '')}")
            
            # Display recommendations
            recommendations = output["recommendations"]
            print(f"\n🧳 RECOMMENDATIONS 🧳")
            for item in recommendations:
                print(f"- {item}")
            
            # Display video information
            video = output["video"]
            print(f"\n🎵 MATCHING VIDEO 🎵")
            if "error" in video:
                print(f"Couldn't find a video: {video.get('error', 'Unknown error')}")
            else:
                print(f"Title: {video['title']}")
                print(f"Channel: {video['channel']}")
                print(f"URL: {video['url']}")
                print(f"Based on query: {video['query']}")
    
    except Exception as e:
        print(f"Error running agent: {str(e)}")
        # Print more detailed error information in debug mode
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main()) 