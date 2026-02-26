from pydantic import BaseModel, Field
from typing import Dict, Any, List


class AgentResult(BaseModel):
    output: Dict[str, Any]
    confidence: float = Field(ge=0.0, le=1.0)
    reasoning: str

class PlannerOutput(BaseModel):
    topic: str

class PlannerLLMResponse(BaseModel):
    output: PlannerOutput
    confidence: float = Field(ge=0.0, le=1.0)
    reasoning: str

class Frame(BaseModel):
    text: str
    image_prompt: str
    duration: int

class ScriptOutput(BaseModel):
    script: List[Frame]

class ScriptLLMResponse(BaseModel):
    output: ScriptOutput
    confidence: float = Field(ge=0.0, le=1.0)
    reasoning: str

class CriticOutput(BaseModel):
    score: float
    issues: List[str]
    hook_score: float
    visual_diversity_score: float
    coherence_score: float

class CriticLLMResponse(BaseModel):
    output: CriticOutput
    confidence: float = Field(ge=0.0, le=1.0)
    reasoning: str

class DebateOutput(BaseModel):
    winner: str
    scores: Dict[str, float]  # script_name -> score
    reason: str

class DebateLLMResponse(BaseModel):
    output: DebateOutput
    confidence: float = Field(ge=0.0, le=1.0)
    reasoning: str

class ResearchOutput(BaseModel):
    key_points: List[str]
    audience_angle: str
    compliance_notes: List[str]


class ResearchLLMResponse(BaseModel):
    output: ResearchOutput
    confidence: float = Field(ge=0.0, le=1.0)
    reasoning: str

class ImagePrompt(BaseModel):
    positive_prompt: str
    negative_prompt: str

class ImageGenLLMResponse(BaseModel):
    output: ImagePrompt
    confidence: float = Field(ge=0.0, le=1.0)
    reasoning: str

class TTSConfig(BaseModel):
    text: str
    voice_tone: str
    speed: float

class TTSLLMResponse(BaseModel):
    output: TTSConfig
    confidence: float = Field(ge=0.0, le=1.0)
    reasoning: str

class SEOOutput(BaseModel):
    title: str
    description: str
    hashtags: List[str]
    tags: List[str]


class SEOLLMResponse(BaseModel):
    output: SEOOutput
    confidence: float = Field(ge=0.0, le=1.0)
    reasoning: str


class ThumbnailOutput(BaseModel):
    thumbnail_prompt: str
    overlay_text: str


class ThumbnailLLMResponse(BaseModel):
    output: ThumbnailOutput
    confidence: float = Field(ge=0.0, le=1.0)
    reasoning: str


class RetentionOutput(BaseModel):
    improved_hook: str


class RetentionLLMResponse(BaseModel):
    output: RetentionOutput
    confidence: float = Field(ge=0.0, le=1.0)
    reasoning: str