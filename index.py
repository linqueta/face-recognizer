import boto3

s3 = boto3.resource('s3')
bucket_name = 'linqueta-fa-images'
collection_name = 'faces'
client = boto3.client('rekognition', region_name='us-east-1')

def list_images():
    images = []
    bucket = s3.Bucket(bucket_name)
    for image in bucket.objects.all():
        images.append(image.key)
    print(images)
    return images

def create_collection(collection_id):
    print('Creating collection:' + collection_id)
    response=client.create_collection(CollectionId=collection_id)
    print('Collection ARN: ' + response['CollectionArn'])
    print('Status code: ' + str(response['StatusCode']))
    print('Done...')

def index_collection(images):
    for i in images:
        response = client.index_faces(
            CollectionId=collection_name,
            DetectionAttributes=[
            ],
            ExternalImageId=i[:-4],
            Image={
                'S3Object': {
                    'Bucket': bucket_name,
                    'Name': i,
                },
            },
        )

def main():
    images = list_images()
    # create_collection(collection_name)
    index_collection(images)

if __name__ == "__main__":
    main()
