from google.cloud import vision

from core.models import ImageTag
from discovery import DiscoveryClient


def tib():
    dc = DiscoveryClient()
    vision_client = vision.ImageAnnotatorClient()
    games = dc.all_documents()
    for game in games:
        for image in game.get('screenshots', []):
            image_id = image['image_id']
            if ImageTag.objects.filter(image=image_id).count() == 0:
                url = f"https://images.igdb.com/igdb/image/upload/t_1080p/{image_id}.jpg"
                img = vision.Image()
                img.source.image_uri = url
                web_detection = vision_client.web_detection(image=img).web_detection
                labels = web_detection.web_entities
                for label in labels:
                    desc = label.description.lower()
                    if desc is not None and desc != '':
                        ImageTag.objects.create(game=game['slug'], image=image_id, tag=label.description.lower())
        print(f"Processed {game['name']}")
