from fastapi import APIRouter, HTTPException
from ..payloads.payloads import RequestPayload, ResponsePayload
from services.services import GetStudyPlan

router = APIRouter()

@router.post("/generate-study-plan", response_model=ResponsePayload, tags=["Generate study plan with LearnX"])
async def generate_study_plan(request_data: RequestPayload):
    try:
        # Call the service function with the request data
        study_plan = GetStudyPlan.generate_plan(request_data)
        
        # Return the response with the generated study plan
        return {"StudyPlan": study_plan}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# router = APIRouter()

# @router.post("/study-plan")
# def study_plan(payload: RequestPayload):
#     study_plan_service = GetStudyPlan(payload)
#     result = study_plan_service.generate_plan()
#     return {"study_plan": result}
