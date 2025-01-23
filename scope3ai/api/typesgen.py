# generated by datamodel-codegen:
#   filename:  aiapi.yaml
#   timestamp: 2025-01-21T22:57:07+00:00

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, ConfigDict, Field, RootModel
from typing_extensions import Annotated


class StatusResponse(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    ready: bool
    reason: Optional[str] = None


class NodeCreateRequest(BaseModel):
    """
    Create a new node.
    Note on permissions:
    - cloud_instance_id and managed_service_id can only be set by admins or users who own those resources
    - Custom nodes are visible only to their owners
    - Global nodes are visible to all users
    - Admins can see and manage all nodes

    """

    id: Annotated[
        str,
        Field(
            examples=["my-custom-node-1"],
            max_length=64,
            min_length=3,
            pattern="^[a-z0-9-]+$",
        ),
    ]
    cloud_id: Annotated[Optional[str], Field(examples=["aws"])] = None
    cloud_instance_id: Annotated[Optional[str], Field(examples=["a2-highgpu-1g"])] = (
        None
    )
    managed_service_id: Annotated[Optional[str], Field(examples=["aws-bedrock"])] = None
    gpu_id: Annotated[str, Field(examples=["a100_40gb"])]
    gpu_count: Annotated[int, Field(examples=[8], ge=0, le=10000)]
    cpu_count: Annotated[int, Field(examples=[2], ge=1, le=10000)]
    idle_power_w_ex_gpu: Annotated[
        Optional[float], Field(examples=[100], ge=0.0, le=10000.0)
    ] = None
    average_utilization_rate: Annotated[
        Optional[float], Field(examples=[0.8], ge=0.0, le=1.0)
    ] = None
    embodied_emissions_kgco2e_ex_gpu: Annotated[
        Optional[float], Field(examples=[2500], ge=0.0, le=100000.0)
    ] = None
    embodied_water_l_ex_gpu: Annotated[
        Optional[float], Field(examples=[2500], ge=0.0, le=100000.0)
    ] = None
    use_life_years: Annotated[Optional[float], Field(examples=[5], ge=1.0, le=30.0)] = (
        None
    )


class NodeUpdateRequest(BaseModel):
    """
    Update an existing node.
    - Id can not be updated
    Note on permissions:
    - cloud_instance_id and managed_service_id can only be set by admins or users who own those resources
    - Custom nodes are visible only to their owners
    - Global nodes are visible to all users
    - Admins can see and manage all nodes

    """

    cloud_id: Annotated[Optional[str], Field(examples=["aws"])] = None
    cloud_instance_id: Annotated[Optional[str], Field(examples=["a2-highgpu-1g"])] = (
        None
    )
    managed_service_id: Annotated[Optional[str], Field(examples=["aws-bedrock"])] = None
    gpu_id: Annotated[Optional[str], Field(examples=["a100_40gb"])] = None
    gpu_count: Annotated[Optional[int], Field(examples=[8], ge=0, le=10000)] = None
    cpu_count: Annotated[Optional[int], Field(examples=[2], ge=1, le=10000)] = None
    idle_power_w_ex_gpu: Annotated[
        Optional[float], Field(examples=[100], ge=0.0, le=10000.0)
    ] = None
    average_utilization_rate: Annotated[
        Optional[float], Field(examples=[0.8], ge=0.0, le=1.0)
    ] = None
    embodied_emissions_kgco2e_ex_gpu: Annotated[
        Optional[float], Field(examples=[2500], ge=0.0, le=100000.0)
    ] = None
    embodied_water_l_ex_gpu: Annotated[
        Optional[float], Field(examples=[2500], ge=0.0, le=100000.0)
    ] = None
    use_life_years: Annotated[Optional[float], Field(examples=[5], ge=1.0, le=30.0)] = (
        None
    )


class Call(RootModel[List[Union[str, int]]]):
    root: Annotated[
        List[Union[str, int]],
        Field(
            description="Array of function call parameters in this exact order:\n  model_id STRING, model_family STRING, model_name STRING,\n  model_hugging_face_path STRING, request_time TIMESTAMP,\n  node_id STRING, cloud_id STRING, cloud_region STRING,\n  cloud_instance_id STRING, managed_service_id STRING,\n  country STRING, region STRING, task STRING, input_tokens INT64,\n  output_tokens INT64, input_images STRING, output_images STRING,\n  output_video_resolution INT64,\n  output_video_frames INT64, input_audio_seconds INT64, input_steps INT64\n",
            examples=[
                [
                    "gpt-4-turbo",
                    "2024-03-15T10:30:00Z",
                    "us-central1",
                    "US",
                    "CA",
                    "text-generation",
                    100,
                    50,
                    None,
                ]
            ],
            max_length=21,
            min_length=17,
        ),
    ]


class ImpactBigQueryRequest(BaseModel):
    requestId: Annotated[
        str,
        Field(description="Unique identifier for the request", examples=["124ab1c"]),
    ]
    caller: Annotated[
        str,
        Field(
            description="Full resource name of the BigQuery job",
            examples=[
                "//bigquery.googleapis.com/projects/myproject/jobs/myproject:US.bquxjob_5b4c112c_17961fafeaf"
            ],
        ),
    ]
    sessionUser: Annotated[
        str,
        Field(
            description="Email of the user executing the BigQuery query",
            examples=["user@company.com"],
        ),
    ]
    userDefinedContext: Annotated[
        Optional[Dict[str, Any]],
        Field(description="User-defined context from BigQuery"),
    ] = None
    calls: List[Call]


class ImpactBigQueryResponse(BaseModel):
    replies: Annotated[
        List[str],
        Field(
            description="Array of impact metric results", max_length=1000, min_length=0
        ),
    ]
    errorMessage: Optional[str] = None


class ImpactBigQueryError(BaseModel):
    errorMessage: Annotated[
        str,
        Field(
            description="Error message for BigQuery",
            examples=["Invalid request format: missing required field 'calls'"],
        ),
    ]


class ImpactMetrics(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    usage_energy_wh: Annotated[float, Field(examples=[0.13])]
    usage_emissions_gco2e: Annotated[float, Field(examples=[0.81])]
    usage_water_ml: Annotated[float, Field(examples=[1.32])]
    embodied_emissions_gco2e: Annotated[float, Field(examples=[0.81])]
    embodied_water_ml: Annotated[float, Field(examples=[1.32])]


class PredictionStep(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    description: str
    duration_ms: float
    inferences: int


class Details(BaseModel):
    reason: Optional[str] = None
    field: Optional[str] = None


class Error(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    code: Optional[str] = None
    message: str
    details: Optional[Details] = None


class Node(NodeCreateRequest):
    customer_id: Annotated[
        Optional[Any],
        Field(
            description="ID of the customer who owns this node (visible to admins only)"
        ),
    ] = None
    created_at: datetime
    updated_at: datetime
    created_by: Annotated[
        Optional[str],
        Field(description="ID of the user who created the node (admin or owner only)"),
    ] = None


class GPU(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    name: Annotated[Optional[str], Field(examples=["NVIDIA A100 40GB"])] = None
    id: Annotated[str, Field(examples=["a100_40gb"])]
    max_power_w: Annotated[float, Field(examples=[700])]
    embodied_emissions_kgco2e: Annotated[float, Field(examples=[282.1])]
    embodied_water_mlh2o: Annotated[float, Field(examples=[181.1])]
    performance_ratio_to_h200: Annotated[float, Field(examples=[1.5])]
    ols_coefficient_gpu_count: Annotated[float, Field(examples=[11.4])]
    ols_intercept: Annotated[float, Field(examples=[11.4])]


class Image(RootModel[str]):
    root: Annotated[
        str, Field(examples=["1024x1024"], pattern="^(\\d{1,4})x(\\d{1,4})$")
    ]


class Task(str, Enum):
    """
    Common types of AI/ML models and their primary functions:
    - Text-based models for natural language processing
    - Vision models for image analysis and generation
    - Audio models for speech and sound processing
    - Multimodal models that combine different types of inputs/outputs
    - Specialized models for specific use cases

    """

    text_generation = "text-generation"
    chat = "chat"
    text_embedding = "text-embedding"
    text_classification = "text-classification"
    sentiment_analysis = "sentiment-analysis"
    named_entity_recognition = "named-entity-recognition"
    question_answering = "question-answering"
    summarization = "summarization"
    translation = "translation"
    image_classification = "image-classification"
    object_detection = "object-detection"
    image_segmentation = "image-segmentation"
    image_generation = "image-generation"
    image_to_text = "image-to-text"
    text_to_image = "text-to-image"
    style_transfer = "style-transfer"
    face_detection = "face-detection"
    facial_recognition = "facial-recognition"
    speech_to_text = "speech-to-text"
    text_to_speech = "text-to-speech"
    speaker_identification = "speaker-identification"
    audio_classification = "audio-classification"
    music_generation = "music-generation"
    multimodal_embedding = "multimodal-embedding"
    multimodal_generation = "multimodal-generation"
    visual_question_answering = "visual-question-answering"
    recommendation_system = "recommendation-system"
    reinforcement_learning = "reinforcement-learning"
    anomaly_detection = "anomaly-detection"
    time_series_forecasting = "time-series-forecasting"
    clustering = "clustering"


class Family(str, Enum):
    """
    Core AI model families from various organizations:
    - Commercial models from major AI companies
    - Open source model families
    - Research/academic model families
    - Models may appear in multiple categories if they have both commercial and open source variants

    """

    claude = "claude"
    gpt = "gpt"
    dall_e = "dall-e"
    whisper = "whisper"
    gemini = "gemini"
    palm = "palm"
    bert = "bert"
    t5 = "t5"
    llama = "llama"
    opt = "opt"
    galactica = "galactica"
    phi = "phi"
    stable_diffusion = "stable-diffusion"
    stable_lm = "stable-lm"
    mistral = "mistral"
    mixtral = "mixtral"
    command = "command"
    embed = "embed"
    falcon = "falcon"
    mpt = "mpt"
    pythia = "pythia"
    dolly = "dolly"
    bloom = "bloom"
    roberta = "roberta"
    gpt_neo = "gpt-neo"
    gpt_j = "gpt-j"


class DataType(str, Enum):
    fp8 = "fp8"
    fp8_e4m3 = "fp8-e4m3"
    fp8_e5m2 = "fp8-e5m2"
    fp16 = "fp16"
    tf32 = "tf32"
    fp32 = "fp32"
    fp64 = "fp64"
    bfloat8 = "bfloat8"
    bfloat16 = "bfloat16"
    bf16 = "bf16"
    int4 = "int4"
    int8 = "int8"
    int16 = "int16"
    int32 = "int32"
    int64 = "int64"
    uint4 = "uint4"
    uint8 = "uint8"
    uint16 = "uint16"
    uint32 = "uint32"
    uint64 = "uint64"


class CountryCode(RootModel[str]):
    root: Annotated[
        str,
        Field(
            description="Two-letter country code as defined by ISO 3166-1 alpha-2",
            examples=["US"],
            max_length=2,
            min_length=2,
            pattern="^[A-Z]{2}$",
        ),
    ]


class RegionCode(RootModel[str]):
    root: Annotated[
        str,
        Field(
            description="Two-letter region code as defined by ISO 3166-1 alpha-2",
            examples=["NY"],
            max_length=2,
            min_length=2,
            pattern="^[A-Z]{2}$",
        ),
    ]


class NodeResponse(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    nodes: Annotated[List[Node], Field(max_length=100)]


class GPUResponse(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    gpus: Annotated[List[GPU], Field(max_length=100)]


class ImpactRow(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    utc_datetime: Annotated[
        Optional[datetime],
        Field(
            description="The start time of the request in UTC",
            examples=["2022-01-01T00:00:00Z"],
        ),
    ] = None
    request_duration_ms: Annotated[
        Optional[float],
        Field(
            description="The time the request took (as measured by client or proxy)",
            examples=[283],
        ),
    ] = None
    processing_duration_ms: Annotated[
        Optional[float],
        Field(
            description="The time taken in processing the request (as measured at execution)",
            examples=[238],
        ),
    ] = None
    request_cost: Annotated[
        Optional[float],
        Field(description="The cost to execute this request", examples=[0.18]),
    ] = None
    currency: Annotated[
        Optional[str],
        Field(description="The currency for the cost data", examples=["USD"]),
    ] = None
    integration_source: Annotated[
        Optional[str],
        Field(
            description="The integration used to source the data", examples=["litellm"]
        ),
    ] = None
    environment: Annotated[
        Optional[str],
        Field(
            description="Environment (prod/production indicates production)",
            examples=["staging"],
        ),
    ] = None
    session_id: Annotated[
        Optional[str], Field(description="The ID of the session (multiple requests)")
    ] = None
    trace_id: Annotated[
        Optional[str],
        Field(
            description="The trace ID of the request (multiple requests in one task)"
        ),
    ] = None
    request_id: Annotated[
        Optional[str], Field(description="The unique identifier of this request")
    ] = None
    client_id: Annotated[
        Optional[str], Field(description="The client to attribute this call to")
    ] = None
    project_id: Annotated[
        Optional[str], Field(description="The project to attribute this call to")
    ] = None
    application_id: Annotated[
        Optional[str], Field(description="The application to attribute this call to")
    ] = None
    model_id: Annotated[
        Optional[str],
        Field(description="The ID of the model requested", examples=["llama_31_8b"]),
    ] = None
    model_family: Annotated[
        Optional[str], Field(description="The family of the model", examples=["llama"])
    ] = None
    model_name: Annotated[
        Optional[str],
        Field(description="The name of the model", examples=["LLaMa v3.1 8B"]),
    ] = None
    model_hugging_face_path: Annotated[
        Optional[str],
        Field(
            description="The Hugging Face path of the model",
            examples=["meta/llama31_8b"],
        ),
    ] = None
    model_used_id: Annotated[
        Optional[str],
        Field(
            description="The ID of the model that did the inference",
            examples=["llama_31_8b_0125"],
        ),
    ] = None
    cloud_region: Annotated[
        Optional[str],
        Field(description="The region of cloud hosting", examples=["us-central1"]),
    ] = None
    managed_service_id: Annotated[
        Optional[str],
        Field(
            description="The ID of a managed service provider", examples=["aws-bedrock"]
        ),
    ] = None
    cloud_id: Annotated[
        Optional[str], Field(description="The ID of the cloud", examples=["aws"])
    ] = None
    cloud_instance_id: Annotated[
        Optional[str],
        Field(description="The instance type in the cloud", examples=["xl-4g-8a100"]),
    ] = None
    node_id: Annotated[
        Optional[str],
        Field(
            description="The ID of a custom or global node",
            examples=["h200-2024-build"],
        ),
    ] = None
    country: Optional[CountryCode] = None
    region: Optional[RegionCode] = None
    task: Annotated[Optional[Task], Field(examples=["text-generation"])] = None
    input_tokens: Annotated[
        Optional[int],
        Field(
            description="the number of input (or prompt) tokens",
            examples=[128],
            ge=0,
            le=100000000,
        ),
    ] = None
    input_audio_seconds: Annotated[
        Optional[int],
        Field(
            description="the duration of audio input in seconds",
            examples=[60],
            ge=0,
            le=100000,
        ),
    ] = None
    output_tokens: Annotated[
        Optional[int],
        Field(
            description="the number of output (or completion) tokens",
            examples=[128],
            ge=0,
            le=100000000,
        ),
    ] = None
    input_images: Annotated[Optional[List[Image]], Field(max_length=100)] = None
    input_steps: Annotated[
        Optional[int],
        Field(
            description="the number of steps to use in the model",
            examples=[50],
            ge=1,
            le=10000,
        ),
    ] = None
    output_images: Annotated[
        Optional[List[Image]],
        Field(description="a list of output image sizes", max_length=100),
    ] = None
    output_audio_seconds: Annotated[
        Optional[float],
        Field(
            description="the duration of audio output in seconds",
            examples=[60],
            ge=0.0,
            le=100000.0,
        ),
    ] = None
    output_audio_tokens: Annotated[
        Optional[int],
        Field(
            description="the number of audio tokens in the output",
            examples=[2300],
            ge=0,
            le=100000000,
        ),
    ] = None
    output_video_frames: Annotated[
        Optional[int],
        Field(
            description="the number of video frames (frame rate x duration)",
            examples=[60],
            ge=0,
            le=100000000,
        ),
    ] = None
    output_video_resolution: Annotated[
        Optional[int],
        Field(
            description="the resolution of the video in number of lines (for instance, 1080 for 1080p)",
            examples=[1080],
        ),
    ] = None


class Model(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    id: Annotated[str, Field(examples=["gpt-4-turbo"])]
    name: Annotated[Optional[str], Field(examples=["GPT-4 Turbo"])] = None
    family: Annotated[Optional[str], Field(examples=["gpt"])] = None
    hugging_face_path: Annotated[
        Optional[str], Field(examples=["EleutherAI/gpt-neo-2.7B"])
    ] = None
    benchmark_model_id: Annotated[Optional[str], Field(examples=["GPTJ-6B"])] = None
    total_params_billions: Annotated[Optional[float], Field(examples=[175])] = None
    number_of_experts: Annotated[Optional[int], Field(examples=[7])] = None
    params_per_expert_billions: Annotated[Optional[float], Field(examples=[8])] = None
    tensor_parallelism: Annotated[Optional[int], Field(examples=[1])] = None
    datatype: Annotated[Optional[DataType], Field(examples=["fp8"])] = None
    task: Annotated[Optional[Task], Field(examples=["text-generation"])] = None
    training_usage_energy_kwh: Annotated[Optional[float], Field(examples=[1013.1])] = (
        None
    )
    training_usage_emissions_kgco2e: Annotated[
        Optional[float], Field(examples=[1013.1])
    ] = None
    training_usage_water_l: Annotated[Optional[float], Field(examples=[1013.1])] = None
    training_embodied_emissions_kgco2e: Annotated[
        Optional[float], Field(examples=[11013.1])
    ] = None
    training_embodied_water_l: Annotated[Optional[float], Field(examples=[11013.1])] = (
        None
    )
    estimated_use_life_days: Annotated[Optional[float], Field(examples=[1013.1])] = None
    estimated_requests_per_day: Annotated[Optional[float], Field(examples=[1013.1])] = (
        None
    )
    fine_tuned_from_model_id: Annotated[
        Optional[str], Field(examples=["llama_31_8b"])
    ] = None


class GridMix(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    country: CountryCode
    region: Optional[RegionCode] = None
    gco2e_per_kwh: Annotated[float, Field(examples=[475], ge=0.0, le=2000.0)]


class ModelResponse(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    models: Annotated[List[Model], Field(max_length=100)]


class ImpactRequest(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    rows: Annotated[List[ImpactRow], Field(max_length=1000)]


class DebugInfo(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    model: Optional[Model] = None
    hardware_node: Optional[Node] = None
    grid_mix: Optional[GridMix] = None
    steps: Annotated[Optional[List[PredictionStep]], Field(max_length=100)] = None


class ModeledRow(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    inference_impact: Optional[ImpactMetrics] = None
    training_impact: Optional[ImpactMetrics] = None
    fine_tuning_impact: Optional[ImpactMetrics] = None
    total_impact: ImpactMetrics
    debug: Optional[DebugInfo] = None
    error: Optional[Error] = None


class ImpactResponse(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    rows: Annotated[List[ModeledRow], Field(max_length=1000)]
    total_energy_wh: Annotated[Optional[float], Field(examples=[0.13])] = None
    total_gco2e: Annotated[Optional[float], Field(examples=[0.81])] = None
    total_mlh2o: Annotated[Optional[float], Field(examples=[1.32])] = None
    has_errors: Annotated[bool, Field(examples=[False])]
