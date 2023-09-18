# Test file for testing functions in utils
import os
import sys
import torch
from megatron import utils

def test_get_sequence_ids():
    pass

def test_get_shifted_multimodal_position_ids():
    eps = 1e-7
    
    # Case 1: 1 image in between text
    text_positions = torch.tensor([[0, 2, 3, 4, 5, 6, 7]])
    vision_positions = torch.tensor([[1]])
    vision_seq_len = 2
    input_info = {
        "text": {
            "positions" : text_positions,
            "seq_length": 1
        },
        "vision": {
            "positions" : vision_positions,
            "seq_length": vision_seq_len,
        }
    }


    new_text_positions, new_vision_positions, _ = utils.get_shifted_multimodal_position_ids(input_info=input_info)
    assert torch.all(torch.abs(new_text_positions - torch.tensor([[0, 3, 4, 5, 6, 7, 8]])) < eps)
    assert torch.all(torch.abs(new_vision_positions - torch.tensor([[1, 2]])) < eps)
    
    # Case 2: Different image position
    text_positions = torch.tensor([[0, 1, 2, 5]])
    vision_positions = torch.tensor([[3]])
    vision_seq_len = 3
    input_info = {
        "text": {
            "positions" : text_positions,
            "seq_length": 1
        },
        "vision": {
            "positions" : vision_positions,
            "seq_length": vision_seq_len,
        }
    }

    new_text_positions, new_vision_positions, new_audio_positions = utils.get_shifted_multimodal_position_ids(input_info=input_info)

    assert torch.all(torch.abs(new_text_positions - torch.tensor([[0, 1, 2, 7]])) < eps)
    assert torch.all(torch.abs(new_vision_positions - torch.tensor([[3, 4, 5]])) < eps)

    # Case 3: Image position in the start 
    text_positions = torch.tensor([[1, 2, 5]])
    vision_positions = torch.tensor([[0]])
    vision_seq_len = 3
    input_info = {
        "text": {
            "positions" : text_positions,
            "seq_length": 1
        },
        "vision": {
            "positions" : vision_positions,
            "seq_length": vision_seq_len,
        }
    }

    new_text_positions, new_vision_positions, new_audio_positions = utils.get_shifted_multimodal_position_ids(input_info=input_info)

    assert torch.all(torch.abs(new_text_positions - torch.tensor([[3, 4, 7]])) < eps)
    assert torch.all(torch.abs(new_vision_positions - torch.tensor([[0, 1, 2]])) < eps)

    # Case 4: Image position at the end
    text_positions = torch.tensor([[0, 1, 2]])
    vision_positions = torch.tensor([[3]])
    vision_seq_len = 3
    input_info = {
        "text": {
            "positions" : text_positions,
            "seq_length": 1
        },
        "vision": {
            "positions" : vision_positions,
            "seq_length": vision_seq_len,
        }
    }

    new_text_positions, new_vision_positions, new_audio_positions = utils.get_shifted_multimodal_position_ids(input_info=input_info)

    assert torch.all(torch.abs(new_text_positions - torch.tensor([[0, 1, 2]])) < eps)
    assert torch.all(torch.abs(new_vision_positions - torch.tensor([[3, 4, 5]])) < eps)

    # Case 5: Multiple images 
    text_positions = torch.tensor([[0, 2, 5]])
    vision_positions = torch.tensor([[1, 4, ]])
    vision_seq_len = 3
    input_info = {
        "text": {
            "positions" : text_positions,
            "seq_length": 1
        },
        "vision": {
            "positions" : vision_positions,
            "seq_length": vision_seq_len,
        }
    }

    new_text_positions, new_vision_positions, new_audio_positions = utils.get_shifted_multimodal_position_ids(input_info=input_info)

    assert torch.all(torch.abs(new_text_positions - torch.tensor([[0, 4, 9]])) < eps)
    assert torch.all(torch.abs(new_vision_positions - torch.tensor([[1, 2, 3, 6, 7, 8]])) < eps)

    # Case 6: Zero images 
    text_positions = torch.tensor([[0, 1, 2, 5]])
    vision_positions = torch.tensor([[]])
    vision_seq_len = 3
    input_info = {
        "text": {
            "positions" : text_positions,
            "seq_length": 1
        },
        "vision": {
            "positions" : vision_positions,
            "seq_length": vision_seq_len,
        }
    }

    new_text_positions, new_vision_positions, new_audio_positions = utils.get_shifted_multimodal_position_ids(input_info=input_info)

    assert torch.all(torch.abs(new_text_positions - torch.tensor([[0, 1, 2, 5]])) < eps)
    assert torch.all(torch.abs(new_vision_positions - torch.tensor([[]])) < eps)

    # Case 7: Zero text
    text_positions = torch.tensor([[]])
    vision_positions = torch.tensor([[3]])
    vision_seq_len = 3
    input_info = {
        "text": {
            "positions" : text_positions,
            "seq_length": 1
        },
        "vision": {
            "positions" : vision_positions,
            "seq_length": vision_seq_len,
        }
    }

    new_text_positions, new_vision_positions, new_audio_positions = utils.get_shifted_multimodal_position_ids(input_info=input_info)

    assert torch.all(torch.abs(new_text_positions - torch.tensor([[]])) < eps)
    assert torch.all(torch.abs(new_vision_positions - torch.tensor([[3, 4, 5]])) < eps)

    # Case 8: Multiple samples 
    text_positions = torch.tensor([[0, 2, 5, -1, -1], [0, 1, 2, 5, -1]])
    vision_positions = torch.tensor([[1, 4, -1], [3, -1, -1]])
    vision_seq_len = 3
    input_info = {
        "text": {
            "positions" : text_positions,
            "seq_length": 1
        },
        "vision": {
            "positions" : vision_positions,
            "seq_length": vision_seq_len,
        }
    }

    new_text_positions, new_vision_positions, new_audio_positions = utils.get_shifted_multimodal_position_ids(input_info=input_info)
    assert torch.all(torch.abs(new_text_positions - torch.tensor([[0, 4, 9, 10, 11], [0, 1, 2, 7, 8]])) < eps)
    assert torch.all(torch.abs(new_vision_positions - torch.tensor([[1, 2, 3, 6, 7, 8, 12, 13, 14], [3, 4, 5, 9, 10, 11, 12, 13, 14]])) < eps)

def test_get_proxy_tokens():
    
    pass

def test_get_multimodal_mask():
    pass

def test_get_multimodal_attn_mask():
    pass 

def test_embedding_interleaving():
    pass

# Main function
def main():
    test_get_sequence_ids()
    test_get_shifted_multimodal_position_ids()
    test_get_proxy_tokens()
    test_get_multimodal_mask()
    test_get_multimodal_attn_mask()
    test_embedding_interleaving()

if __name__ == "__main__":
    main()