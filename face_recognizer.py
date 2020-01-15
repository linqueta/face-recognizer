import boto3
import json

s3 = boto3.resource('s3')
bucket_name = 'linqueta-fa-images'
collection_name = 'faces'
client = boto3.client('rekognition', region_name='us-east-1')

def recognize():
    return client.index_faces(
        CollectionId=collection_name,
        DetectionAttributes=['DEFAULT'],
        ExternalImageId='TEMPORARY',
        Image={
            'S3Object': {
                'Bucket': bucket_name,
                'Name': 'drake-jeni.png',
            },
        },
    )

def list_face_ids(faces):
    return list(map(lambda x: x['Face']['FaceId'], faces['FaceRecords']))

def search_face(face_id):
    return client.search_faces(
        CollectionId=collection_name,
        FaceId=face_id,
        FaceMatchThreshold=80,
        MaxFaces=10,
    )

def compare(face_ids):
    return list(map(search_face, face_ids))

def response_dict(payload):
    return dict(
        name=payload['Face']['ExternalImageId'],
        faceMatch=round(payload['Similarity'])
    )

def handle(compared):
    filtered = filter(lambda x: x['FaceMatches'], compared)
    return list(map(lambda x: response_dict(x['FaceMatches'][0]), filtered))

def main():
    faces = recognize()
    face_ids = list_face_ids(faces)
    compared = compare(face_ids)
    return handle(compared)

if __name__ == "__main__":
    main()
