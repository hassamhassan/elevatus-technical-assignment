import uuid
from typing import List, Dict

from fastapi import APIRouter, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorCollection

from database.db import database
from schemas.candidates_schema import (
    CandidateRegisterRequestSchema,
    CandidateRegisterResponseSchema,
    UpdateCandidateRequestSchema,
    SearchParametersSchema,
)
from utils.constants import (
    NOT_FOUND,
    EMAIL_ALREADY_EXIST,
    CANDIDATE_REGISTERED_SUCCESSFULLY,
    RECORD_DELETED_SUCCESSFULLY,
    SUCCESS
)
from views.candidates import add_data_to_csv, add_data_filters

candidate_router = APIRouter(
    prefix="/candidate",
    tags=["candidate"],
    responses={404: {"description": NOT_FOUND}},
)


@candidate_router.post("/create")
async def register_new_candidate(candidate: CandidateRegisterRequestSchema) -> Dict[str, str]:
    """
    Register a new candidate.

    Args:
        candidate: CandidateRegisterRequestSchema - The candidate data to be registered.

    Returns:
        Dict[str, str]: A dictionary with a message indicating the registration status.
    """
    candidates_collection: AsyncIOMotorCollection = await database.get_collection("candidates")

    candidate_check: Dict = await candidates_collection.find_one({"email": candidate.email})
    if candidate_check:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=EMAIL_ALREADY_EXIST
        )

    candidate_data: Dict = candidate.model_dump()
    candidate_uuid = str(uuid.uuid4())
    candidate_data["uuid"] = candidate_uuid
    await candidates_collection.insert_one(candidate_data)

    return {"message": CANDIDATE_REGISTERED_SUCCESSFULLY, "uuid": candidate_uuid}


@candidate_router.get("/get/{candidate_id}", response_model=CandidateRegisterResponseSchema)
async def get_candidate(candidate_id: str) -> CandidateRegisterResponseSchema:
    """
    Retrieve details of a candidate.

    Args:
        candidate_id: str - The unique identifier of the candidate.

    Returns:
        CandidateRegisterResponseSchema: Details of the candidate as per schema.
    """
    candidates_collection: AsyncIOMotorCollection = await database.get_collection("candidates")

    candidate: Dict = await candidates_collection.find_one({"uuid": candidate_id})

    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=NOT_FOUND
        )

    return CandidateRegisterResponseSchema(**candidate)


@candidate_router.put("/update/{candidate_id}", response_model=CandidateRegisterResponseSchema)
async def update_candidate_data(
        candidate_id: str, candidate: UpdateCandidateRequestSchema
) -> CandidateRegisterResponseSchema:
    """
    Update candidate data.

    Args:
        candidate_id: str - The unique identifier of the candidate.
        candidate: UpdateCandidateRequestSchema - The updated candidate data.

    Returns:
        CandidateRegisterResponseSchema: Updated details of the candidate as per schema.
    """
    candidates_collection: AsyncIOMotorCollection = await database.get_collection("candidates")

    candidate_check: Dict = await candidates_collection.find_one({"uuid": candidate_id})
    if not candidate_check:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=NOT_FOUND
        )

    update_fields: Dict = candidate.model_dump(exclude_unset=True)
    if update_fields:
        update_query: Dict = {"$set": update_fields}
        await candidates_collection.update_one({"uuid": candidate_id}, update_query)

    return await candidates_collection.find_one({"uuid": candidate_id})


@candidate_router.delete("/delete/{candidate_id}")
async def delete_candidate(candidate_id: str) -> Dict[str, str]:
    """
    Delete candidate.

    Args:
        candidate_id: str - The unique identifier of the candidate to be deleted.

    Returns:
        Dict[str, str]: A dictionary with a message indicating the deletion status.
    """
    candidates_collection: AsyncIOMotorCollection = await database.get_collection("candidates")

    candidate = await candidates_collection.find_one({"uuid": candidate_id})
    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=NOT_FOUND
        )

    await candidates_collection.delete_one({"uuid": candidate_id})

    return {"message": RECORD_DELETED_SUCCESSFULLY}


@candidate_router.post("/all-candidates", response_model=List[CandidateRegisterResponseSchema])
async def get_all_candidates(candidate_filter: SearchParametersSchema) -> List[CandidateRegisterResponseSchema]:
    """
    Retrieve all candidates based on filtering criteria.

    Args:
        candidate_filter: SearchParametersSchema - Filtering criteria for candidates.

    Returns:
        List[CandidateRegisterResponseSchema]: A list of candidate details as per schema.
    """
    candidates_collection: AsyncIOMotorCollection = await database.get_collection("candidates")

    filters: Dict = await add_data_filters(candidate_filter)
    candidates: List = await candidates_collection.find(filters).to_list(length=None)

    if not candidates:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=NOT_FOUND
        )

    return candidates


@candidate_router.get("/generate-csv-report")
async def generate_csv_report() -> Dict[str, str]:
    """
    Generate CSV report of candidates.

    Returns:
        Dict[str, str]: A dictionary with a message indicating the report generation status.
    """
    candidates_collection: AsyncIOMotorCollection = await database.get_collection("candidates")

    candidates: List = await candidates_collection.find({}).to_list(length=None)
    if not candidates:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=NOT_FOUND
        )
    add_data_to_csv(candidates)

    return {"message": SUCCESS}
