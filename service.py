import json
from uuid import uuid4

import spacy
from spacy.matcher import PhraseMatcher

from clients import TranscribeClient, S3Client
from schemas import InsightResponseSchema, InsightsResponseSchema
from util import Cache


NLP = spacy.load("en_core_web_sm")


class InsightService:

    def __init__(self, transcribe_client: TranscribeClient, s3_client: S3Client, cache: Cache) -> None:
        self.transcribe_client = transcribe_client
        self.s3_client = s3_client
        self.cache = cache

    def transcribe_audio_file(self, file_path: str) -> str:
        job_name = self.cache.get(file_path)
        if not job_name:
            job_name = str(uuid4())
            self.transcribe_client.transcribe_audio(job_name, file_path)
            self.cache.set(file_path, job_name)
        return job_name

    def is_transcription_ready(self, job_name: str) -> bool:
        path = None
        while path is None:
            path = self.transcribe_client.get_transcription_path(job_name)
        return path is not None

    def get_transcriptions(self, job_name: str, bucket_name: str):
        file_name = f'{job_name}.json'
        file_data = self.s3_client.read_file(bucket_name=bucket_name, filename=file_name)
        data = json.loads(file_data)
        return [item['transcript'] for item in data['results']['transcripts']]

    @staticmethod
    def get_insights(text: str, trackers: list[str]) -> InsightsResponseSchema:
        matcher = PhraseMatcher(NLP.vocab)
        patterns = [NLP.make_doc(text) for text in trackers]
        matcher.add("Insights", patterns)

        doc = NLP(text)
        sentences = {idx: sentence.text for idx, sentence in enumerate(doc.sents)}

        result = InsightsResponseSchema()
        for sentence_index, sentence in sentences.items():
            doc = NLP(sentence)
            matches = matcher(doc)
            if matches:
                for match_id, start, end in matches:
                    result.insights.append(
                        InsightResponseSchema(
                            sentence_index=sentence_index,
                            start_word_index=start,
                            end_word_index=end,
                            tracker_value=str(doc[start:end]),
                            transcribe_value=sentence,
                        )
                    )
        return result
