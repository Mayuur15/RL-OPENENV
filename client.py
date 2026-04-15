# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

"""Hallucinations (FactCheck) Environment Client."""

from typing import Dict

from openenv.core import EnvClient
from openenv.core.client_types import StepResult
from openenv.core.env_server.types import State

from .models import HallucinationsAction, HallucinationsObservation


class HallucinationsEnv(
    EnvClient[HallucinationsAction, HallucinationsObservation, State]
):

   

 
    def _step_payload(self, action: HallucinationsAction) -> Dict:
        """
        Convert HallucinationsAction to JSON payload for step message.

        Args:
            action: HallucinationsAction instance

        Returns:
            Dictionary representation suitable for JSON encoding
        """
        return {
            "verdicts": action.verdicts,
            "confidences": action.confidences,
            "explanations": action.explanations,
            "sycophancy_override": action.sycophancy_override,
        }

    def _parse_result(self, payload: Dict) -> StepResult[HallucinationsObservation]:
        """
        Parse server response into StepResult[HallucinationsObservation].

        Args:
            payload: JSON response data from server

        Returns:
            StepResult with HallucinationsObservation
        """
        obs_data = payload.get("observation", {})
        observation = HallucinationsObservation(
            task_id=obs_data.get("task_id", 1),
            document=obs_data.get("document", ""),
            claims=obs_data.get("claims", []),
            num_claims=obs_data.get("num_claims", 0),
            social_pressure=obs_data.get("social_pressure"),
            step_feedback=obs_data.get("step_feedback"),
            done=payload.get("done", False),
            reward=payload.get("reward"),
            metadata=obs_data.get("metadata", {}),
        )

        return StepResult(
            observation=observation,
            reward=payload.get("reward"),
            done=payload.get("done", False),
        )

    def _parse_state(self, payload: Dict) -> State:
        """
        Parse server response into State object.

        Args:
            payload: JSON response from state request

        Returns:
            State object with episode_id and step_count
        """
        return State(
            episode_id=payload.get("episode_id"),
            step_count=payload.get("step_count", 0),
        )
