from fastapi import (

    APIRouter,

    Depends,

    HTTPException,

    status

)

from sqlalchemy.orm import (

    Session

)

from app.db.session import (

    get_db

)

from app.schemas.chat_schema import (

    ChatRequest,

    ChatResponse

)

from app.services.chat_service import (

    ChatService

)


router = APIRouter(

    prefix="/chat",

    tags=["Chat"]

)


def get_chat_service(

    db: Session = Depends(

        get_db

    )

):

    return ChatService(

        db

    )


@router.post(

    "/message",

    response_model=ChatResponse,

    status_code=status.HTTP_200_OK

)

async def chat(

    payload: ChatRequest,

    chat_service: ChatService = Depends(

        get_chat_service

    )

):

    try:

        result = await (

            chat_service

            .process_message(

                payload

            )

        )

        return result

    except Exception:

        raise HTTPException(

            status_code=

            status.HTTP_500_INTERNAL_SERVER_ERROR,

            detail=

            "Unable to process chat request"

        )