docker run -ti -p 8000:8000 -e AWS_PROFILE=zappa -v "$(pwd):/var/codeonion/codeonion-core" -v ~/.aws/:/root/.aws  --rm zappa-docker-image
