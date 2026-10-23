# RunPod Deployment — Draft Checklist

The repository includes a RunPod Serverless handler and Dockerfile. Deployment is not yet completed.

1. Confirm the competition's required RunPod endpoint type and worker settings.
2. Build the Docker image from this folder and publish it to the team's approved container registry.
3. Create/configure the RunPod endpoint to use that image and verify the handler input/output contract.
4. Keep registry credentials and RunPod keys in the provider's secret settings; do not commit them to this repository.
5. Record the final endpoint name/ID, image tag, test evidence, and any required screenshot here.

This endpoint is for triage jobs. It does not connect to messaging platforms and cannot send messages.
