# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

from typing import List, Optional
from openenv.core.env_server.types import Action, Observation
from pydantic import Field


class HallucinationsAction(Action):
    """Action for the FactCheck environment — the agent's verdicts on all claims."""

    verdicts: List[str] = Field(
        ...,
        description="Verdict per claim. Each must be 'true', 'false', or 'uncertain'.",
    )
    confidences: List[float] = Field(
        ...,
        description="Confidence score per verdict, each in [0.0, 1.0].",
    )
    explanations: List[str] = Field(
        ...,
        description=(
            "Reasoning per verdict. For 'false' verdicts must include the correct fact."
        ),
    )
    sycophancy_override: bool = Field(
        default=False,
        description=(
            "Set True if the agent is consciously ignoring social-pressure cues "
            "in the observation."
        ),
    )


class HallucinationsObservation(Observation):
    """Observation from the FactCheck environment — the document and claims to evaluate."""

    task_id: int = Field(
        default=1,
        description="Task difficulty: 1=easy, 2=medium, 3=hard.",
    )
    document: str = Field(
        default="",
        description="Full text of the document containing claims.",
    )
    claims: List[str] = Field(
        default_factory=list,
        description="Individual claims extracted from the document.",
    )
    num_claims: int = Field(
        default=0,
        description="Total number of claims the agent must evaluate.",
    )
    social_pressure: Optional[str] = Field(
        default=None,
        description=(
            "Sycophancy-pressure message injected in Task 3. "
            "None for Tasks 1 and 2."
        ),
    )
    step_feedback: Optional[str] = Field(
        default=None,
        description="Feedback from the previous step. None on reset().",
    )
