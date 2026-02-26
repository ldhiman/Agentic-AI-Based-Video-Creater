import asyncio
from pathlib import Path

from orchestrator.engine import Orchestrator
from orchestrator.memory import SharedMemory

from agents.planner_agent import PlannerAgent
from agents.research_agent import ResearchAgent
from agents.script_agent import ScriptAgent
from agents.critic_agent import CriticAgent
from agents.debate_critic_agent import DebateCriticAgent
from agents.retention_agent import RetentionAgent
from agents.seo_agent import SEOAgent
from agents.thumbnail_agent import ThumbnailAgent

from media_pipeline.image_generator import generate_image
from media_pipeline.tts_engine import generate_tts
from media_pipeline.video_renderer import render_video
from media_pipeline.thumbnail_renderer import render_thumbnail

from analytics.performance_tracker import log_video

# Optional
# from uploader.youtube_uploader import upload_video


OUTPUT_DIR = Path("output")
FRAMES_DIR = OUTPUT_DIR / "frames"
AUDIO_FILE = OUTPUT_DIR / "voice.wav"
VIDEO_FILE = OUTPUT_DIR / "final_video.mp4"
THUMBNAIL_FILE = OUTPUT_DIR / "thumbnail.jpg"


async def run_agents():
    memory = SharedMemory()
    orchestrator = Orchestrator()

    # 🧠 Core pipeline
    orchestrator.register("planner", PlannerAgent("planner"))
    orchestrator.register("research", ResearchAgent("research"), depends_on=["planner"])

    NUM_SCRIPTS = 2  # reduce for speed

    for i in range(NUM_SCRIPTS):
        script_name = f"script_{i}"
        critic_name = f"critic_script_{i}"

        orchestrator.register(
            script_name,
            ScriptAgent(script_name),
            depends_on=["research"]
        )

        orchestrator.register(
            critic_name,
            CriticAgent(critic_name),
            depends_on=[script_name]
        )

    orchestrator.register(
        "debate",
        DebateCriticAgent("debate"),
        depends_on=[f"critic_script_{i}" for i in range(NUM_SCRIPTS)]
    )

    # 🚀 Optimization agents
    orchestrator.register(
        "retention",
        RetentionAgent("retention"),
        depends_on=["debate"]
    )

    orchestrator.register(
        "seo",
        SEOAgent("seo"),
        depends_on=["retention"]
    )

    orchestrator.register(
        "thumbnail",
        ThumbnailAgent("thumbnail"),
        depends_on=["retention"]
    )

    await orchestrator.run(memory)
    return memory


def build_media(memory):
    print("\n🎬 Building media pipeline...")

    OUTPUT_DIR.mkdir(exist_ok=True)
    FRAMES_DIR.mkdir(parents=True, exist_ok=True)

    script = memory.read("final_script")["script"]

    image_paths = []

    # 🎨 Generate images
    print("🎨 Generating frame images...")
    for idx, frame in enumerate(script):
        img_path = FRAMES_DIR / f"frame_{idx}.png"
        generate_image(frame["image_prompt"], str(img_path))
        image_paths.append(str(img_path))

    # 🔊 Generate voice
    print("🔊 Generating voice...")
    full_text = " ".join(frame["text"] for frame in script)
    generate_tts(full_text, str(AUDIO_FILE))

    # 🎥 Render video
    print("🎥 Rendering video...")
    render_video(image_paths, str(AUDIO_FILE), str(VIDEO_FILE))

    # 🖼 Render thumbnail
    print("🖼 Rendering thumbnail...")
    thumb_data = memory.read("thumbnail")["output"]

    render_thumbnail(
        image_paths[0],  # first frame as base
        thumb_data["overlay_text"],
        str(THUMBNAIL_FILE)
    )

    print("✅ Media generation complete.")


def upload_and_log(memory):
    seo_data = memory.read("seo")["output"]

    print("\n📊 Logging video metadata...")

    log_video({
        "topic": memory.read("planner")["output"]["topic"],
        "title": seo_data["title"],
        "video_path": str(VIDEO_FILE),
        "thumbnail_path": str(THUMBNAIL_FILE)
    })

    # Uncomment when OAuth ready
    # print("📤 Uploading to YouTube...")
    # upload_video(
    #     str(VIDEO_FILE),
    #     seo_data["title"],
    #     seo_data["description"],
    #     seo_data["tags"]
    # )

    print("🚀 Autonomous cycle complete.")


async def main():
    memory = await run_agents()
    build_media(memory)
    upload_and_log(memory)


if __name__ == "__main__":
    asyncio.run(main())