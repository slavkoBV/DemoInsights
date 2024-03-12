### **Insights API**

This test project allows to transcribe mp3 file and check whether
it contains tracked phrases (It uses AWS Transcribe service)

To run it, you have to have AWS account

#### To run it locally:
1. Create `.env` file by example `env.example` and specify your AWS credentials.
2. `make build`
3. `make run`
4. Check swagger docs http://127.0.0.1:8002/docs
5. Enjoy!


#### To run tests:
1. `make test`


### To deploy on AWS ECS Fargate
1. Build docker image locally `make build`
#### Note. In case you use MacOS, build docker image with next command:
`docker buildx build --platform linux/amd64 -t demoinsights-app:latest --load .`
2. Specify your AWS Account ID and preferred name of the repo in `/DemoInsights/cloudformation/ecr/cf-ecr.params.json`
3. You should be login into AWS CLI
4. Create AWS ECR repo `sh cf-ecr.deploy.sh` from `/DemoInsights/cloudformation/ecr`
5. Add tag `docker tag demoinsights-app:latest [AWSAccountID].dkr.ecr.[AWSRegion].amazonaws.com/[RepoName]:latest`
6. Login: 
`aws ecr get-login-password --region [AwsRegion] | docker login --username AWS --password-stdin [AwsAccountId].dkr.ecr.[AwsRegion].amazonaws.com`
7. Push image to the repo:
`docker push <AWSAccountID>.dkr.ecr.<AWSRegion>.amazonaws.com/<RepoName>:latest`
8. Specify your AWS Account ID, available subnet and name of the S3 Bucket to create (name should be unique across AWS)
9. Deploy APP to ECS/Fargate `sh cf-ecs.deploy.sh` and wait until all resources will be ready
10. Run swagger page [TaskPublicIP]:8000/docs where you can try API