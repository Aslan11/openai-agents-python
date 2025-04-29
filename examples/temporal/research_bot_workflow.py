from temporalio import workflow

from examples.temporal.research_manager import ResearchManager

@workflow.defn(sandboxed=False)
class ResearchWorkflow:
    @workflow.run
    async def run(self, query: str) -> None:
        await ResearchManager().run(query)
