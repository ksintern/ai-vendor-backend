from collections import (
    defaultdict,
    deque
)

from threading import (
    Lock
)

import time


class SessionManager:

    MAX_MESSAGES = 6

    MAX_CONTEXT_CHARS = 800

    SESSION_TTL = 3600

    _lock = Lock()

    _sessions = defaultdict(

        lambda: {

            "messages": deque(
                maxlen=
                SessionManager.MAX_MESSAGES
            ),

            "updated_at":
            time.time()

        }

    )

    _filters = defaultdict(

        dict

    )

    @classmethod
    def _touch(

        cls,

        session_id:str

    ):

        if session_id in cls._sessions:

            cls._sessions[
                session_id
            ][
                "updated_at"
            ] = time.time()

    @classmethod
    def _cleanup(

        cls

    ):

        now = time.time()

        expired = []

        for session_id,data in (

            cls._sessions.items()

        ):

            if (

                now
                -
                data[
                    "updated_at"
                ]

                >

                cls.SESSION_TTL

            ):

                expired.append(

                    session_id

                )

        for session_id in expired:

            cls.clear(

                session_id

            )

    @classmethod
    def add_message(

        cls,

        session_id:str,

        role:str,

        content:str

    ):

        if not content:

            return

        cleaned = (

            content
            .strip()

        )

        if not cleaned:

            return

        with cls._lock:

            cls._cleanup()

            cls._touch(

                session_id

            )

            cls._sessions[
                session_id
            ][
                "messages"
            ].append(

                {

                    "role":
                    role,

                    "content":
                    cleaned

                }

            )

    @classmethod
    def get_context(

        cls,

        session_id:str,

        limit:int=4

    ):

        with cls._lock:

            cls._cleanup()

            cls._touch(

                session_id

            )

            messages = list(

                cls._sessions
                .get(

                    session_id,

                    {}

                )
                .get(

                    "messages",

                    []

                )

            )[-limit:]

        history=[]

        chars=0

        for msg in reversed(

            messages

        ):

            line=(

                f"{msg['role']}: "

                f"{msg['content']}"

            )

            size=len(

                line

            )

            if (

                chars
                +
                size

                >

                cls.MAX_CONTEXT_CHARS

            ):

                continue

            history.insert(

                0,

                line

            )

            chars += size

        return "\n".join(

            history

        )

    @classmethod
    def set_filters(

        cls,

        session_id:str,

        filters:dict

    ):

        with cls._lock:

            existing = (

                cls._filters.get(

                    session_id,

                    {}

                )

            )

            merged = {

                **existing,

                **{

                    k:v

                    for k,v

                    in filters.items()

                    if v is not None

                }

            }

            cls._filters[
                session_id
            ] = merged

    @classmethod
    def get_filters(

        cls,

        session_id:str

    ):

        return dict(

            cls._filters.get(

                session_id,

                {}

            )

        )

    @classmethod
    def clear(

        cls,

        session_id:str

    ):

        cls._sessions.pop(

            session_id,

            None

        )

        cls._filters.pop(

            session_id,

            None

        )