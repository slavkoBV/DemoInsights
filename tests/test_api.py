import json

import moto


@moto.mock_aws
def test_get_insights_success(client, create_bucket, mocker):
    mock_file_data = json.dumps(
        {
            "results": {
                "transcripts": [
                    {
                        "transcript": "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
                        " Fusce elit augue, facilisis et est nec, ornare dignissim mi."
                    }
                ]
            }
        }
    )
    mocker.patch("clients.S3Client.read_file", return_value=mock_file_data)
    response = client.post(
        "/insights",
        json={
            "interaction_url": "http://test_url1",
            "trackers": ["Lorem ipsum", "et est nec"],
        },
    )
    assert response.json() == {
        "insights": [
            {
                "sentence_index": 0,
                "start_word_index": 0,
                "end_word_index": 2,
                "tracker_value": "Lorem ipsum",
                "transcribe_value": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            },
            {
                "sentence_index": 1,
                "start_word_index": 5,
                "end_word_index": 8,
                "tracker_value": "et est nec",
                "transcribe_value": "Fusce elit augue, facilisis et est nec, ornare dignissim mi.",
            },
        ]
    }


@moto.mock_aws
def test_get_insights_empty(client, create_bucket, mocker):
    mock_file_data = json.dumps(
        {
            "results": {
                "transcripts": [
                    {
                        "transcript": "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
                        " Fusce elit augue, facilisis et est nec, ornare dignissim mi."
                    }
                ]
            }
        }
    )
    mocker.patch("clients.S3Client.read_file", return_value=mock_file_data)
    response = client.post(
        "/insights",
        json={"interaction_url": "http://test_url2", "trackers": ["Value1", "Value2"]},
    )
    assert response.json() == {"insights": []}


def test_get_insights_bad_request(client):
    response = client.post(
        "/insights",
        json={"interaction_url": "http://test_url"},
    )
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "trackers"]
    assert response.json()["detail"][0]["msg"] == "Field required"
