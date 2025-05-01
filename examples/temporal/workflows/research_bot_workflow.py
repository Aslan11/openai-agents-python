from temporalio import workflow

from examples.temporal.workflows.research_manager import ResearchManager

@workflow.defn(sandboxed=False)
class ResearchWorkflow:
    @workflow.run
    async def run(self, query: str) -> str:
        return await ResearchManager().run(query)
