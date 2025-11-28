import json

from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.server.tasks import TaskUpdater
from a2a.types import (
    DataPart,
    Part,
    Task,
    TaskState,
    TextPart,
    UnsupportedOperationError,
)
from a2a.utils import (
    new_agent_parts_message,
    new_agent_text_message,
    new_task,
)
from a2a.utils.errors import ServerError
from google.adk.artifacts.in_memory_artifact_service import InMemoryArtifactService
from google.adk.memory.in_memory_memory_service import InMemoryMemoryService
from google.adk.runners import Runner
from google.adk.sessions.in_memory_session_service import InMemorySessionService
from google.genai.types import Content

from gemini_agent import GeminiAgent


class ReimbursementAgentExecutor(AgentExecutor):
    """Reimbursement AgentExecutor."""
    _runner: Runner

    def __init__(
        self,
    ):
        self._agent = GeminiAgent()
        self._runner = Runner(
            app_name=self._agent.name,
            agent=self._agent,
            session_service=InMemorySessionService(),
            artifact_service=InMemoryArtifactService(),
            memory_service=InMemoryMemoryService(),
        )
        self._user_id = "remote_agent"


    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        query = context.get_user_input()
        task = context.current_task

        if not task:
            if not context.message:
                return
            task = new_task(context.message)
            await event_queue.enqueue_event(task)

        updater = TaskUpdater(event_queue, task.id, task.context_id)
        session_id = task.context_id

        session = await self._runner.session_service.get_session(
            app_name=self._agent.name,
            user_id=self._user_id,
            session_id=session_id,
        )
        if session is None:
            session = await self._runner.session_service.create_session(
                app_name=self._agent.name,
                user_id=self._user_id,
                state={},
                session_id=session_id,
            )

        content = Content(role="user", parts=[{"text": query}])

        await updater.start_work()

        try:
            async for event in self._runner.run_async(
                user_id=self._user_id, session_id=session.id, new_message=content
            ):
                        is_task_complete = event.is_final_response()
                        artifacts = None
                        print(f"Received event from agent runner: {event}")
                        if not is_task_complete:
                            await updater.update_status(
                                TaskState.working,
                                new_agent_text_message(
                                    event['updates'], task.context_id, task.id
                                ),
                            )
                            continue
                        print("Task is complete.")
                        # If the response is a dictionary, assume its a form
                        if isinstance(event['content'], dict):
                            # Verify it is a valid form
                            if (
                                'response' in event['content']
                                and 'result' in event['content']['response']
                            ):
                                data = json.loads(event['content']['response']['result'])
                                print(f"Extracted form result data: {data}")
                                await updater.update_status(
                                    TaskState.input_required,
                                    new_agent_parts_message(
                                        [Part(root=DataPart(data=data))],
                                        task.context_id,
                                        task.id,
                                    ),
                                    final=True,
                                )
                                continue
                            await updater.update_status(
                                TaskState.failed,
                                new_agent_text_message(
                                    'Reaching an unexpected state',
                                    task.context_id,
                                    task.id,
                                ),
                                final=True,
                            )
                            break
                        # Emit the appropriate events
                        await updater.add_artifact(
                            [Part(root=TextPart(text=event['content']))], name='form'
                        )
                        await updater.complete()
                        break
        except Exception as e:
            await updater.failed(message=new_agent_text_message(f"Task failed with error: {e}"))

    async def cancel(
        self, request: RequestContext, event_queue: EventQueue
    ) -> Task | None:
        raise ServerError(error=UnsupportedOperationError())
