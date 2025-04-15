



# def format_visit_history(history) (Mehdi)












# def format_visit_details(visit) (Detelina)

@patch("rendering.get_html_end_block", return_value="End")
@patch("rendering.to_text_paragraph", return_value="Paragraph")
@patch("rendering.to_heading_line", return_value="Heading")
@patch("rendering.get_html_start_block", return_value="Start")
def test_format_visit_details_normal(mock_start, mock_heading, mock_paragraph, mock_end ):
    visit = {
    "id": 1,
    "timestamp": "2025-01-01 12:00:00",
    "ip": "127.0.0.1",
    "user_agent": "Chrome"
}
    result = format_visit_details(visit)
    expected = "StartHeadingParagraphParagraphParagraphEnd"
    assert result == expected

  
@patch("rendering.get_html_end_block", return_value="End")
@patch("rendering.to_text_paragraph", return_value="Paragraph")
@patch("rendering.to_heading_line", return_value="Heading")
@patch("rendering.get_html_start_block", return_value="Start")
def test_format_visit_details_missing_data(mock_start, mock_heading, mock_paragraph, mock_end ):
    visit = {
    "id": "2",
    "timestamp": "2025-01-01 12:00:00",
    "ip": "",
    "user_agent": "Chrome"
}
    result = format_visit_details(visit)
    expected = "StartHeadingParagraphParagraphParagraphEnd"
    assert result == expected

  











#def format_hello_greeting(name) (Shaheera)