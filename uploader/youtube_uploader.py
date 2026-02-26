import googleapiclient.discovery
from googleapiclient.http import MediaFileUpload


def upload_video(video_path, title, description, tags):
    youtube = googleapiclient.discovery.build(
        "youtube", "v3", credentials=None
    )

    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": title,
                "description": description,
                "tags": tags,
                "categoryId": "22"
            },
            "status": {"privacyStatus": "public"}
        },
        media_body=MediaFileUpload(video_path)
    )

    response = request.execute()
    return response