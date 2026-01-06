from datetime import datetime
from fastapi import APIRouter, Depends,HTTPException,status
from database.database import (
    get_questions_collection,
    get_assessment_results_collection,
)
from services.auth import get_current_user
from models.Assesment import AssessmentResult

router = APIRouter(
    tags=["Asses"]
)

@router.post("/assess")
async def assess(
    payload: dict,
    user=Depends(get_current_user),
    questions=Depends(get_questions_collection),
    results=Depends(get_assessment_results_collection),
):
    answers = payload.get("answers", [])

    if not answers:
        return {
            "message": "No answers submitted",
            "score": 0,
            "percentage": 0,
            "risk_level": "Critical",
            "answers": []
        }

    user_id = str(user["_id"])
    score = 0
    answer_docs = []

    for ans in answers:
        q = await questions.find_one({"id": ans["questionId"]})
        if not q:
            continue

        opt = next(
            (o for o in q["options"] if o["option_key"] == ans["selectedOption"]),
            None
        )
        if not opt:
            continue

        score += opt["score"]

        answer_docs.append({
            "questionId": ans["questionId"],
            "selectedOption": ans["selectedOption"],
            "pointsAwarded": opt["score"]
        })

    max_score = len(answers) * 3
    percentage = round((score / max_score) * 100, 2)

    risk_level = (
        "Critical" if percentage < 40
        else "Moderate" if percentage < 70
        else "Secure"
    )
    result = {
    "user": user_id,
    "score": score,
    "total_questions": len(answers),
    "max_possible_score": max_score,
    "percentage": percentage,
    "risk_level": risk_level,
    "answers": answer_docs,
    "createdAt": datetime.utcnow(),
    "updatedAt": datetime.utcnow(),
    }
    await results.insert_one(result)
    result["_id"] = str(result["_id"])
    return result

@router.get("/assess/result")
async def get_assessment_results(
    user=Depends(get_current_user),
    results=Depends(get_assessment_results_collection),
):
    user_id = str(user["_id"])

    cursor = results.find(
        {"user": user_id},
        {"_id": 0}
    ).sort("createdAt", -1)

    data = await cursor.to_list(length=1000)

    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No assessment results found"
        )

    return data