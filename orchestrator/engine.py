import asyncio
from datetime import datetime


class Orchestrator:
    def __init__(self, max_retries=2):
        self.agents = {}
        self.dependencies = {}
        self.max_retries = max_retries

    def register(self, name, agent, depends_on=None):
        self.agents[name] = agent
        self.dependencies[name] = depends_on or []
        print(f"[REGISTER] Agent '{name}' registered with deps {self.dependencies[name]}")

    async def run(self, memory):
        completed = set()
        cycle = 0

        print("\n🚀 Starting Orchestration\n")

        while len(completed) < len(self.agents):
            cycle += 1
            print(f"\n🔄 Cycle {cycle} | Completed: {list(completed)}")

            runnable = []

            for name in self.agents:
                if name in completed:
                    continue

                if all(dep in completed for dep in self.dependencies[name]):
                    runnable.append(name)

            if not runnable:
                print("⚠️  No runnable agents found. Possible deadlock.")
                break

            print(f"▶️ Runnable agents: {runnable}")

            tasks = [
                self._run_agent(name, memory)
                for name in runnable
            ]

            results = await asyncio.gather(*tasks)

            for name, status in results:
                if status == "completed":
                    print(f"✅ Agent '{name}' completed.")
                    completed.add(name)

                elif status == "failed":
                    print(f"❌ Agent '{name}' failed permanently.")
                    # Do NOT mark completed
                    # This prevents downstream agents from running
                
                elif status == "retry_script":
                    print(f"🔁 Regeneration triggered by '{name}'. Resetting dependent agents.")
                    script_name = name.replace("critic_", "")
                    completed.discard(script_name)
                    completed.discard(name)
                

        print("\n🏁 Orchestration Finished\n")
        return memory.dump()

    async def _run_agent(self, name, memory):
        agent = self.agents[name]
        retries = 0

        print(f"\n🧠 Running agent: {name}")

        while retries <= self.max_retries:

            print(f"   Attempt {retries + 1} for '{name}'")

            result = await agent.execute(memory.dump(), memory)

            print(f"   → Confidence: {result.confidence}")

            if result.confidence < 0.5:
                retries += 1
                print(f"   ⚠️ Low confidence. Retrying...")
                continue

            memory.write(name, result.model_dump())
            print(f"   💾 Stored result for '{name}'")

            if name.startswith("critic"):
                approved = result.output.get("approved", False)
                print(f"   🔎 Critic approval: {approved}")

                if not approved:
                    print("   ❌ Script rejected.")
                    print(f"   {result.output.get("issues", "")}")
                    return name, "retry_script"

            return name, "completed"

        print(f"   ❌ Max retries exceeded for '{name}'. Marking as failed.")
        return name, "failed"