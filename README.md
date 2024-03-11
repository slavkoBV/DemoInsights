### **Insights API**

This test project allows to transcribe mp3 file and check whether
it contains tracked phrases (It uses AWS Transcribe service)

To run it you have to have AWS account

#### To run it locally:
1. Create `.env` file by example `env.example` and specify your AWS credentials.
2. `make build`
3. `make run`
4. Check swagger docs http://127.0.0.1:8002/docs
5. Enjoy!


#### To run tests:
1. `make test`