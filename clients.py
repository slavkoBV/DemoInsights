import boto3


class TranscribeClient:

    def __init__(self, output_bucket):
        self.client = boto3.client('transcribe')
        self.output_bucket = output_bucket

    def transcribe_audio(self, job_name: str, file_path: str):
        response = self.client.start_transcription_job(
            TranscriptionJobName=job_name,
            MediaFormat='mp3',
            Media={'MediaFileUri': file_path},
            OutputBucketName=self.output_bucket,
            LanguageCode='en-US',
        )
        return response

    def get_transcription_path(self, job_id: str):
        response = self.client.get_transcription_job(TranscriptionJobName=job_id)
        return response['TranscriptionJob'].get('Transcript', {}).get('TranscriptFileUri')


class S3Client:

    def __init__(self):
        self.client = boto3.client('s3')

    def read_file(self, bucket_name: str, filename: str):
        return self.client.get_object(Bucket=bucket_name, Key=filename)['Body'].read()

    def is_file_exists(self, bucket_name: str, filename: str):
        return self.client.get_object(Bucket=bucket_name, Key=filename) is not None
