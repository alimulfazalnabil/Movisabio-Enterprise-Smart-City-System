import pytest
from src.services.optimization.policies.action_space import OptimizerAction
from src.services.optimization.policies.action_mask import ActionMask

def test_action_mask_minimum_green():
    masker = ActionMask(min_green_sec=10.0, max_green_sec=60.0)
    
    # At 5 seconds, we cannot terminate or change. We can hold or extend.
    mask = masker.generate_mask(phase_elapsed=5.0)
    
    assert mask[OptimizerAction.HOLD] is True
    assert mask[OptimizerAction.EXTEND_5] is True
    assert mask[OptimizerAction.EXTEND_10] is True
    assert mask[OptimizerAction.TERMINATE] is False
    assert mask[OptimizerAction.SELECT_NEXT] is False

def test_action_mask_maximum_green():
    masker = ActionMask(min_green_sec=10.0, max_green_sec=60.0)
    
    # At 58 seconds, we cannot hold or extend past 60. We must terminate/change.
    mask = masker.generate_mask(phase_elapsed=58.0)
    
    assert mask[OptimizerAction.HOLD] is True # We can hold for up to 2 seconds
    assert mask[OptimizerAction.EXTEND_5] is False
    assert mask[OptimizerAction.EXTEND_10] is False
    assert mask[OptimizerAction.TERMINATE] is True
    assert mask[OptimizerAction.SELECT_NEXT] is True

def test_action_mask_over_max():
    masker = ActionMask(min_green_sec=10.0, max_green_sec=60.0)
    
    # At 61 seconds, holding is illegal
    mask = masker.generate_mask(phase_elapsed=61.0)
    
    assert mask[OptimizerAction.HOLD] is False
    assert mask[OptimizerAction.EXTEND_5] is False
    assert mask[OptimizerAction.EXTEND_10] is False
    assert mask[OptimizerAction.TERMINATE] is True
    assert mask[OptimizerAction.SELECT_NEXT] is True
