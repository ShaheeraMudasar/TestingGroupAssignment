# unit tests for functions: get_html_start_block, get_html_end_block






# unit test for functions: to_heading_line, to_text_paragraph

def test_to_heading_line_2():
    heading = to_heading_line("Hello", 2)
    expected = "<h2>Hello</h2>\n"
    assert heading == expected

def test_to_heading_line_3():
    heading = to_heading_line("Hello again", 3)
    expected = "<h3>Hello again</h3>\n"
    assert heading == expected

def test_to_heading_line_char():
    heading = to_heading_line("<Hello> & <b>Goodbye<b>", 1)
    expected = "<h1>&lt;Hello&gt; &amp; &lt;b&gt;Goodbye&lt;b&gt;</h1>\n"
    assert heading == expected

def test_to_heading_line_empty():
    heading = to_heading_line("", 1)
    expected = "<h1></h1>\n"
    assert heading == expected

#This test will fail. The function should take heading 1-6
def test_to_heading_line_outside_number():
    with pytest.raises(ValueError, match="Heading must be between 1 and 6."):
        to_heading_line("Hi", 0)


def test_to_text_paragraph_empty():
    text = to_text_paragraph("")
    expected = "<p></p>\n"
    assert text == expected

def test_to_text_paragraph_char():
    text = to_text_paragraph("<> &")
    expected = "<p>&lt;&gt; &amp;</p>\n"
    assert text == expected





# unit test for functions: to_error_message, to_basic_html_page




