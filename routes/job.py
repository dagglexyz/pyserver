from fastapi import APIRouter, Request, Response, status
from fastapi.encoders import jsonable_encoder

# Bacalhau Imports
from bacalhau_sdk.api import submit, results, states
from bacalhau_sdk.config import get_client_id
from bacalhau_apiclient.models.storage_spec import StorageSpec
from bacalhau_apiclient.models.spec import Spec
from bacalhau_apiclient.models.job_spec_language import JobSpecLanguage
from bacalhau_apiclient.models.job_spec_docker import JobSpecDocker
from bacalhau_apiclient.models.publisher_spec import PublisherSpec
from bacalhau_apiclient.models.deal import Deal

router = APIRouter(
    prefix="/bacalhau",
    responses={404: {"message": "Not found"}},
)


@router.post("/submit")
async def signin(request: Request, response: Response):
    try:
        body = await request.json()
        if "jobspecdocker" not in body or "storagespec" not in body:
            raise Exception("Please send valid body.")
        data = dict(
            APIVersion="V1beta1",
            ClientID=get_client_id(),
            Spec=Spec(
                engine="Docker",
                verifier="Noop",
                publisher_spec=PublisherSpec(type="Estuary"),
                inputs=[StorageSpec(**body["storagespec"])],
                docker=JobSpecDocker(**body["jobspecdocker"]),
                language=JobSpecLanguage(job_context=None),
                wasm=None,
                resources=None,
                # timeout=1800,
                outputs=[
                    StorageSpec(
                        storage_source="IPFS",
                        name="outputs",
                        path="/outputs",
                    )
                ],
                # sharding=JobShardingConfig(
                #     batch_size=1,
                #     glob_pattern_base_path="/inputs",
                # ),
                # execution_plan=JobExecutionPlan(shards_total=0),
                deal=Deal(concurrency=1, confidence=0, min_bids=0),
                do_not_track=False,
            ),
        )
        # jsonable_encoder(user)
        result = submit(data)
        return result
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"message": str(e)}


@router.get("/state/{job_id}")
async def get_job(job_id: str, response: Response):
    try:
        if job_id is None:
            raise Exception("Please send a job id.")

        result = states(job_id=job_id)
        return result
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"message": str(e)}


@router.get("/job/{job_id}")
async def get_job(job_id: str, response: Response):
    try:
        if job_id is None:
            raise Exception("Please send a job id.")

        result = results(job_id=job_id)
        return result
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"message": str(e)}
