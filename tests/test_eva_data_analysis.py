import pytest
from eva_data_analysis import text_to_duration, calculate_crew_size

def test_text_to_duration_float():
    """
    Test that text_to_duration returns expected ground truth values
    for typical durations with a non-zero minute component
    """
    actual_result = text_to_duration("10:20") 
    expected_result = 10.33333333
    assert actual_result == pytest.approx(expected_result)
    
def test_text_to_duration_integer():
    """
    Test that text_to_duration returns expected ground truth values
    for typical whole hour durations 
    """
    actual_result =  text_to_duration("10:00")
    expected_result = 10
    assert actual_result == expected_result

@pytest.mark.parametrize("input_value, expected_result", [
    ("", None),
    ("Valentina Tereshkova;", 1),
    ("Judith Resnik; Sally Ride;", 2),
])
def test_calculate_crew_size(input_value, expected_result):
    """
    Test that calculate_crew_size returns expected ground truth values
    for typical crew values
    """
    actual_result = calculate_crew_size(input_value)
    assert actual_result == expected_result


    # # Typical value 0
    # actual_result =  calculate_crew_size("")
    # expected_result = None
    # assert actual_result == expected_result

    # # Typical value 1
    # actual_result =  calculate_crew_size("alice in chains with 'quotes'")
    # expected_result = 1
    # assert actual_result == expected_result

    # # Typical value 2
    # actual_result =  calculate_crew_size("James Van Hoften;Bill Fisher;")
    # expected_result = 2
    # assert actual_result == expected_result

    # # Typical value 3
    # actual_result =  calculate_crew_size("James Van Hoften;Bill Fisher;bob l'eponge")
    # expected_result = 3
    # assert actual_result == expected_result
