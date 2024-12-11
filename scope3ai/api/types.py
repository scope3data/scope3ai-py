from pydantic import BaseModel, Field
from typing import Optional, List
from uuid import UUID
from enum import Enum
from datetime import datetime, timezone


class Task(str, Enum):
    TEXT_GENERATION = "text-generation"
    CHAT = "chat"
    TEXT_EMBEDDING = "text-embedding"
    TEXT_CLASSIFICATION = "text-classification"
    SENTIMENT_ANALYSIS = "sentiment-analysis"
    NAMED_ENTITY_RECOGNITION = "named-entity-recognition"
    QUESTION_ANSWERING = "question-answering"
    SUMMARIZATION = "summarization"
    TRANSLATION = "translation"
    IMAGE_CLASSIFICATION = "image-classification"
    OBJECT_DETECTION = "object-detection"
    IMAGE_SEGMENTATION = "image-segmentation"
    IMAGE_GENERATION = "image-generation"
    IMAGE_TO_TEXT = "image-to-text"
    TEXT_TO_IMAGE = "text-to-image"
    STYLE_TRANSFER = "style-transfer"
    FACE_DETECTION = "face-detection"
    FACIAL_RECOGNITION = "facial-recognition"
    SPEECH_TO_TEXT = "speech-to-text"
    TEXT_TO_SPEECH = "text-to-speech"
    SPEAKER_IDENTIFICATION = "speaker-identification"
    AUDIO_CLASSIFICATION = "audio-classification"
    MUSIC_GENERATION = "music-generation"
    MULTIMODAL_EMBEDDING = "multimodal-embedding"
    MULTIMODAL_GENERATION = "multimodal-generation"
    VISUAL_QUESTION_ANSWERING = "visual-question-answering"
    RECOMMENDATION_SYSTEM = "recommendation-system"
    REINFORCEMENT_LEARNING = "reinforcement-learning"
    ANOMALY_DETECTION = "anomaly-detection"
    TIME_SERIES_FORECASTING = "time-series-forecasting"
    CLUSTERING = "clustering"


class DataType(str, Enum):
    FP8 = "fp8"
    FP16 = "fp16"
    FP32 = "fp32"
    INT1 = "int1"
    INT2 = "int2"
    INT4 = "int4"
    INT8 = "int8"
    INT16 = "int16"


class CloudProvider(str, Enum):
    AWS = "aws"
    AZURE = "azure"
    GCP = "gcp"
    ORACLE = "oracle"
    IBM = "ibm"


class ManagedServiceProvider(str, Enum):
    AWS_BEDROCK = "aws-bedrock"
    AZURE_ML = "azure-ml"
    GOOGLE_VERTEX = "google-vertex"
    IBM_WATSON = "ibm-watson"
    HUGGING_FACE = "hugging-face"


class Gpu(BaseModel):
    """Configuration for GPU hardware"""

    name: Optional[str] = Field(None, description="GPU name (e.g., 'NVIDIA A100 40GB')")
    id: Optional[str] = Field(None, description="GPU identifier (e.g., 'a100_40gb')")
    max_power_w: Optional[float] = Field(
        None, description="Maximum power consumption in watts"
    )
    embodied_emissions_kgco2e: Optional[float] = None
    embodied_water_mlh2o: Optional[float] = None
    performance_ratio_to_h200: Optional[float] = None


class Node(BaseModel):
    """Configuration for compute node"""

    id: Optional[str] = None
    cloud_provider: Optional[CloudProvider] = Field(
        None, description="Cloud provider (e.g., 'aws')"
    )
    cloud_instance_id: Optional[str] = Field(
        None, description="Cloud instance type (e.g., 'a2-highgpu-1g')"
    )
    managed_service: Optional[ManagedServiceProvider] = None
    gpu: Optional[Gpu] = None
    gpu_count: Optional[int] = Field(None, ge=0, le=10000)
    cpu_count: Optional[int] = Field(None, ge=1, le=10000)
    idle_power_w_ex_gpu: Optional[float] = Field(None, ge=0, le=10000)
    average_utilization_rate: Optional[float] = Field(None, ge=0, le=1)
    embodied_emissions_kgco2e_ex_gpu: Optional[float] = Field(None, ge=0, le=100000)
    embodied_water_l_ex_gpu: Optional[float] = Field(None, ge=0, le=100000)
    use_life_years: Optional[float] = Field(None, ge=1, le=30)


class Model(BaseModel):
    """Configuration for AI model"""

    id: str = Field(..., description="Model identifier")
    name: Optional[str] = None
    family: Optional[str] = None
    hugging_face_path: Optional[str] = None
    benchmark_model_id: Optional[str] = None
    total_params_billions: Optional[float] = None
    number_of_experts: Optional[int] = None
    params_per_expert_billions: Optional[float] = None
    tensor_parallelism: Optional[int] = None
    datatype: Optional[DataType] = None
    task: Optional[Task] = None
    training_usage_energy_kwh: Optional[float] = None
    training_usage_emissions_kgco2e: Optional[float] = None
    training_usage_water_l: Optional[float] = None
    training_embodied_emissions_kgco2e: Optional[float] = None
    training_embodied_water_l: Optional[float] = None
    estimated_use_life_days: Optional[float] = None
    estimated_requests_per_day: Optional[float] = None
    fine_tuned_from_model_id: Optional[str] = None


class ImageDimensions(BaseModel):
    """Image dimensions specification"""

    dimensions: str = Field(..., pattern=r"^(\d{1,4})x(\d{1,4})$")


class LocationConfig(BaseModel):
    """Geographic location configuration"""

    cloud_region: Optional[str] = Field(
        None, description="Cloud region (e.g., 'us-east-1')"
    )
    country: Optional[str] = Field(
        None,
        pattern="^[A-Z]{2}$",
        min_length=2,
        max_length=2,
        description="Two-letter country code (e.g., 'US')",
    )
    region: Optional[str] = Field(
        None,
        pattern="^[A-Z]{2}$",
        min_length=2,
        max_length=2,
        description="Two-letter region code (e.g., 'VA')",
    )


class ImpactRequestRow(BaseModel):
    """Complete input for an impact request"""

    model: Model
    location: Optional[LocationConfig] = None
    node: Optional[Node] = None
    utc_timestamp: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="UTC timestamp for the request",
    )
    # Context of the request
    session_id: Optional[UUID] = None
    request_id: Optional[UUID] = None
    client_id: Optional[str] = None
    project_id: Optional[str] = None
    application_id: Optional[str] = None

    # Metrics about the model usage
    task: Optional[Task] = None
    input_tokens: Optional[int] = Field(None, ge=0, le=100000000)
    output_tokens: Optional[int] = Field(None, ge=0, le=100000000)
    input_audio_seconds: Optional[int] = Field(None, ge=0, le=100000)
    input_images: Optional[List[ImageDimensions]] = Field(None, max_items=100)
    input_steps: Optional[int] = Field(None, ge=1, le=10000)
    output_images: Optional[List[ImageDimensions]] = Field(None, max_items=100)
    output_video_frames: Optional[int] = Field(None, ge=0, le=100000000)
    output_video_resolution: Optional[int] = None


class ImpactMetrics(BaseModel):
    """Impact metrics for the model usage"""

    usage_energy_wh: Optional[float] = Field(0, ge=0, le=100000000)
    usage_emissions_gco2e: Optional[float] = Field(0, ge=0, le=100000000)
    usage_water_ml: Optional[float] = Field(0, ge=0, le=100000000)
    embodied_emissions_gco2e: Optional[float] = Field(0, ge=0, le=100000000)
    embodied_water_ml: Optional[float] = Field(0, ge=0, le=100000000)
    errors: Optional[List[str]] = None

    def __add__(self, other: "ImpactMetrics") -> "ImpactMetrics":
        if not isinstance(other, ImpactMetrics):
            raise ValueError(
                "Can only add ImpactMetrics with another ImpactMetrics instance"
            )

        errors = (self.errors or []) + (other.errors or [])
        if len(errors) == 0:
            errors = None

        return ImpactMetrics(
            usage_energy_wh=(self.usage_energy_wh or 0) + (other.usage_energy_wh or 0),
            usage_emissions_gco2e=(self.usage_emissions_gco2e or 0)
            + (other.usage_emissions_gco2e or 0),
            usage_water_ml=(self.usage_water_ml or 0) + (other.usage_water_ml or 0),
            embodied_emissions_gco2e=(self.embodied_emissions_gco2e or 0)
            + (other.embodied_emissions_gco2e or 0),
            embodied_water_ml=(self.embodied_water_ml or 0)
            + (other.embodied_water_ml or 0),
            errors=errors,
        )


class ImpactResponseRowError(BaseModel):
    """Error response from the API"""

    message: str


class ImpactResponseRow(BaseModel):
    """Single row of impact data from the API response"""

    fine_tuning_impact: Optional[ImpactMetrics] = None
    inference_impact: Optional[ImpactMetrics] = None
    training_impact: Optional[ImpactMetrics] = None
    total_impact: ImpactMetrics
    error: Optional[ImpactResponseRowError] = None


class ImpactResponse(BaseModel):
    """Complete response from the impact API"""

    has_errors: bool
    rows: List[ImpactResponseRow]


class ImpactRequest(BaseModel):
    """Final request structure for the API"""

    rows: List[ImpactRequestRow] = Field(..., max_items=1000)


class Scope3AIContext(BaseModel):
    request: ImpactRequestRow | None = Field(
        None,
        description="The impact request information. Contains `trace_id` and `record_id`",
    )
    impact: ImpactResponseRow | None = Field(
        None,
        description="The impact response if `include_impact_response` is set to True",
    )


class ModelFamily(str, Enum):
    CLAUDE = "claude"
    GPT = "gpt"
    DALL_E = "dall-e"
    WHISPER = "whisper"
    GEMINI = "gemini"
    PALM = "palm"
    BERT = "bert"
    T5 = "t5"
    LLAMA = "llama"
    OPT = "opt"
    GALACTICA = "galactica"
    PHI = "phi"
    STABLE_DIFFUSION = "stable-diffusion"
    STABLE_LM = "stable-lm"
    MISTRAL = "mistral"
    MIXTRAL = "mixtral"
    COMMAND = "command"
    EMBED = "embed"
    FALCON = "falcon"
    MPT = "mpt"
    PYTHIA = "pythia"
    DOLLY = "dolly"
    BLOOM = "bloom"
    ROBERTA = "roberta"
    GPT_NEO = "gpt-neo"
    GPT_J = "gpt-j"


class ModelResponse(BaseModel):
    models: List[Model]


class NodeService(str, Enum):
    AWS_BEDROCK = "aws-bedrock"
    AZURE_ML = "azure-ml"
    GOOGLE_VERTEX = "google-vertex"
    IBM_WATSON = "ibm-watson"
    HUGGING_FACE = "hugging-face"


class NodeCloud(str, Enum):
    AWS = "aws"
    AZURE = "azure"
    GCP = "gcp"
    ORACLE = "oracle"
    IBM = "ibm"


class NodeResponse(BaseModel):
    nodes: List[Node]


class GpuResponse(BaseModel):
    gpus: List[Gpu]
