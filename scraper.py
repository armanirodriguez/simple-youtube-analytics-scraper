#!/usr/bin/env python3

import os, sys
from datetime import datetime

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow


def main():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    # Get credentials from secrets file
    flow = InstalledAppFlow.from_client_secrets_file(
        "client_secret.json", ["https://www.googleapis.com/auth/yt-analytics.readonly"]
    )
    credentials = flow.run_console()

    start_date_str = input("Enter the starting date (yyyy-mm-dd): ")
    end_date_str = input("Enter the ending date (yyyy-mm-dd): ")

    # Validate Format
    try:
        datetime.strptime(start_date_str, "%Y-%m-%d")
        datetime.strptime(end_date_str, "%Y-%m-%d")
    except ValueError:
        sys.exit("Date format must be (yyyy-mm-dd)")

    video_id = input('Enter the video id (Found after "watch?v=" in the video URL): ')

    with build("youtubeAnalytics", "v2", credentials=credentials) as youtubeAnalyitcs:
        request = youtubeAnalyitcs.reports().query(
            ids="channel==MINE",
            metrics="views,estimatedMinutesWatched,averageViewDuration",
            dimensions="video",
            filters=f"video=={video_id}",
            startDate=start_date_str,
            endDate=end_date_str,
        )
        try:
            response = request.execute()
            data = response["rows"][0]
            print()
            print(
                f"Statistics for video {data[0]} from {start_date_str} to {end_date_str}"
            )
            print(f"View Count: {data[1]}")
            print(f"Watch Time (minutes): {data[2]}")
            print(f"Average View Duration (seconds): {data[3]}")
        except HttpError as e:
            sys.exit(f"Error: {e.error_details} Status Code: {e.status_code}")
        except Exception as e:
            sys.exit(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
