import os

from fastapi import APIRouter

from clients import TranscribeClient, S3Client
from service import InsightService
from util import Cache
from schemas import InsightsRequestSchema, InsightsResponseSchema


TRANSCRIPTION_BUCKET = os.environ.get("TRANSCRIPTION_BUCKET", "test-bucket")
router = APIRouter(prefix="/insights")

cache = Cache()


@router.post("/")
def retrieve_insights(data: InsightsRequestSchema) -> InsightsResponseSchema:
    input_phrases = data.trackers
    file_path = data.interaction_url

    service = InsightService(
        transcribe_client=TranscribeClient(TRANSCRIPTION_BUCKET),
        s3_client=S3Client(),
        cache=cache,
    )

    job_name = service.transcribe_audio_file(file_path=file_path)
    insights = InsightsResponseSchema()
    if service.is_transcription_ready(job_name):
        transcriptions = service.get_transcriptions(job_name, TRANSCRIPTION_BUCKET)
        insights = service.get_insights(transcriptions[0], input_phrases)

    return insights
