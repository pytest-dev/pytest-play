def test_junit_xml_system_out(testdir):
    yml_file = testdir.makefile(".yml", """
---
- provider: python
  type: assert
  expression: "1"
  comment: first assertion
- provider: python
  type: assert
  expression: "1 == 1"
  comment: second assertion
    """)
    assert yml_file.basename.startswith('test_')
    assert yml_file.basename.endswith('.yml')

    junit_xml_file = testdir.tmpdir.join('results.xml')
    result = testdir.runpytest('--junit-xml={0}'.format(junit_xml_file))

    result.assert_outcomes(passed=1)
    from xml.dom import minidom
    xmldoc = minidom.parse(junit_xml_file.strpath)
    system_out_nodes = xmldoc.getElementsByTagName('system-out')
    assert len(system_out_nodes) == 1
    system_out_node = system_out_nodes[0]
    assert system_out_node.parentNode.tagName == 'testcase'
    assert '1 == 1' in system_out_node.firstChild.nodeValue
    assert '\'expression\': \'1\'' in system_out_node \
        .firstChild.nodeValue


def test_junit_xml_system_out_elapsed(testdir):
    yml_file = testdir.makefile(".yml", """
---
- provider: python
  type: assert
  expression: "1"
  comment: first assertion
    """)
    assert yml_file.basename.startswith('test_')
    assert yml_file.basename.endswith('.yml')

    junit_xml_file = testdir.tmpdir.join('results.xml')
    result = testdir.runpytest('--junit-xml={0}'.format(junit_xml_file))

    result.assert_outcomes(passed=1)
    from xml.dom import minidom
    xmldoc = minidom.parse(junit_xml_file.strpath)
    system_out_nodes = xmldoc.getElementsByTagName('system-out')
    assert len(system_out_nodes) == 1
    system_out_node = system_out_nodes[0]
    assert system_out_node.parentNode.tagName == 'testcase'
    assert '\'_elapsed\':' in system_out_node.firstChild.nodeValue
    import re
    elapsed = re.search(
        "'_elapsed': ([0-9.]*)",
        system_out_node.firstChild.nodeValue).group(1)
    assert float(elapsed) > 0
