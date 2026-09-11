
import boto3
import json
import base64
import uuid

s3 = boto3.client("s3")
rekognition = boto3.client("rekognition")

BUCKET_NAME = "shruti--11"


def lambda_handler(event, context):
    try:
        # Get request body from API Gateway
        body = json.loads(event["body"])

        # Get Base64 image sent from HTML
        image_data = body["image"]

        # Convert Base64 image into bytes
        image_bytes = base64.b64decode(image_data)

        # Generate a unique image name
        file_name = f"uploads/{uuid.uuid4()}.jpg"

        # Upload image to S3
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=file_name,
            Body=image_bytes,
            ContentType="image/jpeg"
        )

        print("Image uploaded to S3:", file_name)

        # Detect faces using Amazon Rekognition
        response = rekognition.detect_faces(
            Image={
                "S3Object": {
                    "Bucket": BUCKET_NAME,
                    "Name": file_name
                }
            },
            Attributes=["DEFAULT"]
        )

        # Count detected faces
        face_count = len(response["FaceDetails"])

        print("Number of faces detected:", face_count)

        # Send result back to HTML
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "content-type",
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "message": "Face detection successful",
                "faceCount": face_count
            })
        }

    except Exception as e:
        print("Error:", str(e))

        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "content-type",
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "error": str(e)
            })
        }
